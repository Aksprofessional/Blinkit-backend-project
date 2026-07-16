from sqlalchemy.orm import Session
from app.models.category import Category
from uuid import UUID
from fastapi import HTTPException,status
from app.schemas.category import CategoryCreate
from app.models.category import Category

def get_category_by_id(db: Session, category_id: UUID):
    category=db.get(Category,category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category

def add_category(db: Session, category_data: CategoryCreate):
    try:
        db_category=Category(**category_data.model_dump())
        db.add(db_category)
        db.commit()
        return db_category
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Category could not be created.{e}"
        )
        


def get_category_by_name(db: Session, category_name: str):
    category=db.get(Category,category_name)
    if category:
        return False
    return True