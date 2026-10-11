from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional, List


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)
    role: str = "user"


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    name: str
    email: str
    role: str
    created_at: datetime


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
    title: Optional[str] = Field(default=None, min_length=5, max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = None
    status_id: Optional[int] = None
    assignee_id: Optional[int] = None
    priority: Optional[str] = None


class StatusOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sla_hours: Optional[int] = None


class RequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    number: str
    title: str
    description: Optional[str] = None
    category: Optional[CategoryOut] = None      # ← вместо object
    status: Optional[StatusOut] = None          # ← вместо object
    requester: Optional[UserOut] = None
    assignee: Optional[UserOut] = None
    priority: str
    created_at: datetime
    updated_at: datetime


class CommentCreate(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    request_id: int
    user: UserOut
    text: str
    created_at: datetime

class CategoryCreate(BaseModel):
    name: str
    code: str | None = None
    sla_hours: int = 24
