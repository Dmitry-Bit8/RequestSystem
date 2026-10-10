from src.database import Base, engine, SessionLocal
from src.models import Status, User, Request  # ← добавьте сюда свои модели запросов, если они называются иначе
from src.security import hash_password

def seed():
   
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

   
    statuses = [
        {"code": "new",         "name": "Новая"},
        {"code": "in_progress", "name": "В работе"},
        {"code": "on_hold",     "name": "Приостановлена"},
        {"code": "resolved",    "name": "Решена"},
        {"code": "rejected",    "name": "Отклонена"},
    ]
    for s in statuses:
        if not db.query(Status).filter(Status.code == s["code"]).first():
            db.add(Status(**s))
    db.commit()

   
    users = [
        # Логин      Имя                 Email                Пароль        Роль
        ("admin",  "Администратор",     "admin@test.ru",     "admin123",   "admin"),
        ("ivanov", "Иванов Иван",       "ivanov@test.ru",    "ivan123",    "user"),
        ("petrov", "Петров Пётр",       "petrov@test.ru",    "petr123",    "user"),
        ("sidorov","Сидоров Сидор",     "sidorov@test.ru",   "sidr123",    "user"),
        ("exec1",  "Кузнецов Алексей",  "exec1@test.ru",     "exec123",    "executor"),
        ("exec2",  "Смирнова Ольга",    "exec2@test.ru",     "exec2123",   "executor"),
    ]
    for username, name, email, password, role in users:
        if not db.query(User).filter(User.username == username).first():
            db.add(User(
                username=username,
                name=name,
                email=email,
                hashed_password=hash_password(password),
                role=role,
            ))
    db.commit()


    db.close()
    print("✅ Данные успешно добавлены!")

if __name__ == "__main__":
    seed()
