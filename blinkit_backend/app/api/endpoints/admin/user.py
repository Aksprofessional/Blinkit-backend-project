from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_admin

from app.models.user import User

from app.repositories.user import (
    get_all_users,
    get_user_by_id,
    disable_user,
    enable_user,
)

router = APIRouter(
    prefix="/users",
    tags=["Admin Users"],
)



@router.get("")
def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    skip = (page - 1) * limit

    return get_all_users(
        db,
        skip,
        limit,
        search,
    )









@router.get("/{user_id}")
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    return get_user_by_id(
        db,
        user_id,
    )








@router.patch("/{user_id}/disable")
def disable_user_account(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    db_user = get_user_by_id(
        db,
        user_id,
    )

    return disable_user(
        db,
        db_user,
    )






@router.patch("/{user_id}/enable")
def enable_user_account(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    db_user = get_user_by_id(
        db,
        user_id,
    )

    return enable_user(
        db,
        db_user,
    )