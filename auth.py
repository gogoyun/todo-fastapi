from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models import get_db, User, PasswordResetToken
from config import settings
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def generate_reset_token() -> str:
    """生成密碼重設 token"""
    return secrets.token_urlsafe(32)

def create_password_reset_token(email: str, db: Session) -> str | None:
    """建立密碼重設 token 並儲存到資料庫"""
    # 檢查用戶是否存在
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    
    # 生成 token
    token = generate_reset_token()
    expires_at = datetime.utcnow() + timedelta(hours=1)  # 1小時後過期
    
    # 儲存到資料庫
    reset_token = PasswordResetToken(
        email=email,
        token=token,
        expires_at=expires_at
    )
    db.add(reset_token)
    db.commit()
    
    return token

def verify_reset_token(token: str, db: Session) -> str:
    """驗證重設 token 並回傳對應的 email"""
    reset_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token,
        PasswordResetToken.used == 0,
        PasswordResetToken.expires_at > datetime.utcnow()
    ).first()
    
    if not reset_token:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    return reset_token.email

def mark_token_as_used(token: str, db: Session):
    """標記 token 為已使用"""
    reset_token = db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()
    if reset_token:
        reset_token.used = 1
        db.commit()

def send_reset_email(email: str, token: str):
    """發送密碼重設郵件"""
    # 使用環境變數中的前端 URL
    reset_url = f"{settings.app_url}/reset-password?token={token}"
    
    # 檢查是否設定了郵件配置
    if not settings.smtp_username or not settings.smtp_password:
        # 開發環境：輸出到控制台
        print(f"密碼重設郵件已發送到 {email}")
        print(f"重設連結: {reset_url}")
        return
    
    try:
        # 建立郵件
        msg = MIMEMultipart()
        msg['From'] = settings.smtp_from_email or settings.smtp_username
        msg['To'] = email
        msg['Subject'] = '密碼重設請求'
        
        body = f'''
        您好,
        
        您請求重設密碼. 請點擊以下連結重設您的密碼:
        
        {reset_url}
        
        此連結將在1小時後過期.
        
        如果您沒有請求重設密碼, 請忽略此郵件.
        '''
        
        msg.attach(MIMEText(body, 'plain'))
        
        # 發送郵件
        server = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        text = msg.as_string()
        server.sendmail(settings.smtp_from_email or settings.smtp_username, email, text)
        server.quit()
        
        print(f"密碼重設郵件已成功發送到 {email}")
        
    except Exception as e:
        print(f"發送郵件失敗: {e}")
        # 在生產環境中，你可能想要記錄錯誤但不中斷流程
        if settings.environment == "development":
            print(f"重設連結: {reset_url}")
