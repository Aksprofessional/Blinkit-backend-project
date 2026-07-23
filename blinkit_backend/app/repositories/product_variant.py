from sqlalchemy.orm import Session
from app.models.category import Category
from uuid import UUID
from fastapi import HTTPException,status
from app.models.product_variant import product_variant
from app.models.products import Products

def get_product_variant(db: Session, product_variant_id: UUID):
    product=db.query(product_variant).join(Products).filter(product_variant.id==product_variant_id,product_variant.isdeleted==False,Products.isdeleted==False).first()
    return product

