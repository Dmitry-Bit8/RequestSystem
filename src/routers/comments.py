from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import Comment, Request
from src.schemas import CommentCreate, CommentOut

router = APIRouter(prefix="/api/requests/{request_id}/comments", tags=["Комментарии"])

@router.get("", response_model=list[CommentOut])
def list_comments(request_id: int, db: Session = Depends(get_db)):
    """Список комментариев к заявке"""
    return db.query(Comment).filter(Comment.request_id == request_id).all()

@router.post("", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(request_id: int, data: CommentCreate, db: Session = Depends(get_db)):
    """Добавить комментарий к заявке"""
    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    comment = Comment(
        request_id=request_id,
        user_id=1,  # TODO: вытащить из токена
        text=data.text
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
