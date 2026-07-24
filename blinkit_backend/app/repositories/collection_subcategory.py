from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.collection_subcategory import CollectionSubCategory
from app.schemas.collection_subcategory import (
    CollectionSubCategoryCreate,
    CollectionSubCategoryUpdate,
)


def get_collection_subcategory_by_id(
    db: Session,
    collection_subcategory_id: UUID,
):
    db_mapping = db.get(
        CollectionSubCategory,
        collection_subcategory_id,
    )

    if db_mapping is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection SubCategory mapping not found",
        )

    return db_mapping


def get_all_collection_subcategories(
    db: Session,
):
    return db.query(
        CollectionSubCategory
    ).all()


def create_collection_subcategory(
    db: Session,
    mapping_data: CollectionSubCategoryCreate,
):
    db_mapping = CollectionSubCategory(
        **mapping_data.model_dump()
    )

    db.add(db_mapping)
    db.commit()
    db.refresh(db_mapping)

    return db_mapping


def update_collection_subcategory(
    db: Session,
    db_mapping: CollectionSubCategory,
    mapping_data: CollectionSubCategoryUpdate,
):
    update_data = mapping_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update.",
        )

    for key, value in update_data.items():
        setattr(
            db_mapping,
            key,
            value,
        )

    db.commit()
    db.refresh(db_mapping)

    return db_mapping


def delete_collection_subcategory(
    db: Session,
    db_mapping: CollectionSubCategory,
):
    db.delete(db_mapping)
    db.commit()

    return {
        "message": "Collection SubCategory mapping deleted successfully."
    }


def get_mapping_by_collection_and_subcategory(
    db: Session,
    collection_id: UUID,
    subcategory_id: UUID,
):
    return db.query(CollectionSubCategory).filter(
        CollectionSubCategory.collection_id == collection_id,
        CollectionSubCategory.subcategory_id == subcategory_id,
    ).first()


