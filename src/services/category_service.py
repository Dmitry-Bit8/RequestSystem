from typing import List, Optional
from models import Category, Request


class CategoryService:
    def __init__(self, db):
        self.db = db

    def create_category(self, name: str, description: Optional[str] = None) -> Category:
        """Создание новой категории"""
        # Проверка на дубликаты
        if self.get_category_by_name(name):
            raise ValueError(f"Категория '{name}' уже существует")

        category = Category(name=name, description=description)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def get_category_by_name(self, name: str) -> Optional[Category]:
        """Получение категории по имени"""
        return self.db.query(Category).filter(Category.name == name).first()

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Получение категории по ID"""
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_all_categories(self) -> List[Category]:
        """Получение всех категорий"""
        return self.db.query(Category).all()

    def update_category(self, category_id: int, **kwargs) -> Optional[Category]:
        """Обновление категории"""
        category = self.get_category_by_id(category_id)
        if category:
            for key, value in kwargs.items():
                setattr(category, key, value)
            self.db.commit()
            self.db.refresh(category)
        return category

    def delete_category(self, category_id: int) -> bool:
        """Удаление категории"""
        category = self.get_category_by_id(category_id)
        if category:
            # Проверка на связанные заявки
            if category.requests:
                raise ValueError("Невозможно удалить категорию с заявками")

            self.db.delete(category)
            self.db.commit()
            return True
        return False

    def get_category_statistics(self) -> List[dict]:
        """Статистика по категориям"""
        from sqlalchemy import func

        results = self.db.query(
            Category.name,
            Category.id,
            func.count(Request.id).label('request_count')
        ).join(Request, Request.category_id == Category.id, isouter=True).group_by(Category.id).all()

        return [
            {'id': r.id, 'name': r.name, 'requests': r.request_count}
            for r in results
        ]
