from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.permissions import require_admin

from app.models.user import User
from app.schemas.tag import (
    TagCreate,
    TagUpdate,
)

from app.repositories.tag import (
    create_tag,
    delete_tag,
    get_all_tags,
    get_tag_by_id,
    update_tag,
)

router = APIRouter(
    prefix="/tags",
    tags=["Admin Tags"],
)




@router.post("")
def add_tag(
    tag: TagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return create_tag(
        db,
        tag,
    )






@router.get("")
def list_tags(
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    skip = (page - 1) * limit

    return get_all_tags(
        db,
        skip,
        limit,
        search,
    )







@router.get("/{tag_id}")
def get_tag(
    tag_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_tag_by_id(
        db,
        tag_id,
    )




@router.patch("/{tag_id}")
def edit_tag(
    tag_id: UUID,
    tag: TagUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    db_tag = get_tag_by_id(
        db,
        tag_id,
    )

    return update_tag(
        db,
        db_tag,
        tag,
    )








@router.delete("/{tag_id}")
def remove_tag(
    tag_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    db_tag = get_tag_by_id(
        db,
        tag_id,
    )

    return delete_tag(
        db,
        db_tag,
    )