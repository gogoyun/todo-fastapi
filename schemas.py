from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional, Any, List

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

    model_config = {"from_attributes": True}

# Todo 建立用
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: int = Field(
        default=0,
        description="任務狀態：0=未完成, 1=已完成",
        ge=0,
        le=1
    )

# Todo 更新用
class TodoUpdate(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: Optional[int] = Field(
        default=None,
        description="任務狀態：0=未完成, 1=已完成",
        ge=0,
        le=1
    )

# 回傳 Todo 用
class TodoOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: Optional[int] = Field(
        description="任務狀態：0=未完成, 1=已完成"
    )
    owner_id: int

    model_config = {"from_attributes": True}

class APIResponse(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None

# 直接定義一個 Todo 陣列的 schema
TodoCreateList = List[TodoCreate]

class TodoStatusUpdate(BaseModel):
    status: int = Field(
        description="任務狀態：0=未完成, 1=已完成",
        ge=0,
        le=1
    )

# 直接定義一個 TodoUpdate 陣列的 schema
TodoUpdateList = List[TodoUpdate]
