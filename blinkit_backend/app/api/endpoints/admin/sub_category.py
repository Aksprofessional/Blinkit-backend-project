from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_admin

from app.models.user import User

from app.schemas.sub_category import (
    SubCategoryCreate,
    SubCategoryUpdate
)

from app.repositories.sub_category import (
    create_subcategory,
    get_all_subcategories,
    get_subcategory_by_id,
    update_subcategory,
    delete_subcategory
)



router = APIRouter(
    prefix="/subcategories",
    tags=["Admin SubCategory"]
)



@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def add_subcategory(
    subcategory: SubCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)

    return create_subcategory(
        db,
        subcategory
    )





@router.get("")
def list_subcategories(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    skip = (page - 1) * limit

    result = get_all_subcategories(
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






@router.get("/{subcategory_id}")
def get_subcategory(
    subcategory_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)

    return get_subcategory_by_id(
        db,
        subcategory_id
    )





@router.patch("/{subcategory_id}")
def edit_subcategory(
    subcategory_id: UUID,
    subcategory: SubCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)

    return update_subcategory(
        db,
        subcategory_id,
        subcategory
    )







@router.delete("/{subcategory_id}")
def remove_subcategory(
    subcategory_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)

    return delete_subcategory(
        db,
        subcategory_id
    )