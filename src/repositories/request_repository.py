# repositories/request_repository.py

from h11 import Data
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional, Dict

from models import Request, RequestStatus, User, Category, Comment, UserRole


class RequestRepository:
    def __init__(self, db: Session):
        self.db = db
        """Создание новой заявки"""
        request = Request(**Data)
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)
        return request

    def get_request_by_id(self, request_id: int) -> Optional[Request]:
        """Получение заявки по ID"""
        return self.db.query(Request).filter(Request.id == request_id).first()

    def get_all_requests(self, filters: Optional[Dict] = None) -> List[Request]:
        """Получение всех заявок с фильтрацией"""
        query = self.db.query(Request)

        if filters:
            if filters.get("status"):
                query = query.filter(Request.status == filters["status"])
            if filters.get("category_id"):
                query = query.filter(Request.category_id == filters["category_id"])
            if filters.get("executor_id"):
                query = query.filter(Request.executor_id == filters["executor_id"])
            if filters.get("creator_id"):
                query = query.filter(Request.creator_id == filters["creator_id"])
            if filters.get("search"):
                search = f"%{filters['search']}%"
                query = query.filter(
                    or_(
                        Request.title.ilike(search),
                        Request.description.ilike(search),
                    )
                )
            if filters.get("priority"):
                query = query.filter(Request.priority == filters["priority"])

        return query.all()
        """Обновление заявки"""
        request = self.get_request_by_id(request_id)
        if request:
            for key, value in data.items():
                setattr(request, key, value)
            self.db.commit()
            self.db.refresh(request)
        return request

    def change_status(
        self, request_id: int, new_status: RequestStatus
    ) -> Optional[Request]:
        """Смена статуса заявки"""
        request = self.get_request_by_id(request_id)
        if request:
            request.status = new_status
            self.db.commit()
            self.db.refresh(request)
        return request

    def assign_executor(
        self, request_id: int, executor: User
    ) -> Optional[Request]:
        """Назначение исполнителя"""
        request = self.get_request_by_id(request_id)
        if request and executor.role == UserRole.EXECUTOR:
            request.executor_id = executor.id
            request.status = RequestStatus.IN_PROGRESS
            self.db.commit()
            self.db.refresh(request)
        return request

    def delete_request(self, request_id: int) -> bool:
        """Удаление заявки"""
        request = self.get_request_by_id(request_id)
        if request:
            self.db.delete(request)
            self.db.commit()
            return True
        return False

    def add_comment(self, request_id: int, user_id: int, text: str) -> Comment:
        """Добавление комментария"""
        comment = Comment(
            request_id=request_id,
            user_id=user_id,
            text=text,
        )
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_requests_by_category(self, category_id: int) -> List[Request]:
        """Получение заявок по категории"""
        return self.db.query(Request).filter(Request.category_id == category_id).all()

    def get_requests_by_executor(self, executor_id: int) -> List[Request]:
        """Получение заявок по исполнителю"""
        return self.db.query(Request).filter(Request.executor_id == executor_id).all()
