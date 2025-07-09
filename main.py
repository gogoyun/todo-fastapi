from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth import get_password_hash, verify_password, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_password_reset_token, verify_reset_token, mark_token_as_used, send_reset_email
from models import Base, engine, get_db, User, Todo
from schemas import UserCreate, UserLogin, UserOut, TodoCreate, TodoOut, TodoUpdate, APIResponse, TodoCreateList, TodoStatusUpdate, TodoUpdateList, ForgotPasswordRequest, ResetPasswordRequest
from datetime import timedelta
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

# 設定 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # "http://localhost:5173"
        "https://gogoyun.github.io"
    ],  # 允許所有來源（開發環境用）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# 自訂 HTTPException handler，讓錯誤也有統一格式
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )

@app.post("/register", response_model=APIResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, name=user.name, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "code": 200,
        "message": "註冊成功",
        "data": UserOut.model_validate(new_user)
    }

@app.post("/login", response_model=APIResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {
        "code": 200,
        "message": "登入成功",
        "data": {"access_token": access_token, "name": db_user.name, "token_type": "bearer"}
    }

@app.post("/forgot-password", response_model=APIResponse)
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    try:
        # 建立重設 token
        token = create_password_reset_token(request.email, db)
        
        # 如果 token 存在 (表示用戶存在)，才發送郵件
        if token:
            send_reset_email(request.email, token)
        
        # 為了安全，無論用戶是否存在，都回傳成功的訊息
        return {
            "code": 200,
            "message": "密碼重設郵件已發送",
            "data": None
        }
    except Exception as e:
        # 這裡可以記錄錯誤，但不應將詳細資訊回傳給客戶端
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

@app.post("/reset-password", response_model=APIResponse)
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        # 驗證 token
        email = verify_reset_token(request.token, db)
        
        # 更新用戶密碼
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # 雜湊新密碼
        hashed_password = get_password_hash(request.new_password)
        user.hashed_password = hashed_password
        
        # 標記 token 為已使用
        mark_token_as_used(request.token, db)
        
        db.commit()
        
        return {
            "code": 200,
            "message": "密碼重設成功",
            "data": None
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to reset password")

@app.post("/todos", response_model=APIResponse)
def create_todos(todos: TodoCreateList, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_todos = []
    for todo in todos:
        new_todo = Todo(title=todo.title, description=todo.description, owner_id=current_user.id)
        db.add(new_todo)
        new_todos.append(new_todo)
    
    db.commit()
    for todo in new_todos:
        db.refresh(todo)
    
    return {
        "code": 200,
        "message": "建立成功",
        "data": [TodoOut.model_validate(todo) for todo in new_todos]
    }

@app.get("/todos", response_model=APIResponse)
def read_todos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todos = db.query(Todo).filter(Todo.owner_id == current_user.id).all()
    return {
        "code": 200,
        "message": "查詢成功",
        "data": [TodoOut.model_validate(todo) for todo in todos]
    }

@app.put("/todos", response_model=APIResponse)
def update_todos(
    updates: TodoUpdateList,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_todos = []
    for todo in updates:
        db_todo = db.query(Todo).filter(Todo.id == todo.id, Todo.owner_id == current_user.id).first()
        if not db_todo:
            raise HTTPException(status_code=404, detail=f"Todo with id {todo.id} not found")
        
        db_todo.title = todo.title
        if todo.description is not None:
            db_todo.description = todo.description
        if todo.status is not None:
            db_todo.status = todo.status
        
        updated_todos.append(db_todo)
    
    db.commit()
    for todo in updated_todos:
        db.refresh(todo)
    
    return {
        "code": 200,
        "message": "更新成功",
        "data": [TodoOut.model_validate(todo) for todo in updated_todos]
    }

@app.delete("/todos/{todo_id}", response_model=APIResponse)
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == current_user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    deleted_todo = TodoOut.model_validate(db_todo)
    db.delete(db_todo)
    db.commit()
    return {
        "code": 200,
        "message": "刪除成功",
        "data": deleted_todo
    }

@app.patch("/todos/{todo_id}/status", response_model=APIResponse)
def update_todo_status(
    todo_id: int, 
    status_update: TodoStatusUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == current_user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db_todo.status = status_update.status
    db.commit()
    db.refresh(db_todo)
    
    return {
        "code": 200,
        "message": "狀態更新成功",
        "data": TodoOut.model_validate(db_todo)
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}
