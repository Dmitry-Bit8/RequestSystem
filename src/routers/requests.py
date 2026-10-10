from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import random
from src import schemas
from src import models
from src.database import get_db
from src.models import Request, Status, Category
from src.schemas import RequestCreate, RequestUpdate, RequestOut
from src.security import get_current_user

router = APIRouter(prefix="/api/requests", tags=["Заявки"])

def generate_number() -> str:
    """Генерация уникального номера заявки"""
    return f"REQ-{random.randint(1000, 9999)}"

@router.get("", response_model=list[RequestOut])
def list_requests(
    status_id: Optional[int] = None,
    category_id: Optional[int] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Список заявок с фильтрацией"""
    query = db.query(Request)

    if status_id:
        query = query.filter(Request.status_id == status_id)
    if category_id:
        query = query.filter(Request.category_id == category_id)
    if priority:
        query = query.filter(Request.priority == priority)
    if search:
        query = query.filter(
            (Request.title.contains(search)) |
            (Request.description.contains(search)) |
            (Request.number.contains(search))
        )

    return query.order_by(Request.created_at.desc()).all()

@router.get("/{request_id}", response_model=RequestOut)
def get_request(request_id: int, db: Session = Depends(get_db)):
    """Получить заявку по ID"""
    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return request

@router.post("", response_model=schemas.RequestOut, status_code=201)
def create_request(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # ... вместо author_id=data.author_id ставим:
    new_request = models.Request(
        ...,
        author_id=current_user.id,
    )

    # Получаем статус "новая"
    new_status = db.query(Status).filter(Status.code == "new").first()
    if not new_status:
        new_status = Status(code="new", name="Новая")
        db.add(new_status)
        db.flush()

    # Создаём заявку
    class data:
        description = None
        title = None
        category_id = None

    request = Request(
        number=generate_number(),
        title=data.title,
        description=data.description,
        category_id=data.category_id,
        status_id=new_status.id,
        priority="medium",
        requester_id=1  # TODO: вытащить из токена
    )

    db.add(request)
    db.commit()
    db.refresh(request)
    return request

@router.put("/{request_id}", response_model=RequestOut)
def update_request(request_id: int, data: RequestUpdate, db: Session = Depends(get_db)):
    """Обновить заявку"""
    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(request, field, value)

    db.commit()
    db.refresh(request)
    return request

@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_request(request_id: int, db: Session = Depends(get_db)):
    """Удалить заявку"""
    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    db.delete(request)
    db.commit()

@router.patch("/{request_id}/status", response_model=RequestOut)
def change_status(request_id: int, status_id: int, db: Session = Depends(get_db)):
    """Сменить статус заявки"""
    request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    status_obj = db.query(models.Status).filter(models.Status.id == status_id).first()
    if not status_obj:
        raise HTTPException(status_code=404, detail="Статус не найден")

    request.status_id = status_id  # type: ignore

    db.commit()
    db.refresh(request)
    return request


