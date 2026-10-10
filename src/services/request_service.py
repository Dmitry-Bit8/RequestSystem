from sqlalchemy.orm import Session
from sqlalchemy import select
from src.models import Request
from src.schemas import RequestCreate, RequestUpdate

def get_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(Request).offset(skip).limit(limit)).all()

def get_request_by_id(db: Session, request_id: int) -> Request | None:
    return db.get(Request, request_id)
    db_request = Request(
        title=request_data.title,
        description=request_data.description,
        author_id=author_id,
        status="new"
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request
    if data.title is not None:
        request.title = data.title
    if data.description is not None:
        request.description = data.description
    if data.status is not None:
        request.status = data.status
    db.commit()
    db.refresh(request)
    return request

def delete_request(db: Session, request: Request):
    db.delete(request)
    db.commit()
