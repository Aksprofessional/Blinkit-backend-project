from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.brand import brand
from app.schemas.brand import BrandCreate, BrandUpdate
from typing import Optional


def get_brand_by_id(db: Session, brand_id: UUID):
    db_brand = db.get(brand, brand_id)

    if db_brand is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found"
        )

    return db_brand


def get_brand_by_name(db: Session, brand_name: str):
    return db.query(brand).filter(
        brand.name == brand_name
    ).first()






def get_all_brands(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
):
    query = db.query(brand)

    if search:
        query = query.filter(
            brand.name.ilike(f"%{search}%")
        )

    total = query.count()

    brands = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "data": brands,
    }








def create_brand(
    db: Session,
    brand_data: BrandCreate
):
    db_brand = brand(**brand_data.model_dump())

    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)

    return db_brand


def update_brand(
    db: Session,
    db_brand: brand,
    brand_data: BrandUpdate
):
    update_data = brand_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update."
        )

    for key, value in update_data.items():
        setattr(
            db_brand,
            key,
            value
        )

    db.commit()
    db.refresh(db_brand)

    return db_brand


def delete_brand(
    db: Session,
    db_brand: brand
):
    db_brand.is_active = False

    db.commit()

    return {
        "message": "Brand deleted successfully."
    }