from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.products import ProductCreate, ProductUpdate
from app.repositories.product import (
    create_product,
    get_all_products,
    get_product_by_id,
    update_product,
    delete_product,
)
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_admin
from app.models.user import User




router = APIRouter(
    prefix="/products",
    tags=["Admin Products"]
)




@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def add_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    return create_product(
        db,
        product
    )






@router.get("")
def list_products(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    skip = (page - 1) * limit

    result = get_all_products(
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






@router.get("/{product_id}")
def get_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    return get_product_by_id(
        db,
        product_id
    )








@router.patch("/{product_id}")
def edit_product(
    product_id: UUID,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    return update_product(
        db,
        product_id,
        product
    )







@router.delete("/{product_id}")
def remove_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    return delete_product(
        db,
        product_id
    )