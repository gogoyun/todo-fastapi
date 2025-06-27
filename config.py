from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 告訴 Pydantic Settings 去讀取 .env 檔案
    # extra='ignore' 表示如果 .env 有額外變數但模型未定義，則忽略
    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

    # JWT 設定
    secret_key: str
    algorithm: str = "HS256" # 常用於 JWT
    
    # 資料庫設定
    database_url: str = "sqlite:///./todo.db"
    
    # 郵件設定
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    
    # 應用程式設定
    app_url: str = "http://localhost:5173"  # 前端 URL
    environment: str = "development"  # development, production

settings = Settings()

# 可以做一個簡單的檢查
if not settings.secret_key:
    raise ValueError("SECRET_KEY environment variable not set in .env or environment.")