from pydantic import BaseModel, EmailStr, constr
from typing import Optional

# 會員註冊用
class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=8)
    name: str

# 會員登入用
class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=8)

# 回傳用戶資訊（不含密碼）
class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        orm_mode = True

# Todo 建立用
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

# Todo 更新用
class TodoUpdate(BaseModel):
    title: str
    description: Optional[str] = None

# 回傳 Todo 用
class TodoOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    owner_id: int

    class Config:
        orm_mode = True
