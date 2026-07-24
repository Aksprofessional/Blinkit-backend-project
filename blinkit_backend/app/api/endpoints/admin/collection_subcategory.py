from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.permissions import require_admin
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.collection_subcategory import (
    CollectionSubCategoryCreate,
    CollectionSubCategoryUpdate,
)

from app.repositories.collection_subcategory import (
    get_collection_subcategory_by_id,
    get_all_collection_subcategories,
    get_mapping_by_collection_and_subcategory,
    create_collection_subcategory,
    update_collection_subcategory,
    delete_collection_subcategory,
)

from app.repositories.collection import (
    get_collection_by_id,
)

from app.repositories.sub_category import (
    get_subcategory_by_id,
)

router = APIRouter(
    prefix="/collection-subcategories",
    tags=["Admin Collection SubCategory"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def add_collection_subcategory(
    mapping_data: CollectionSubCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    # Validate Collection
    get_collection_by_id(
        db,
        mapping_data.collection_id,
    )

    # Validate SubCategory
    get_subcategory_by_id(
        db,
        mapping_data.subcategory_id,
    )

    existing_mapping = get_mapping_by_collection_and_subcategory(
        db,
        mapping_data.collection_id,
        mapping_data.subcategory_id,
    )

    if existing_mapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SubCategory already exists in this collection.",
        )

    return create_collection_subcategory(
        db,
        mapping_data,
    )





@router.get("")
def get_collection_subcategories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    return get_all_collection_subcategories(db)



@router.get("/{mapping_id}")
def get_collection_subcategory(
    mapping_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    return get_collection_subcategory_by_id(
        db,
        mapping_id,
    )




@router.patch("/{mapping_id}")
def update_collection_subcategory_details(
    mapping_id: UUID,
    mapping_data: CollectionSubCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    db_mapping = get_collection_subcategory_by_id(
        db,
        mapping_id,
    )

    return update_collection_subcategory(
        db,
        db_mapping,
        mapping_data,
    )





@router.delete("/{mapping_id}")
def remove_collection_subcategory(
    mapping_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    db_mapping = get_collection_subcategory_by_id(
        db,
        mapping_id,
    )

    return delete_collection_subcategory(
        db,
        db_mapping,
    )