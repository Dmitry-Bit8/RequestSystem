from typing import Union
import re


def validate_title(title: str) -> bool:
    """Проверка корректности заголовка заявки"""
    if not title or not title.strip():
        raise ValueError("Заголовок не может быть пустым")
    if len(title) < 5:
        raise ValueError("Заголовок должен содержать минимум 5 символов")
    if len(title) > 200:
        raise ValueError("Заголовок слишком длинный (максимум 200 символов)")
    return True


def validate_description(description: str) -> bool:
    """Проверка корректности описания заявки"""
    if not description or not description.strip():
        raise ValueError("Описание не может быть пустым")
    if len(description) < 20:
        raise ValueError("Описание должно содержать минимум 20 символов")
    if len(description) > 5000:
        raise ValueError("Описание слишком длинное (максимум 5000 символов)")
    return True


def validate_priority(priority: int) -> bool:
    """Проверка корректности приоритета"""
    if priority not in [1, 2, 3]:
        raise ValueError("Приоритет должен быть 1, 2 или 3")
    return True


def validate_email(email: str) -> bool:
    """Проверка корректности email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError("Некорректный формат email")
    return True


def validate_username(username: str) -> bool:
    """Проверка корректности имени пользователя"""
    if not username or not username.strip():
        raise ValueError("Имя пользователя не может быть пустым")
    if len(username) < 3:
        raise ValueError("Имя пользователя должно содержать минимум 3 символа")
    if len(username) > 50:
        raise ValueError("Имя пользователя слишком длинное")
    return True
