from fastapi import APIRouter,Depends,Query,Body
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.services.products import suggestion_search_product_details,get_products_service
from app.schemas.products import ListSuggestionProducts,SuggestionProducts,ProductVariant
from uuid import UUID
from app.schemas.products import ProductListResponse
from app.schemas.product_variant import ProductDetailResponse
from app.services.products import get_product_by_id_service





router = APIRouter()

# Search for products based on the provided search term
@router.get('',dependencies=[Depends(get_current_user)])
def suggestion_search_product_api(db: Session = Depends(get_db), search: str = Query(...,min_length=3)):

    # Retrieve matching products from the service layer
    searched_products=suggestion_search_product_details(db,search)

    # Convert the products into the response schema
    response = ListSuggestionProducts(
    products=
    [
        SuggestionProducts(
            id=product.id,
            name=product.name,
            image=product.image,
            description=product.description,
            product_variant=[
                ProductVariant(
                    id=variant.id,
                    price=variant.price,
                    variant_name=variant.variant_name,
                )
                for variant in product.product_variants
            ],
        )
        for product in searched_products
    ]
)

    # Return the search results
    return response





# Retrieve all products belonging to a specific subcategory
@router.get(
    "/{subcategory_id}/subcategory",
    response_model=ProductListResponse,
    dependencies=[Depends(get_current_user)]
)
def get_products(
    subcategory_id: UUID,
    limit: int = Query(1, ge=1, le=50),
    cursor: str | None = Query(None),
    db: Session = Depends(get_db),
):

    return get_products_service(
        db=db,
        subcategory_id=subcategory_id,
        limit=limit,
        cursor=cursor,
    )



# Retrieve detailed information for a specific product
@router.get("/{product_id}",response_model=ProductDetailResponse,dependencies=[Depends(get_current_user)])
def get_product_by_id_api(product_id: UUID,db: Session = Depends(get_db)):

    # Fetch the product details from the service layer
    return get_product_by_id_service(
        db=db,
        product_id=product_id,
    )