from enum import Enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base


class UserRole(str, Enum):
    ADMIN = "admin"
    EXECUTOR = "executor"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=True)      
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default=UserRole.USER.value)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


class Status(Base):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True)
    code = Column(String(30), unique=True, nullable=False)
    name = Column(String(50), nullable=False)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    sla_hours = Column(Integer, default=24)


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    number = Column(String(20), unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"))
    status_id = Column(Integer, ForeignKey("statuses.id"))
    requester_id = Column(Integer, ForeignKey("users.id"))
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    priority = Column(String(10), default="medium")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    due_date = Column(DateTime, nullable=True)

    category = relationship("Category")
    status = relationship("Status")
    requester = relationship("User", foreign_keys=[requester_id])
    assignee = relationship("User", foreign_keys=[assignee_id])
    comments = relationship("Comment", back_populates="request")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("requests.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    request = relationship("Request", back_populates="comments")
    user = relationship("User")