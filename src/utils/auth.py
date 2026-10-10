from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.database import get_db
from src.models import User
import os

# --- Конфигурация JWT ---
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-me-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- Настройка паролей ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Настройка OAuth2 ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Хеширование пароля ---
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# --- Проверка пароля ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# --- Создание JWT токена ---
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Получение текущего пользователя ---
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учётные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Декодируем токен
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Получаем email из payload (с проверкой типа)
        email_value = payload.get("sub")
        if email_value is None:
            raise credentials_exception

        email = str(email_value)  # Приводим к строке
    except JWTError:
        raise credentials_exception


    # Получаем пользователя из БД
    stmt = select(User).where(User.email == email)
    user = db.scalars(stmt).first()
    if user is None:
        raise credentials_exception

    return user
