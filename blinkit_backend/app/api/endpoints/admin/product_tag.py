from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from uuid import UUID

from app.db.database import get_db
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_admin
from app.schemas.product_tag import ProductTagCreate
from app.repositories.product_tag import (
    add_product_tag,
    delete_product_tag,
    get_product_tags,
)

router = APIRouter(
    prefix="/product-tags",
    tags=["Admin Product Tags"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_mapping(
    product_tag: ProductTagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)
    return add_product_tag(
        db,
        product_tag,
    )


@router.get("/")
def list_mappings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)
    return get_product_tags(db)


@router.delete("/{mapping_id}")
def remove_mapping(
    mapping_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)
    return delete_product_tag(
        db,
        mapping_id,
    )