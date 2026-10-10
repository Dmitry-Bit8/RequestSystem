from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO
from openpyxl import Workbook # type: ignore
from src.database import get_db
from src.models import Request

router = APIRouter(prefix="/api/reports", tags=["Отчёты"])

@router.get("/export")
def export_requests_xlsx(db: Session = Depends(get_db)):
    """Экспорт всех заявок в Excel"""
    requests = db.query(Request).all()

    # Создаём Excel файл
    wb = Workbook()
    ws = wb.active
    assert ws is not None
    ws.title = "Заявки"

    # Заголовки
    headers = ["ID", "Номер", "Название", "Описание", "Приоритет", "Дата создания"]
    ws.append(headers)

    # Данные
    for req in requests:
        ws.append([
            req.id,
            req.number,
            req.title,
            req.description,
            req.priority,
            req.created_at.strftime("%Y-%m-%d %H:%M")
        ])

    # Сохраняем в память
    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)

    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=requests.xlsx"}
    )
