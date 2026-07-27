from sqlalchemy.orm import Session,joinedload
from app.models.category import Category
from uuid import UUID
from fastapi import HTTPException,status
from app.schemas.category import CategoryCreate
from typing import Optional
from sqlalchemy.orm import selectinload
from app.models.collection import Collection
from app.models.collection_subcategory import CollectionSubCategory
from app.models.sub_category import SubCategory


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
        db.refresh(db_category)
        return db_category
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create category."
        )
        


def get_category_by_name(db: Session, category_name: str):
    category=db.query(Category).filter(
        Category.name == category_name
    ).first()
    return category









def get_all_categories(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
):
    query = db.query(Category)

    if search:
        query = query.filter(
            Category.name.ilike(f"%{search}%")
        )

    return (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )







def update_category(
    db: Session,
    category: Category,
):
    db.commit()
    db.refresh(category)
    return category


#soft delete-Blinkit would rarely permanently delete categories because products may still reference them.
def delete_category(
    db: Session,
    category: Category,
):
    category.is_active = False
    db.commit()
    db.refresh(category)
    return category






def get_all_categories_user(db: Session):

    return (
        db.query(Category)
        .options(
            joinedload(Category.sub_categories)
        )
        .filter(
            Category.is_active.is_(True)
        )
        .all()
    )

