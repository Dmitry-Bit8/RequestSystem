from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src import schemas
from src import models
from src.database import get_db
from src.models import User
from src.schemas import UserOut
from src.security import require_role

router = APIRouter(prefix="/api/users", tags=["Пользователи"])

@router.get("", response_model=list[schemas.UserOut])
def list_users(
    db: Session = Depends(get_db),
    _: models.User = Depends(require_role("admin")),
):
    return db.query(models.User).all()

