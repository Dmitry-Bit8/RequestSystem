from datetime import datetime, timedelta
from typing import Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload

from src import models, schemas
from src.database import get_db
from src.models import Request, Status, Category, User
from src.schemas import RequestCreate, RequestUpdate, RequestOut
from src.security import get_current_user
from typing import cast
router = APIRouter(prefix="/api/requests", tags=["Заявки"])



class StatusChange(BaseModel):
    status_id: int


def generate_number() -> str:
    """Уникальный номер заявки. Не random.randint(1000, 9999)."""
    return f"REQ-{datetime.utcnow():%Y%m%d}-{uuid.uuid4().hex[:6].upper()}"


def _with_relations(query):
    """Подтягивает связи одним запросом — иначе N+1 и ленивые падения в response_model."""
    return query.options(
        joinedload(Request.category),
        joinedload(Request.status),
        joinedload(Request.requester),
        joinedload(Request.assignee),
    )


def _get_or_404(db: Session, request_id: int) -> Request:
    request = (
        _with_relations(db.query(Request))
        .filter(Request.id == request_id)
        .first()
    )
    if not request:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return request


def _is_privileged(user: User) -> bool:
    return user.role in ("admin", "executor")


@router.get("", response_model=list[RequestOut])
def list_requests(
    status_id: Optional[int] = None,
    category_id: Optional[int] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Список заявок с фильтрацией."""
    query = db.query(Request)

    if status_id is not None:
        query = query.filter(Request.status_id == status_id)
    if category_id is not None:
        query = query.filter(Request.category_id == category_id)
    if priority:
        query = query.filter(Request.priority == priority)
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            Request.title.ilike(pattern)
            | Request.description.ilike(pattern)
            | Request.number.ilike(pattern)
        )

    return (
        _with_relations(query)
        .order_by(Request.created_at.desc())
        .all()
    )

@router.get("/{request_id}", response_model=RequestOut)
def get_request(request_id: int, db: Session = Depends(get_db)):
    """Получить заявку по ID."""
    return _get_or_404(db, request_id)

@router.post("", response_model=RequestOut, status_code=status.HTTP_201_CREATED)
def create_request(
    data, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Создать заявку. Автор — текущий пользователь."""
    
    category = db.get(Category, data.category_id)
    if not category:
        raise HTTPException(status_code=400, detail="Категория не найдена")

    
    new_status = db.query(Status).filter(Status.code == "new").first()
    if not new_status:
        new_status = Status(code="new", name="Новая")
        db.add(new_status)
        db.flush()

  
    sla_hours = getattr(category, "sla_hours", None) or 24

    request = Request(
        number=generate_number(),
        title=data.title,
        description=data.description,
        category_id=data.category_id,
        status_id=new_status.id,
        priority=getattr(data, "priority", None) or "medium",
        requester_id=current_user.id,
        due_date=datetime.utcnow() + timedelta(hours=sla_hours),
    )

    db.add(request)
    db.commit()
    db.refresh(request)
    return request



@router.put("/{request_id}", response_model=RequestOut)
def update_request(
    request_id: int, data,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Полное обновление заявки."""
    request = _get_or_404(db, request_id)

    is_priv = _is_privileged(current_user)
    requester_id = cast(int, request.requester_id)

    if not is_priv and requester_id != current_user.id:
        raise HTTPException(status_code=403, detail="Можно править только свои заявки")

    data_dict = data.model_dump(exclude_unset=True)

    forbidden = {"status_id", "assignee_id"} & set(data_dict.keys())
    if not is_priv and forbidden:
        raise HTTPException(
            status_code=403,
            detail="Смена статуса/исполнителя недоступна",
        )

    if (cid := data_dict.get("category_id")) is not None and not db.get(Category, cid):
        raise HTTPException(status_code=400, detail="Категория не найдена")
    if (sid := data_dict.get("status_id")) is not None and not db.get(Status, sid):
        raise HTTPException(status_code=400, detail="Статус не найден")
    if (aid := data_dict.get("assignee_id")) is not None and not db.get(User, aid):
        raise HTTPException(status_code=400, detail="Исполнитель не найден")

    for field, value in data_dict.items():
        setattr(request, field, value)

    db.commit()
    db.refresh(request)
    return request


@router.patch("/{request_id}", response_model=RequestOut)
def patch_request(
    request_id: int, data,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Частичное обновление заявки."""
    request = _get_or_404(db, request_id)

    is_priv = _is_privileged(current_user)
    requester_id = cast(int, request.requester_id)

    if not is_priv and requester_id != current_user.id:
        raise HTTPException(status_code=403, detail="Можно править только свои заявки")

    data_dict = data.model_dump(exclude_unset=True)

    forbidden = {"status_id", "assignee_id"} & set(data_dict.keys())
    if not is_priv and forbidden:
        raise HTTPException(
            status_code=403,
            detail="Смена статуса/исполнителя недоступна",
        )

    if (cid := data_dict.get("category_id")) is not None and not db.get(Category, cid):
        raise HTTPException(status_code=400, detail="Категория не найдена")
    if (sid := data_dict.get("status_id")) is not None and not db.get(Status, sid):
        raise HTTPException(status_code=400, detail="Статус не найден")
    if (aid := data_dict.get("assignee_id")) is not None and not db.get(User, aid):
        raise HTTPException(status_code=400, detail="Исполнитель не найден")

    for field, value in data_dict.items():
        setattr(request, field, value)

    db.commit()
    db.refresh(request)
    return request




@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Удалить заявку. Только админ."""
    request = _get_or_404(db, request_id)

    def is_admin(current_user):
        ...

    if not is_admin(current_user):
        raise HTTPException(
            status_code=403,
            detail="Удалять заявку может только админ",
        )

    db.delete(request)
    db.commit()
    return None




@router.patch("/{request_id}/status", response_model=RequestOut)
def change_status(
    request_id: int,
    payload: StatusChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Сменить статус заявки."""
    request = _get_or_404(db, request_id)

    def is_privileged(current_user):
        ...

    is_priv = is_privileged(current_user)
    requester_id = cast(int, request.requester_id)

    if not is_priv and requester_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Смена статуса недоступна",
        )

    status_obj = db.get(Status, payload.status_id)
    if not status_obj:
        raise HTTPException(status_code=404, detail="Статус не найден")

    request.status_id = status_obj.id

    db.commit()
    db.refresh(request)
    return request
