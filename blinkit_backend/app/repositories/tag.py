from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.section_tag import SectionTag
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate


def get_tag_by_id(
    db: Session,
    tag_id: UUID,
):
    db_tag = db.get(Tag, tag_id)

    if db_tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )

    return db_tag


def get_tag_by_name(
    db: Session,
    name: str,
):
    return (
        db.query(Tag)
        .filter(Tag.name == name)
        .first()
    )


def get_all_tags(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
):
    query = db.query(Tag)

    if search:
        query = query.filter(
            Tag.name.ilike(f"%{search}%")
        )

    total = query.count()

    tags = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "data": tags,
    }


def create_tag(
    db: Session,
    tag_data: TagCreate,
):
    existing = get_tag_by_name(
        db,
        tag_data.name,
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Tag already exists.",
        )

    db_tag = Tag(
        **tag_data.model_dump()
    )

    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)

    return db_tag


def update_tag(
    db: Session,
    db_tag: Tag,
    tag_data: TagUpdate,
):
    update_data = tag_data.model_dump(
        exclude_none=True,
        exclude_unset=True,
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided.",
        )

    if (
        "name" in update_data
        and update_data["name"] != db_tag.name
    ):
        existing = get_tag_by_name(
            db,
            update_data["name"],
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Tag already exists.",
            )

    for key, value in update_data.items():
        setattr(
            db_tag,
            key,
            value,
        )

    db.commit()
    db.refresh(db_tag)

    return db_tag


def delete_tag(
    db: Session,
    db_tag: Tag,
):
    db_tag.is_active = False

    db.commit()

    return {
        "message": "Tag deleted successfully."
    }



def check_all_tag_valid_by_id(db: Session, tag_ids: set[UUID]):
    db_tags=db.query(Tag.id).filter(Tag.id.in_(tag_ids)).all()
    if len(db_tags) != len(tag_ids):
        missing_ids=tag_ids-db_tags
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="some of the tags are not found.",
            missing_ids=f"tags not found, {missing_ids}."
        )
    return db_tags


def get_tag_by_section(db: Session, section_id: UUID):
    tags=db.query(SectionTag).filter(SectionTag.section_id==section_id).order_by(SectionTag.group_no.asc()).all()
    if tags is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="the section does not have any tags.",
        )
    return tags




