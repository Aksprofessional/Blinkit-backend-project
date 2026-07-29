from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.section import Section
from app.models.collection import Collection
from app.schemas.section import (
    SectionCreate,
    SectionUpdate,
)


def get_section_by_id(
    db: Session,
    section_id: UUID,
):
    db_section = db.get(
        Section,
        section_id,
    )

    if db_section is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found",
        )

    return db_section


def get_section_by_title(
    db: Session,
    title: str,
):
    return (
        db.query(Section)
        .filter(Section.title == title)
        .first()
    )


def get_all_sections(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
):
    query = db.query(Section)

    if search:
        query = query.filter(
            Section.title.ilike(f"%{search}%")
        )

    total = query.count()

    sections = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "data": sections,
    }


def create_section(
    db: Session,
    section_data: SectionCreate,
):
    collection = db.get(
        Collection,
        section_data.collection_id,
    )

    if collection is None:
        raise HTTPException(
            status_code=404,
            detail="Collection not found",
        )

    db_section = Section(
        **section_data.model_dump()
    )

    db.add(db_section)
    db.commit()
    db.refresh(db_section)

    return db_section


def update_section(
    db: Session,
    db_section: Section,
    section_data: SectionUpdate,
):
    update_data = section_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided.",
        )

    for key, value in update_data.items():
        setattr(
            db_section,
            key,
            value,
        )

    db.commit()
    db.refresh(db_section)

    return db_section


def delete_section(
    db: Session,
    db_section: Section,
):
    db_section.is_active = False

    db.commit()

    return {
        "message": "Section deleted successfully."
    }