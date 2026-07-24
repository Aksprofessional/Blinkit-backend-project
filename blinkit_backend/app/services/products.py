from fastapi import HTTPException, status
from app.models.product_variant import product_variant
from uuid import UUID
from app.repositories.product_variant import get_product_variant
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.product import suggestion_search_product_customer



def check_product_variant_exist(db: Session, product_variant_id: UUID):
    product_variant=get_product_variant(db,product_variant_id)
    if product_variant is None:
        raise HTTPException(
                     status_code=status.HTTP_404_NOT_FOUND,
                     detail="product not found"
                )
    return product_variant



def suggestion_search_product_details(db: Session, search_param: str):
    return suggestion_search_product_customer(db,search_param)



from app.repositories.product import (
    get_products_by_subcategory,
)

from app.schemas.products import (
    ProductListResponse,
    ProductResponse,
    ProductVariantResponseFor,
)


def get_products_service(
    db,
    subcategory_id,
):

    products = get_products_by_subcategory(
        db,
        subcategory_id,
    )

    return ProductListResponse(
        products=[
            ProductResponse(
                id=product.id,
                name=product.name,
                image=product.image,
                description=product.description,
                variants=[
                    ProductVariantResponseFor(
                        id=variant.id,
                        variant_name=variant.variant_name,
                        price=variant.price,
                    )
                    for variant in product.product_variants
                    if not variant.isdeleted
                ],
            )
            for product in products
        ]
    )


from fastapi import HTTPException

from app.repositories.product import get_product_by_id
from app.schemas.product_variant import (
    ProductDetailResponse,
    ProductVariantResponse,
)


def get_product_by_id_service(
    db,
    product_id,
):

    product = get_product_by_id(
        db,
        product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )

    variants = [
        ProductVariantResponse(
            id=variant.id,
            variant_name=variant.variant_name,
            price=variant.price,
            stock_quantity=variant.stock_quantity,
        )
        for variant in product.product_variants
        if not variant.isdeleted
    ]

    if not variants:
        raise HTTPException(
            status_code=404,
            detail="Product not available.",
        )

    return ProductDetailResponse(
        id=product.id,
        name=product.name,
        image=product.image,
        description=product.description,
        variants=variants,
    )