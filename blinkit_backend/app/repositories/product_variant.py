from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from typing import Optional

from app.models.product_variant import product_variant
from app.schemas.product_variant import (
    ProductVariantCreate,
    ProductVariantUpdate,
)


def create_product_variant(
    db: Session,
    variant: ProductVariantCreate,
):
    db_variant = product_variant(
        **variant.model_dump()
    )

    db.add(db_variant)
    db.commit()
    db.refresh(db_variant)

    return db_variant


def get_product_variant_by_id(
    db: Session,
    variant_id: UUID,
):
    variant = db.get(
        product_variant,
        variant_id
    )

    if not variant or variant.isdeleted:
        raise HTTPException(
            status_code=404,
            detail="Variant not found"
        )

    return variant







def get_all_product_variants(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
):
    query = db.query(product_variant)

    if search:
        query = query.filter(
            product_variant.variant_name.ilike(f"%{search}%")
        )

    total = query.count()

    variants = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "data": variants,
    }



def update_product_variant(
    db: Session,
    variant_id: UUID,
    variant: ProductVariantUpdate,
):
    db_variant = get_product_variant_by_id(
        db,
        variant_id
    )

    update_data = variant.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            db_variant,
            key,
            value
        )

    db.commit()
    db.refresh(db_variant)

    return db_variant







def delete_product_variant(
    db: Session,
    variant_id: UUID,
):
    db_variant = get_product_variant_by_id(
        db,
        variant_id
    )

    #we are soft deleting it just in case well need this row later on say its connected to any other db row so didnt hard delete.Also storing the tym we deleted it so that we can get it later 
    db_variant.isdeleted = True
    db_variant.delete_timestamp = datetime.now(
        timezone.utc
    )

    db.commit()

    return {
        "message": "Variant deleted successfully"
    }