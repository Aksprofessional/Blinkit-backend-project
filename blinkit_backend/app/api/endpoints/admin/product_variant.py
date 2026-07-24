from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_admin
from app.models.user import User

from app.schemas.product_variant import (
    ProductVariantCreate,
    ProductVariantUpdate,
)

from app.repositories.product_variant import (
    create_product_variant,
    get_all_product_variants,
    get_product_variant_by_id,
    update_product_variant,
    delete_product_variant,
)

router = APIRouter(
    prefix="/product-variants",
    tags=["Admin Product Variants"]
)




@router.post("")
def add_product_variant(
    variant: ProductVariantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    return create_product_variant(
        db,
        variant
    )





@router.get("")
def list_product_variants(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    skip = (page - 1) * limit

    result = get_all_product_variants(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
    )

    return {
        "page": page,
        "limit": limit,
        "search": search,
        "total": result["total"],
        "data": result["data"],
    }





@router.get("/{variant_id}")
def get_variant(
    variant_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    return get_product_variant_by_id(
        db,
        variant_id
    )






@router.patch("/{variant_id}")
def edit_variant(
    variant_id: UUID,
    variant: ProductVariantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    return update_product_variant(
        db,
        variant_id,
        variant
    )







@router.delete("/{variant_id}")
def remove_variant(
    variant_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    return delete_product_variant(
        db,
        variant_id
    )