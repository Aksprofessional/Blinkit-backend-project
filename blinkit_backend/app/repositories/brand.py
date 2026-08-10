from uuid import UUID
from fastapi import HTTPException, status,UploadFile
from sqlalchemy.orm import Session
from app.models.brand import brand
from app.schemas.brand import BrandCreate, BrandUpdate
from typing import Optional
from app.services.image_sevice import upload_image,destroy_image
from app.exceptions.custom_exception import NotFoundException, InternalServerException, BadRequestException

from app.core.logger import logger

def get_brand_by_id(db: Session, brand_id: UUID):
    db_brand = db.get(brand, brand_id)

    if db_brand is None:
        raise NotFoundException(
            "Brand not found"
        )

    return db_brand


def get_brand_by_name(db: Session, brand_name: str):
    return db.query(brand).filter(
        brand.name == brand_name
    ).first()





#added limit offset pagination for admin apis and search functionality also
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
    brand_data: BrandCreate,
    logo: UploadFile
):
    db_brand = brand(**brand_data.model_dump())
    image_url=upload_image(logo,brand.__tablename__)
    db_brand.logo=image_url.get("url")
    db_brand.image_public_id=image_url.get("public_id")
    try:
        db.add(db_brand)
        db.commit()
        db.refresh(db_brand)

    except Exception:
        db.rollback()

        raise InternalServerException(
            "Failed to create brand."
        )

    return db_brand


def update_brand(
    db: Session,
    db_brand: brand,
    brand_data: BrandUpdate,
    logo : UploadFile | None
):
    update_data = brand_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    if not update_data and logo is None:
        raise BadRequestException(
            "No fields provided for update."
        )

    for key, value in update_data.items():
        setattr(
            db_brand,
            key,
            value
        )

    try:
        if logo is not None:
            # Upload the new logo and update the stored image details.
            image_url = upload_image(
                logo,
                brand.__tablename__,
            )

            db_brand.logo = image_url["url"]

            public_id_old = db_brand.image_public_id

            db_brand.image_public_id = image_url["public_id"]

            db.commit()

            db.refresh(db_brand)

            try:
                destroy_image(public_id_old)
            except Exception:
                logger.exception(
                    "Failed to delete old brand image."
                )
        else:

            db.commit()

            db.refresh(db_brand)

    except Exception:

        db.rollback()

        raise InternalServerException(
            "Failed to update brand."
        )

    return db_brand


def delete_brand(
    db: Session,
    db_brand: brand
):
    db_brand.is_active = False

    try:

        db.commit()

    except Exception:
        # Roll back the transaction if database update fails.
        db.rollback()

        raise InternalServerException(
            "Failed to delete brand."
        )

    return {
        "message":"Brand deleted successfully."
    }