from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.exceptions.custom_exception import ConflictException

from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_admin

from app.models.user import User

from app.schemas.main_category import (
    MainCategoryCreate,
    MainCategoryUpdate,
)

from app.repositories.main_category import (
    get_main_category_by_id,
    get_main_category_by_name,
    get_all_main_categories,
    create_main_category,
    update_main_category,
    delete_main_category,
)

router = APIRouter(
    prefix="/main-category",
    tags=["Admin Main Category"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def add_main_category(
    main_category_data: MainCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    existing = get_main_category_by_name(
        db,
        main_category_data.name,
    )

    if existing:
        raise ConflictException(
                    "Main Category already exists"
                )

    return create_main_category(
        db,
        main_category_data,
    )


@router.get("")
def list_main_categories(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    skip = (page - 1) * limit

    return get_all_main_categories(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
    )


@router.get("/{main_category_id}")
def get_main_category(
    main_category_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    return get_main_category_by_id(
        db,
        main_category_id,
    )


@router.patch("/{main_category_id}")
def edit_main_category(
    main_category_id: UUID,
    main_category_data: MainCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    db_main_category = get_main_category_by_id(
        db,
        main_category_id,
    )

    return update_main_category(
        db,
        db_main_category,
        main_category_data,
    )


@router.delete("/{main_category_id}")
def remove_main_category(
    main_category_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    db_main_category = get_main_category_by_id(
        db,
        main_category_id,
    )

    return delete_main_category(
        db,
        db_main_category,
    )