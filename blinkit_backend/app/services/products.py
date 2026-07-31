from fastapi import HTTPException, status
from uuid import UUID
from app.repositories.product_variant import get_product_variant
from sqlalchemy.orm import Session
from app.repositories.product import suggestion_search_product_customer
from fastapi import HTTPException
from app.utils.cursor import encode_cursor,decode_cursor
from app.repositories.product import get_product_by_id
from app.schemas.product_variant import ProductDetailResponse,ProductVariantResponse




# Verify that a product variant exists
def check_product_variant_exist(db: Session, product_variant_id: UUID):

    # Retrieve the product variant
    product_variant=get_product_variant(db,product_variant_id)

    # Raise an exception if the product variant does not exist
    if product_variant is None:
        raise HTTPException(
                     status_code=status.HTTP_404_NOT_FOUND,
                     detail="product not found"
                )
    return product_variant



# Search for products matching the provided search term
def suggestion_search_product_details(db: Session, search_param: str):

    # Delegate the search to the repository layer
    return suggestion_search_product_customer(db,search_param)



from app.repositories.product import (
    get_products_by_subcategory,
)

from app.schemas.products import (
    ProductListResponse,
    ProductResponse,
    ProductVariantResponseFor,
)


# Retrieve all products belonging to a subcategory
def get_products_service(
    db,
    subcategory_id,
    limit: int,
    cursor: str | None,
):

    cursor_created_at = None
    cursor_id = None

    if cursor:
        cursor_created_at, cursor_id = decode_cursor(cursor)

    products = get_products_by_subcategory(
        db=db,
        subcategory_id=subcategory_id,
        limit=limit,
        cursor_created_at=cursor_created_at,
        cursor_id=cursor_id,
    )

    has_next = len(products) > limit

    if has_next:
        products = products[:limit]

    next_cursor = None

    if has_next:
        last_product = products[-1]

        next_cursor = encode_cursor(
            created_at=last_product.created_at,
            cursor_id=last_product.id,
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
        ],
        next_cursor=next_cursor,
        has_next=has_next,
    )


# Retrieve detailed information for a specific product
def get_product_by_id_service(
    db,
    product_id,
):

    # Fetch the requested product
    product = get_product_by_id(
        db,
        product_id,
    )

    # Raise an exception if the product does not exist
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )

    # Include only active product variants
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

    # Raise an exception if no active variants are available
    if not variants:
        raise HTTPException(
            status_code=404,
            detail="Product not available.",
        )

    # Return the product details
    return ProductDetailResponse(
        id=product.id,
        name=product.name,
        image=product.image,
        description=product.description,
        variants=variants,
    )