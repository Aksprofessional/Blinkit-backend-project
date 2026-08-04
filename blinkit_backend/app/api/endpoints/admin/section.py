from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_admin
from app.db.database import get_db
from app.models.user import User
from app.schemas.section import SectionCreate,SectionUpdate
from app.repositories.section import create_section,delete_section,get_all_sections,get_section_by_id,update_section


router = APIRouter(
    prefix="/sections",
    tags=["Admin Sections"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def add_section(
    section: SectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)
    return create_section(db, section)


@router.get("/")
def list_sections(
    skip: int = 0,
    limit: int = Query(default=10, le=100),
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)
    return get_all_sections(
        db,
        skip,
        limit,
        search,
    )


@router.get("/{section_id}")
def get_section(
    section_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)
    return get_section_by_id(
        db,
        section_id,
    )


@router.patch("/{section_id}")
def edit_section(
    section_id: UUID,
    section: SectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    db_section = get_section_by_id(
        db,
        section_id,
    )

    return update_section(
        db,
        db_section,
        section,
    )


@router.delete("/{section_id}")
def remove_section(
    section_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)
    db_section = get_section_by_id(
        db,
        section_id,
    )

    return delete_section(
        db,
        db_section,
    )




