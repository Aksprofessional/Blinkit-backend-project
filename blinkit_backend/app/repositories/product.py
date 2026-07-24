from uuid import UUID
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from typing import Optional 

from app.models.products import Products
from app.schemas.products import ProductCreate, ProductUpdate


def create_product(db: Session, product_data: ProductCreate):

    existing_product = db.query(Products).filter(
        Products.name == product_data.name
    ).first()

    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already exists"
        )

    product = Products(**product_data.model_dump())

    db.add(product)
    db.commit()
    db.refresh(product)

    return product





def get_product_by_id(
    db: Session,
    product_id: UUID
):

    product = db.get(
        Products,
        product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product







def get_all_products(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
):
    query = db.query(Products)

    if search:
        query = query.filter(
            Products.name.ilike(f"%{search}%")
        )

    total = query.count()

    products = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "data": products,
    }







def update_product(
    db: Session,
    product_id: UUID,
    product_data: ProductUpdate
):
    product = get_product_by_id(
        db,
        product_id
    )

    update_data = product_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            product,
            key,
            value
        )

    db.commit()
    db.refresh(product)

    return product








def delete_product(
    db: Session,
    product_id: UUID
):
    product = get_product_by_id(
        db,
        product_id
    )

    product.isdeleted = True
    product.delete_timestamp = datetime.now(timezone.utc) 

    db.commit()

    return {
        "message": "Product deleted successfully"
    }