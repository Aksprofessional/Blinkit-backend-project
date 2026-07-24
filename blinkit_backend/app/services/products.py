from fastapi import HTTPException, status
from app.models.product_variant import product_variant
from uuid import UUID
from app.repositories.product_variant import get_product_variant
from sqlalchemy.orm import Session




def check_product_variant_exist(db: Session, product_variant_id: UUID):
    product_variant=get_product_variant(db,product_variant_id)
    if product_variant is None:
        raise HTTPException(
                     status_code=status.HTTP_404_NOT_FOUND,
                     detail="product not found"
                )
    return product_variant

