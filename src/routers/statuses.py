from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import Status
from src.schemas import StatusOut

router = APIRouter(prefix="/api/statuses", tags=["Статусы"])

@router.get("", response_model=list[StatusOut])
def list_statuses(db: Session = Depends(get_db)):
    """Список всех статусов"""
    return db.query(Status).all()
