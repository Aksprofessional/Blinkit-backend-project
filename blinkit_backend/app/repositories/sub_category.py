from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from typing import Optional

from app.models.sub_category import SubCategory
from app.schemas.sub_category import (
    SubCategoryCreate,
    SubCategoryUpdate
)


def create_subcategory(
    db: Session,
    subcategory_data: SubCategoryCreate
):

    existing = db.query(SubCategory).filter(
        SubCategory.name == subcategory_data.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="SubCategory already exists"
        )

    subcategory = SubCategory(
        **subcategory_data.model_dump()
    )

    db.add(subcategory)
    db.commit()
    db.refresh(subcategory)

    return subcategory






def get_all_subcategories(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
):
    query = db.query(SubCategory)

    if search:
        query = query.filter(
            SubCategory.name.ilike(f"%{search}%")
        )

    total = query.count()

    subcategories = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "data": subcategories,
    }



def get_subcategory_by_id(
    db: Session,
    subcategory_id: UUID
):

    subcategory = db.get(
        SubCategory,
        subcategory_id
    )

    if subcategory is None:
        raise HTTPException(
            status_code=404,
            detail="SubCategory not found"
        )

    return subcategory




def update_subcategory(
    db: Session,
    subcategory_id: UUID,
    subcategory_data: SubCategoryUpdate
):

    subcategory = get_subcategory_by_id(
        db,
        subcategory_id
    )

    update_data = subcategory_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            subcategory,
            key,
            value
        )

    db.commit()
    db.refresh(subcategory)

    return subcategory





def delete_subcategory(
    db: Session,
    subcategory_id: UUID
):

    subcategory = get_subcategory_by_id(
        db,
        subcategory_id
    )

    subcategory.is_active = False

    db.commit()

    return {
        "message":"SubCategory deleted successfully"
    }