from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.permissions import require_admin
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.brand import (
    BrandCreate,
    BrandUpdate
)

from app.repositories.brand import (
    create_brand,
    get_all_brands,
    get_brand_by_id,
    get_brand_by_name,
    update_brand,
    delete_brand
)

router = APIRouter(
    prefix="/brands",
    tags=["Admin Brands"]
)



@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def add_brand(
    brand_data: BrandCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    #checkinf if this brand already exists ,will not add
    existing_brand = get_brand_by_name(
        db,
        brand_data.name
    )

    if existing_brand:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Brand already exists"
        )
    
    return create_brand(
    db,
    brand_data
    )





@router.get("")
def get_brands(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    skip = (page - 1) * limit

    result = get_all_brands(
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






@router.get("/{brand_id}")
def get_brand(
    brand_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)

    return get_brand_by_id(
        db,
        brand_id
    )




@router.patch("/{brand_id}")
def update_brand_details(
    brand_id: UUID,
    brand_data: BrandUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)

    db_brand = get_brand_by_id(
        db,
        brand_id,
    )

    return update_brand(
        db,
        db_brand,
        brand_data
    )





@router.delete("/{brand_id}")
def remove_brand(
    brand_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)

    db_brand = get_brand_by_id(
        db,
        brand_id,
    )

    return delete_brand(
        db,
        db_brand
    )