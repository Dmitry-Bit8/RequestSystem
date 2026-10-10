from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import Category
from src.schemas import CategoryOut

router = APIRouter(prefix="/api/categories", tags=["Категории"])

@router.get("", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    """Список всех категорий"""
    return db.query(Category).all()
