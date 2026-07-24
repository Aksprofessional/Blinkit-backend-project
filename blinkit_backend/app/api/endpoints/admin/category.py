from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.permissions import require_admin
from app.models.user import User
from app.schemas.category import CategoryCreate,CategoryUpdate
from uuid import UUID
from app.repositories.category import (
    add_category,
    get_category_by_name,
    get_all_categories,
    get_category_by_id,
    update_category,
    delete_category,
)

router = APIRouter(
    prefix="/category",
    tags=["Admin Category"],
)

#for adding category
@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    require_admin(current_user)
    existing_category = get_category_by_name(
        db,
        category.name,
    )

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists",
        )

    new_category = add_category(
        db,
        category,
    )

    return {
        "message": "Category created successfully",
        "data": new_category,
    }




#for getting all categories
@router.get("")
def list_categories(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    require_admin(current_user)

    skip = (page - 1) * limit

    categories = get_all_categories(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
    )

    return {
        "page": page,
        "limit": limit,
        "search": search,
        "message": "Categories fetched successfully",
        "data": categories,
    }







@router.get("/{category_id}")
def get_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    category = get_category_by_id(
        db,
        category_id,
    )

    return {
        "message": "Category fetched successfully",
        "data": category,
    }







@router.patch("/{category_id}")
def edit_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    require_admin(current_user)
    category = get_category_by_id(
        db,
        category_id,
    )

    #leaving those fields as it is which isnt sent by the admin to change.
    update_data = category_data.model_dump(
        exclude_unset=True,
    )

    for key, value in update_data.items():
        setattr(category, key, value)

    updated_category = update_category(
        db,
        category,
    )

    return {
        "message": "Category updated successfully",
        "data": updated_category,
    }






@router.delete("/{category_id}")
def remove_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    require_admin(current_user)
    category = get_category_by_id(
        db,
        category_id,
    )

    delete_category(
        db,
        category,
    )

    return {
        "message": "Category deleted successfully"
    }