from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product_tag import ProductTag
from app.models.products import Products
from app.models.tag import Tag
from app.schemas.product_tag import ProductTagCreate

from app.exceptions.custom_exception import NotFoundException, InternalServerException

from app.core.logger import logger

def add_product_tag(
    db: Session,
    product_tag: ProductTagCreate,
):
    product = db.get(
        Products,
        product_tag.product_id,
    )

    if product is None:
        raise NotFoundException(
                    "Product not found"
                )

    tag = db.get(
        Tag,
        product_tag.tag_id,
    )

    if tag is None:
        raise NotFoundException(
                    "Tag not found"
                )

    existing = db.query(ProductTag).filter(
        ProductTag.product_id == product_tag.product_id,
        ProductTag.tag_id == product_tag.tag_id,
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag already assigned to product.",
        )

    db_product_tag = ProductTag(
        **product_tag.model_dump()
    )

    try:
        db.add(db_product_tag)
        db.commit()
        db.refresh(db_product_tag)

    except Exception:
        db.rollback()

        raise InternalServerException(
            "Failed to create product tag."
        )

    return db_product_tag


def get_product_tags(
    db: Session,
):
    return db.query(ProductTag).all()


def delete_product_tag(
    db: Session,
    mapping_id: UUID,
):
    db_mapping = db.get(
        ProductTag,
        mapping_id,
    )

    if db_mapping is None:
        raise NotFoundException(
                    "Mapping not found"
                )

    db.delete(db_mapping)

    try:
        db.commit()

    except Exception:
        db.rollback()

        raise InternalServerException(
            "Failed to delete product tag."
        )

    return {
        "message": "Product tag deleted successfully."
    }