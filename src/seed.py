from src.database import Base, engine, SessionLocal
from src.models import Status, User, Request
from src.security import hash_password
import random
import uuid
from datetime import datetime, timedelta


def generate_number():
    """Генерирует уникальный номер заявки"""
    return f"REQ-{uuid.uuid4().hex[:8].upper()}"


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

    users_data = [
        ("admin",   "Администратор",    "admin@test.ru",   "admin123", "admin"),
        ("ivanov",  "Иванов Иван",      "ivanov@test.ru",  "ivan123",  "user"),
        ("petrov",  "Петров Пётр",      "petrov@test.ru",  "petr123",  "user"),
        ("sidorov", "Сидоров Сидор",    "sidorov@test.ru", "sidr123",  "user"),
        ("exec1",   "Кузнецов Алексей", "exec1@test.ru",   "exec123",  "executor"),
        ("exec2",   "Смирнова Ольга",   "exec2@test.ru",   "exec2123", "executor"),
    ]
    
    for username, name, email, password, role in users_data:
        if not db.query(User).filter(User.username == username).first():
            db.add(User(
                username=username,
                name=name,
                email=email,
                hashed_password=hash_password(password),
                role=role,
            ))
    db.commit()

    if db.query(Request).count() > 0:
        print("ℹ️  Заявки уже есть в БД — пропускаем генерацию.")
        db.close()
        return


    all_statuses = db.query(Status).all()
    all_users = db.query(User).all()

  
    executors = [u for u in all_users if u.username in ("exec1", "exec2")]
    requesters = [u for u in all_users if u.username not in ("exec1", "exec2", "admin")]

   
    if not requesters:
        requesters = all_users
    if not executors:
        executors = all_users

    
    templates = [
        ("Сломалась клавиатура",    "Клавиатура перестала работать после перезагрузки",       "Оборудование", "high"),
        ("Не работает сеть",        "Отсутствует доступ в интернет на 3 этаже",              "Сеть",         "critical"),
        ("Не устанавливается ПО",   "Ошибка при установке Microsoft Office",                  "ПО",           "medium"),
        ("Нет доступа к файлам",    "Не могу открыть общую папку",                            "Доступ",       "high"),
        ("Заменить монитор",        "Монитор мерцает и гаснет",                               "Оборудование", "low"),
        ("Обновить антивирус",      "Антивирус устарел, требуется обновление баз",            "ПО",           "medium"),
        ("Настроить принтер",       "Необходимо добавить принтер на рабочее место",           "Оборудование", "medium"),
        ("Ошибка в 1С",             "При запуске 1С ошибка подключения к базе",               "ПО",           "high"),
        ("Доступ к CRM",            "Новому сотруднику нужен доступ к CRM",                   "Доступ",       "medium"),
        ("Заменить ноутбук",        "Ноутбук устарел и не тянет задачи",                       "Оборудование", "high"),
        ("Проблема с Wi-Fi",        "Wi-Fi постоянно отключается",                            "Сеть",         "medium"),
        ("Установить VPN",          "Нужен VPN для удалённой работы",                          "Сеть",         "high"),
        ("Настроить почту",         "Не настроен Outlook на новом ПК",                        "ПО",           "low"),
        ("Сбросить пароль",         "Забыл пароль от учётной записи",                         "Доступ",       "critical"),
        ("Заменить мышь",           "Мышь работает с перебоями",                              "Оборудование", "low"),
        ("Проблемы с Teams",        "Не отображаются контакты в Teams",                       "ПО",           "medium"),
        ("Доступ к серверу",        "Требуется доступ к dev-серверу",                         "Доступ",       "high"),
        ("Медленный ПК",            "Компьютер работает очень медленно",                      "Оборудование", "medium"),
        ("Не работает камера",      "Веб-камера не определяется системой",                    "Оборудование", "medium"),
        ("Ошибка в Excel",          "Макросы перестали работать",                             "ПО",           "high"),
        ("Настроить сканер",        "Нужно настроить сканер документов",                      "Оборудование", "low"),
        ("Восстановить данные",     "Случайно удалил важные файлы",                           "Данные",       "critical"),
        ("Проблема со звуком",      "Нет звука при видеоконференциях",                        "Оборудование", "medium"),
        ("Установить Python",       "Установить Python и нужные библиотеки",                  "ПО",           "medium"),
        ("Настроить бэкап",         "Настроить резервное копирование",                        "Данные",       "high"),
        ("Проблема с питанием",     "Ноутбук отключается от питания",                         "Оборудование", "critical"),
        ("Обновить драйверы",       "Требуется обновление драйверов",                         "ПО",           "low"),
        ("Создать общую папку",     "Нужна общая папка для отдела",                           "Доступ",       "medium"),
        ("Настроить 2FA",           "Включить двухфакторную аутентификацию",                  "Доступ",       "high"),
        ("Принтер не печатает",     "Принтер выдаёт ошибку при печати",                       "Оборудование", "medium"),
        ("Обновить ОС",             "Обновить Windows до последней версии",                   "ПО",           "medium"),
        ("Проверить на вирусы",     "Возможно заражение компьютера",                          "Безопасность", "critical"),
        ("Новое рабочее место",     "Настроить рабочее место для нового сотрудника",          "Оборудование", "high"),
        ("Выдать бейдж",            "Пропуск для нового сотрудника",                          "Доступ",       "low"),
        ("Проблема с БД",           "Не удаётся подключиться к базе данных",                  "Данные",       "critical"),
        ("Модернизация ПК",         "Компьютер не отвечает требованиям",                      "Оборудование", "high"),
        ("Настроить RDP",           "Удалённый доступ для работы из дома",                    "Сеть",         "high"),
        ("Установить SSL",          "SSL-сертификат на веб-сервер",                           "Безопасность", "medium"),
        ("Обучить работе с CRM",    "Провести обучение сотрудников",                          "Прочее",       "low"),
        ("Заменить блок питания",   "Блок питания ноутбука шумит",                            "Оборудование", "high"),
        ("Ошибка входа",            "Ошибка авторизации в системе",                           "Доступ",       "critical"),
        ("Настроить факс",          "Настроить факс в бухгалтерии",                           "Оборудование", "low"),
    ]

  
    status_weights = {
        "new": 0.25,
        "in_progress": 0.30,
        "on_hold": 0.10,
        "resolved": 0.25,
        "rejected": 0.10,
    }

    
    priority_weights = {
        "low": 0.25,
        "medium": 0.40,
        "high": 0.25,
        "critical": 0.10,
    }

    for title, desc, category, priority in templates:
        number = generate_number()

       
        status_code = random.choices(
            list(status_weights.keys()),
            weights=list(status_weights.values()),
            k=1
        )[0]

        status = next(
            (s for s in all_statuses if str(s.code) == str(status_code)),
            all_statuses[0]  
        )




        
        requester = random.choice(requesters)
        executor = random.choice(executors) if random.random() < 0.6 else None

        
        days_ago = random.randint(0, 30)
        created_at = datetime.utcnow() - timedelta(days=days_ago)
        due_date = created_at + timedelta(hours=random.randint(1, 72))

               
        assert status is not None
        data = {
            "number": f"REQ-{random.randint(100000, 999999)}",
            "title": f"Заявка №{random.randint(100, 999)}",
            "description": "Описание проблемы...",
            "created_at": created_at,
            "due_date": due_date,
            "status_id": status.id,
            "requester_id": requester.id,
            "assignee_id": executor.id if executor else None
        }


        
        new_request = Request(**data)
        db.add(new_request)

    db.commit()
    print("=" * 50)
    print("✅ Данные успешно добавлены!")
    print("=" * 50)
    print(f"📊 Статусов:       {db.query(Status).count()}")
    print(f"👤 Пользователей:  {db.query(User).count()}")
    print(f"📝 Заявок:         {db.query(Request).count()}")
    print("\n📈 Заявки по статусам:")
    for s in all_statuses:
        cnt = db.query(Request).filter(Request.status_id == s.id).count()
        print(f"   • {s.name}: {cnt}")

    db.close()


if __name__ == "__main__":
    seed()
