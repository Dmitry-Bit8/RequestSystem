# Заголовок документа

О проекте
Приложение для автоматизации обработки заявок в организации. Позволяет создавать, отслеживать и управлять заявками.

Технологии: Python 3.12+, SQLite, Git, VS Code

Автор: [Ваше Фамилия Имя]

Дата: 08.10.2026

Архитектура

Слоистая архитектура:

Presentation → Service → Repository → Database

Слой Ответственность

Presentation CLI-интерфейс

Service Бизнес-логика

Repository Работа с БД

Database SQLite

Структура проекта

RequestSystem/

├── docs/          # Документация (ТЗ, диаграммы, AI-журнал)

├── src/           # Исходный код

│   ├── models/    # Классы

│   ├── services/  # Бизнес-логика

│   ├── repos/     # Работа с БД

│   └── main.py    # Точка входа

├── tests/         # Тесты

├── schema.sql     # Схема БД

├── seed.sql       # Тестовые данные

└── README.md

Установка и запуск

bash

Копировать

git clone <https://github.com/username/RequestSystem.git>

cd RequestSystem

python -m venv venv

venv\Scripts\activate  # Windows

source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt

python src/init_db.py

python src/main.py

Основные команды

python main.py login — вход

python main.py create_request — создать заявку

python main.py list_requests — список заявок

python main.py update_status id ,status — изменить статус

python main.py add_comment id "текст" — добавить комментарий

База данных

Таблицы: Users, Requests, Statuses, Categories, Comments

Пример запроса:

sql

Копировать

SELECT * FROM Requests WHERE status_id = 2;

Использование ИИ

Нейросети использовались для генерации ТЗ, проектирования архитектуры, SQL-запросов и UX-аудита. Подробности в docs/ai_journal.md.

Тестирование

bash

Копировать

pytest tests/ -v

Красноперов Дмитрий Васильевич
[GitHub профиль](https://github.com/Dmitry-Bit8/RequestSystem)

## RequestSystem — Система учёта заявок

## Описание

Веб-приложение для подачи, обработки и отслеживания заявок.

## Технологии

- Python 3.12+
- FastAPI
- SQLAlchemy
- SQLite
- JWT-авторизация
- Docker

## Установка и запуск

### Локальный запуск
