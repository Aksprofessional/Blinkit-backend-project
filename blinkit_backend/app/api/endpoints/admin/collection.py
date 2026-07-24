from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.permissions import require_admin
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.collection import (
    CollectionCreate,
    CollectionUpdate
)

from app.repositories.collection import (
    get_collection_by_id,
    get_collection_by_name,
    get_all_collections,
    create_collection,
    update_collection,
    delete_collection
)

router = APIRouter(
    prefix="/collection",
    tags=["Admin Collection"]
)



@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)


def add_collection(
    collection_data: CollectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    existing_collection = get_collection_by_name(
        db,
        collection_data.name,
    )

    if existing_collection:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Collection already exists",
        )

    return create_collection(
        db,
        collection_data,
    )




@router.get("")
def list_collections(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    skip = (page - 1) * limit

    result = get_all_collections(
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






@router.get("/{collection_id}")
def get_collection(
    collection_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    return get_collection_by_id(
        db,
        collection_id,
    )




@router.patch("/{collection_id}")
def update_collection_details(
    collection_id: UUID,
    collection_data: CollectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    db_collection = get_collection_by_id(
        db,
        collection_id,
    )

    return update_collection(
        db,
        db_collection,
        collection_data,
    )





@router.delete("/{collection_id}")
def remove_collection(
    collection_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    db_collection = get_collection_by_id(
        db,
        collection_id,
    )

    return delete_collection(
        db,
        db_collection,
    )