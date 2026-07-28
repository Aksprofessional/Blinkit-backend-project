from uuid import UUID
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.main_category import MainCategory
from app.schemas.main_category import (
    MainCategoryCreate,
    MainCategoryUpdate,
)


def get_main_category_by_id(
    db: Session,
    main_category_id: UUID,
):
    db_main_category = db.get(
        MainCategory,
        main_category_id,
    )

    if db_main_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Main category not found",
        )

    return db_main_category


def get_main_category_by_name(
    db: Session,
    name: str,
):
    return (
        db.query(MainCategory)
        .filter(MainCategory.name == name)
        .first()
    )


def get_all_main_categories(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
):
    query = db.query(MainCategory)

    if search:
        query = query.filter(
            MainCategory.name.ilike(
                f"%{search}%"
            )
        )

    total = query.count()

    main_categories = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "data": main_categories,
    }


def create_main_category(
    db: Session,
    main_category_data: MainCategoryCreate,
):
    db_main_category = MainCategory(
        **main_category_data.model_dump()
    )

    db.add(db_main_category)
    db.commit()
    db.refresh(db_main_category)

    return db_main_category


def update_main_category(
    db: Session,
    db_main_category: MainCategory,
    main_category_data: MainCategoryUpdate,
):
    update_data = main_category_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update.",
        )

    for key, value in update_data.items():
        setattr(
            db_main_category,
            key,
            value,
        )

    db.commit()
    db.refresh(db_main_category)

    return db_main_category


def delete_main_category(
    db: Session,
    db_main_category: MainCategory,
):
    db_main_category.is_active = False

    db.commit()

    return {
        "message": "Main category deleted successfully."
    }