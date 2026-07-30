from uuid import UUID
from datetime import datetime, timezone
from fastapi import HTTPException, status,UploadFile
from sqlalchemy.orm import Session,joinedload
from typing import Optional 
from app.models.product_variant import product_variant
from app.models.products import Products
from app.models.product_tag import ProductTag
from app.models.tag import Tag
from app.schemas.products import ProductCreate, ProductUpdate
from app.services.image_sevice import upload_image,destroy_image



def create_product(db: Session, product_data: ProductCreate, image: UploadFile):

    existing_product = db.query(Products).filter(
        Products.name == product_data.name
    ).first()

    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already exists"
        )

    image_url=upload_image(image,Products.__tablename__)


    
    

    product = Products(
        name=product_data.name,
        image= image_url.get("url"),
        description= product_data.description,
        brand_id= product_data.brand_id,
        sub_category_id= product_data.sub_category_id,
        image_public_id=image_url.get("public_id")

    )

    db.add(product)
    db.flush()

    for tag_id in product_data.tag_ids:

        tag = db.get(
            Tag,
            tag_id,
        )

        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag {tag_id} not found",
            )

        db.add(
            ProductTag(
                product_id=product.id,
                tag_id=tag_id,
            )
        )

    db.commit()
    db.refresh(product)

    return product




def get_product_by_id(
    db: Session,
    product_id: UUID
):

    product = (
    db.query(Products)
    .filter(
        Products.id == product_id,
        Products.isdeleted.is_(False),
    )
    .first()
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
    product_data: ProductUpdate,
    image: UploadFile | None,
):
    product = get_product_by_id(
        db,
        product_id,
    )

    update_data = product_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    tag_ids = update_data.pop(
        "tag_ids",
        None,
    )

    for key, value in update_data.items():
        setattr(
            product,
            key,
            value,
        )

    if tag_ids is not None:

        db.query(ProductTag).filter(
            ProductTag.product_id == product.id
        ).delete(
            synchronize_session=False
        )

        for tag_id in tag_ids:

            tag = db.get(
                Tag,
                tag_id,
            )

            if not tag:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tag {tag_id} not found",
                )

            db.add(
                ProductTag(
                    product_id=product.id,
                    tag_id=tag_id,
                )
            )

    if image is not None:
        image_url = upload_image(
            image,
            Products.__tablename__,
        )

        product.image = image_url.get("url")

        old_public_id = product.image_public_id

        product.image_public_id = image_url.get("public_id")

        db.commit()
        db.refresh(product)

        destroy_image(old_public_id)

    else:
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


def suggestion_search_product_customer(db: Session, search_param: str):
    products= db.query(Products).options(joinedload(Products.product_variants)).filter(Products.name.ilike(f"%{search_param}%"),Products.isdeleted == False, product_variant.isdeleted==False).all()
    return products








def get_products_by_subcategory(
    db: Session,
    subcategory_id,
):

    return (
        db.query(Products)
        .options(
            joinedload(Products.product_variants)
        )
        .filter(
            Products.sub_category_id == subcategory_id,
            Products.isdeleted.is_(False),
        )
        .all()
    )