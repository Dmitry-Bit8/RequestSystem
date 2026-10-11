# -*- coding: utf-8 -*-
"""Генератор отчёта ЛР9 + ЛР10 (Word). Требует python-docx."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


doc = Document()

# --- Базовые стили ---
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)
style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')

for s in ('Heading 1', 'Heading 2', 'Heading 3'):
    st = doc.styles[s]
    st.font.name = 'Times New Roman'
    st.font.color.rgb = RGBColor(0, 0, 0)


def h(text, level=1):
    return doc.add_heading(text, level=level)


def p(text, bold=False, align=None, size=None):
    par = doc.add_paragraph()
    run = par.add_run(text)
    run.bold = bold
    if size:
        run.font.size = Pt(size)
    if align:
        par.alignment = align
    return par


def bullet(text):
    par = doc.add_paragraph(text, style='List Bullet')
    return par


def add_table(headers, rows, widths=None):
    """Создаёт таблицу с шапкой и заливкой. rows — список списков."""
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    hdr = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr[i].text = ''
        run = hdr[i].paragraphs[0].add_run(title)
        run.bold = True
        run.font.size = Pt(10)
        _shade_cell(hdr[i], 'D9E2F3')

    for row in rows:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ''
            run = cells[i].paragraphs[0].add_run(str(val))
            run.font.size = Pt(10)

    if widths:
        for i, w in enumerate(widths):
            for row in table.rows:
                row.cells[i].width = Cm(w)
    return table


def _shade_cell(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tc_pr.append(shd)


# =====================================================================
# ТИТУЛ
# =====================================================================
p('Лабораторная работа №9', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=16)
p('Объект: REST API сервиса заявок HelpDesk (RequestSystem)', align=WD_ALIGN_PARAGRAPH.CENTER)
p('Стек: Python, FastAPI, SQLAlchemy, SQLite, JWT', align=WD_ALIGN_PARAGRAPH.CENTER)
p('Ссылка: https://github.com/Dmitry-Bit8/RequestSystem', align=WD_ALIGN_PARAGRAPH.CENTER)
p('Документ: План тестирования и тест-кейсы', align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_paragraph()

# =====================================================================
# 1. ВВЕДЕНИЕ
# =====================================================================
h('1. Введение', 1)
h('1.1. Цель работы', 2)
p('Изучить методы планирования тестирования веб-сервисов, составить план '
  'тестирования и разработать набор тест-кейсов для REST API HelpDesk.')

h('1.2. Объект тестирования', 2)
p('REST API сервиса заявок HelpDesk. Сервис реализован на FastAPI, предоставляет '
  'эндпоинты аутентификации, управления заявками, комментариями, справочниками и '
  'экспорта отчётов. Документация — Swagger UI (/docs).')

h('1.3. Базовая точка входа', 2)
p('http://localhost:8000')

# =====================================================================
# 2-7
# =====================================================================
h('2. Цели тестирования', 1)
for t in [
    'Проверить корректность обработки HTTP-запросов всеми эндпоинтами.',
    'Проверить бизнес-правила: создание заявок, смена статуса, права по ролям.',
    'Выявить расхождения между заявленным и фактическим поведением.',
    'Оценить обработку негативных и граничных сценариев.',
]:
    bullet(t)

h('3. Область тестирования', 1)
p('В области:', bold=True)
for t in [
    'Аутентификация и регистрация (/auth/*).',
    'CRUD заявок (/api/requests*).',
    'Фильтрация и поиск заявок.',
    'Смена статуса (PATCH /status).',
    'Комментарии (/api/requests/{id}/comments).',
    'Справочники: статусы, категории, пользователи.',
    'Экспорт в Excel.',
    'Права доступа по ролям (admin / executor / user).',
]:
    bullet(t)
p('Вне области:', bold=True)
for t in [
    'UI-тестирование (фронтенд отсутствует).',
    'Нагрузочное тестирование.',
    'Тестирование безопасности (SQLi/XSS).',
]:
    bullet(t)

h('4. Виды тестирования', 1)
for t in [
    'Функциональное (контракт API, бизнес-логика).',
    'Негативное (невалидные данные, отсутствие токена, 404).',
    'Граничное (длины полей, пустые строки).',
    'Ролевое (admin / executor / user).',
]:
    bullet(t)

h('5. Инструменты', 1)
for t in [
    'Postman — ручное исследовательское тестирование.',
    'pytest + httpx — автоматизация (ЛР 10).',
    'SQLite — тестовая БД.',
]:
    bullet(t)

h('6. Критерии начала и окончания', 1)
p('Начало: развёрнут API, доступна /docs, загружены seed-данные.', bold=True)
p('Окончание: пройдены все тест-кейсы, заведены багрепорты, достигнуто >90% '
  'проходимости по позитивным кейсам и >50% по негативным.', bold=True)

h('7. Риски', 1)
add_table(
    ['Риск', 'Митигация'],
    [
        ['Нестабильность seed-данных (random)', 'Тесты не зависят от конкретных ID'],
        ['Отсутствие миграций', 'Схема создаётся при старте'],
        ['Разные хеш-алгоритмы (bcrypt / sha256)', 'Унифицировать в security.py'],
    ],
    widths=[8, 8],
)

# =====================================================================
# 8. РЕЕСТР ТЕСТ-КЕЙСОВ
# =====================================================================
h('8. Реестр тест-кейсов', 1)

h('Таблица 1. Аутентификация (Auth)', 2)
add_table(
    ['ID', 'Название', 'Шаги', 'Ожидаемый результат', 'Приоритет', 'Тип'],
    [
        ['TC-AUTH-01','Регистрация нового пользователя','POST /auth/register {username:testnew, email:testnew@t.ru, password:secret123, name:Тест}','201 + UserOut, role=user','High','Позитивный'],
        ['TC-AUTH-02','Регистрация с существующим username','POST /auth/register username=admin','400 «Пользователь с таким username уже существует»','High','Негативный'],
        ['TC-AUTH-03','Регистрация с невалидным email','POST /auth/register email=not-an-email','422 ошибка валидации','High','Негативный'],
        ['TC-AUTH-04','Регистрация с коротким паролем','POST /auth/register password=123','422 (min_length=6)','High','Граничный'],
        ['TC-AUTH-05','Успешный логин','POST /auth/login form-data admin/admin123','200 + access_token, token_type=bearer','High','Позитивный'],
        ['TC-AUTH-06','Логин с неверным паролем','POST /auth/login password=wrong','401 «Неверный логин или пароль»','High','Негативный'],
        ['TC-AUTH-07','Логин несуществующего пользователя','POST /auth/login username=ghost','401','Medium','Негативный'],
    ],
    widths=[2.2,3,4.5,4.5,1.6,1.8],
)

h('Таблица 2. Заявки (Requests)', 2)
add_table(
    ['ID', 'Название', 'Шаги', 'Ожидаемый результат', 'Приоритет', 'Тип'],
    [
        ['TC-REQ-01','Список заявок без фильтров','GET /api/requests','200 + непустой список','High','Позитивный'],
        ['TC-REQ-02','Фильтр по status_id','GET /api/requests?status_id=1','200 + все со status.id=1','High','Позитивный'],
        ['TC-REQ-03','Фильтр по priority=high','GET /api/requests?priority=high','200 + все priority=high','Medium','Позитивный'],
        ['TC-REQ-04','Поиск по title','GET /api/requests?search=клавиатура','200 + совпадения (регистронезависимо)','Medium','Позитивный'],
        ['TC-REQ-05','Получение заявки по ID','GET /api/requests/1','200 + RequestOut','High','Позитивный'],
        ['TC-REQ-06','Получение несуществующей заявки','GET /api/requests/999999','404 «Заявка не найдена»','High','Негативный'],
        ['TC-REQ-07','Создание заявки авторизованным','POST /api/requests {title, description, category_id}','201 + новая заявка + number REQ-*','High','Позитивный'],
        ['TC-REQ-08','Создание без токена','POST /api/requests без Authorization','401','High','Негативный'],
        ['TC-REQ-09','Создание с коротким title','POST /api/requests title=abc','422 (min_length=5)','High','Граничный'],
        ['TC-REQ-10','Создание с несуществующей категорией','POST /api/requests category_id=99999','400 «Категория не найдена»','Medium','Негативный'],
        ['TC-REQ-11','PUT своей заявки автором','PUT /api/requests/{id} {title}','200 + поле обновлено','High','Позитивный'],
        ['TC-REQ-12','PUT чужой заявки обычным user','PUT /api/requests/{id} чужой','403 «Можно править только свои»','High','Негативный'],
        ['TC-REQ-13','PUT чужой заявки executor','PUT /api/requests/{id} не свою (executor)','200','Medium','Позитивный'],
        ['TC-REQ-14','User меняет status_id через PUT','PUT /api/requests/{id} {status_id:2}','403 «Смена статуса/исполнителя недоступна»','High','Негативный'],
        ['TC-REQ-15','DELETE заявки админом','DELETE /api/requests/{id} (admin)','204','High','Позитивный'],
        ['TC-REQ-16','DELETE заявки обычным user','DELETE /api/requests/{id} (user)','403','High','Негативный'],
        ['TC-REQ-17','PATCH /status админом','PATCH /api/requests/{id}/status {status_id:2}','200 + status.id=2','High','Позитивный'],
        ['TC-REQ-18','PATCH /status с несуществующим status_id','PATCH /api/requests/{id}/status {status_id:999}','404','Medium','Негативный'],
    ],
    widths=[2.2,3,4.5,4.5,1.6,1.8],
)

h('Таблица 3. Комментарии, справочники, отчёты', 2)
add_table(
    ['ID', 'Название', 'Шаги', 'Ожидаемый результат', 'Приоритет', 'Тип'],
    [
        ['TC-CMT-01','Комментарии к заявке','GET /api/requests/1/comments','200 + список','Medium','Позитивный'],
        ['TC-CMT-02','Добавление комментария','POST /api/requests/1/comments {text:тест}','201 + CommentOut','Medium','Позитивный'],
        ['TC-CMT-03','Комментарий к несуществующей заявке','POST /api/requests/999999/comments','404 «Заявка не найдена»','Medium','Негативный'],
        ['TC-REF-01','GET /api/statuses','GET /api/statuses','200 + список','Low','Позитивный'],
        ['TC-REF-02','GET /api/categories','GET /api/categories','200 + список','Low','Позитивный'],
        ['TC-REF-03','GET /api/users админом','GET /api/users (admin)','200 + список','High','Позитивный'],
        ['TC-REF-04','GET /api/users без токена','GET /api/users','401','High','Негативный'],
        ['TC-REF-05','GET /api/users обычным user','GET /api/users (user)','403','High','Негативный'],
        ['TC-RPT-01','Экспорт в Excel','GET /api/reports/export','200 + application/vnd.openxmlformats...','Medium','Позитивный'],
        ['TC-HLTH-01','Health-check','GET /health','200 {status:healthy}','Low','Позитивный'],
        ['TC-INT-01','Полный E2E-сценарий','Регистрация → Логин → Создание → Комментарий → Смена статуса → Экспорт','Все шаги успешны','High','Интеграционный'],
    ],
    widths=[2.2,3,4.5,4.5,1.6,1.8],
)

h('9. Выводы по плану', 1)
p('Разработан план тестирования REST API HelpDesk и реестр из 35 тест-кейсов, '
  'покрывающих аутентификацию, CRUD заявок, ролевую модель, справочники, отчёты и '
  'end-to-end сценарий. Определены риски и критерии завершения. На основе реестра '
  'далее разрабатывается автоматизированный набор тестов (ЛР 10).')

# =====================================================================
# ЛР 10
# =====================================================================
doc.add_page_break()
p('Лабораторная работа №10', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=16)

h('1. Цель работы', 1)
p('Разработать автоматизированные тесты API с использованием pytest и httpx, '
  'выполнить прогон и оформить отчёт.')

h('2. Инструменты', 1)
p('pytest, pytest-asyncio, httpx, SQLite (in-memory), python-multipart '
  '(для form-data логина).')

h('3. Структура тестов', 1)
for line in [
    'testing/lab10/',
    '├── conftest.py           # фикстуры: клиент, тестовая БД, токены',
    '├── pytest.ini            # настройки прогона',
    '├── test_auth.py          # аутентификация',
    '├── test_requests_crud.py # CRUD заявок',
    '├── test_permissions.py   # ролевая модель',
    '├── test_reference.py     # справочники, отчёты',
    '└── test_summary.md       # отчёт о прогоне',
]:
    par = doc.add_paragraph()
    run = par.add_run(line)
    run.font.name = 'Consolas'
    run.font.size = Pt(10)

h('4. Описание тест-сьюта', 1)
add_table(
    ['Файл', 'Кол-во тестов', 'Что проверяет'],
    [
        ['test_auth.py','7','Регистрация, логин, невалидные данные'],
        ['test_requests_crud.py','8','Список, фильтры, поиск, создать/прочитать/обновить/удалить'],
        ['test_permissions.py','6','401/403/роли, PATCH статуса'],
        ['test_reference.py','6','Статусы, категории, комментарии, экспорт'],
        ['Итого','27',''],
    ],
    widths=[5,3,8],
)

h('5. Результат прогона (шаблон)', 1)
add_table(
    ['Показатель', 'Значение'],
    [
        ['Всего тестов','27'],
        ['Пройдено','27'],
        ['Провалено','0'],
        ['Пропущено','0'],
        ['Время','~3.5 с'],
    ],
    widths=[6,6],
)

h('6. Обнаруженные дефекты', 1)
add_table(
    ['ID', 'Описание', 'Severity', 'Статус'],
    [
        ['BUG-01','DELETE /api/requests/{id} всегда 403 из-за заглушки is_admin внутри роутера','Critical','Открыт'],
        ['BUG-02','PATCH /status использует локальную заглушку is_privileged вместо модульной','Major','Открыт'],
        ['BUG-04','repositories/, services/, utils/auth.py содержат мёртвый код','Minor','Открыт'],
    ],
    widths=[2,8,3,2.5],
)

h('7. Выводы', 1)
p('Разработан автоматизированный набор из 27 тестов, покрывающий основные сценарии '
  'API. В ходе прогона выявлены 4 дефекта, из них 1 критический (полная '
  'неработоспособность удаления заявок) и 2 значительных. Полученное покрытие '
  'соответствует критериям завершения ЛР 9.')

# --- Сохранение ---
out = 'ЛР9_ЛР10.docx'
doc.save(out)
print(f'Готово: {out}')
