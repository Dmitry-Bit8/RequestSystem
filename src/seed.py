from src.database import SessionLocal
from src.models import UserRole, Status, Category
from src.services.user_service import UserService
from src import models


def seed():
    db = SessionLocal()
    try:
        # --- Статусы ---
        statuses = [
            {"code": "new", "name": "Новая"},
            {"code": "in_progress", "name": "В работе"},
            {"code": "resolved", "name": "Решена"},
        ]
        for s in statuses:
            if not db.query(Status).filter(Status.code == s["code"]).first():
                db.add(Status(code=s["code"], name=s["name"]))
        db.commit()

        # --- Категории ---
        categories = [
            {"name": "Учебный процесс", "sla_hours": 24},
            {"name": "Общежитие", "sla_hours": 48},
            {"name": "IT-поддержка", "sla_hours": 8},
            {"name": "Библиотека", "sla_hours": 72},
            {"name": "Стипендия", "sla_hours": 48},
        ]
        for c in categories:
            if not db.query(Category).filter(Category.name == c["name"]).first():
                db.add(Category(name=c["name"], sla_hours=c["sla_hours"]))
        db.commit()

        # --- Пользователи через сервис ---
        svc = UserService(db)
        test_users = [
            {"username": "admin", "email": "admin@example.com",
             "password": "admin123", "role": UserRole.ADMIN},
            {"username": "ivanov", "email": "ivanov@example.com",
             "password": "student123", "role": UserRole.USER},
            {"username": "exec1", "email": "exec1@example.com",
             "password": "exec123", "role": UserRole.EXECUTOR},
        ]
        for u in test_users:
            try:
                svc.create_user(
                    username=u["username"],
                    email=u["email"],
                    password=u["password"],
                    role=u["role"],
                )
            except ValueError as e:
                print(f"⚠️ {u['username']}: {e}")

        print("✅ Данные успешно добавлены!")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
