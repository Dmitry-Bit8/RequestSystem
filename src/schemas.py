from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)
    role: str = "user"

class UserOut(BaseModel):
    id: int
    username: str
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class LoginData(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RequestCreate(BaseModel):
    title: str = Field(min_length=5, max_length=200)
    description: str = Field(min_length=10)
    category_id: int

class RequestUpdate(BaseModel):
    title: Optional[str] = Field(min_length=5, max_length=200)
    description: Optional[str]
    category_id: Optional[int]
    status_id: Optional[int]
    assignee_id: Optional[int]
    priority: Optional[str]

class RequestOut(BaseModel):
    id: int
    number: str
    title: str
    description: Optional[str]
    category: Optional[object]
    status: Optional[object]
    requester: Optional[UserOut]
    assignee: Optional[UserOut]
    priority: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    text: str = Field(min_length=1, max_length=1000)

class CommentOut(BaseModel):
    id: int
    request_id: int
    user: UserOut
    text: str
    created_at: datetime

    class Config:
        from_attributes = True

class StatusOut(BaseModel):
    id: int
    code: str
    name: str

    class Config:
        from_attributes = True

class CategoryOut(BaseModel):
    id: int
    name: str
    sla_hours: Optional[int]

    class Config:
        from_attributes = True
