from typing import Optional, List
from src.models import User, UserRole
from src.utils.validators import validate_email, validate_username

import hashlib


class UserService:
    def __init__(self, db):
        self.db = db

    def create_user(self, username: str, email: str, password: str,
                    role: UserRole = UserRole.USER) -> User:
        """Создание нового пользователя"""
        # Валидация
        validate_username(username)
        validate_email(email)

        # Проверка уникальности
        if self.get_user_by_username(username):
            raise ValueError(f"Пользователь с именем {username} уже существует")

        # Хеширование пароля
        hashed = hashlib.sha256(password.encode()).hexdigest()

        user = User(
            username=username,
            email=email,
            hashed_password=hashed,
            role=role
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Получение пользователя по имени"""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Получение пользователя по email"""
        return self.db.query(User).filter(User.email == email).first()

    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Аутентификация пользователя"""
        user = self.get_user_by_username(username)
        if user:
            hashed = hashlib.sha256(password.encode()).hexdigest()
            if user.hashed_password == hashed: # type: ignore
                return user
        return None

    def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        """Обновление данных пользователя"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            if 'email' in kwargs:
                validate_email(kwargs['email'])
            if 'username' in kwargs:
                validate_username(kwargs['username'])
            if 'password' in kwargs:
                kwargs['hashed_password'] = hashlib.sha256(
                    kwargs['password'].encode()
                ).hexdigest()
                del kwargs['password']

            for key, value in kwargs.items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        """Удаление пользователя"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

    def get_all_users(self) -> List[User]:
        """Получение списка всех пользователей"""
        return self.db.query(User).all()

    def get_executors(self) -> List[User]:
        """Получение списка исполнителей"""
        return self.db.query(User).filter(User.role == UserRole.EXECUTOR).all()
