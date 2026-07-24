from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from typing import Optional

from app.models.collection import Collection
from app.schemas.collection import CollectionCreate, CollectionUpdate


def get_collection_by_id(
    db: Session,
    collection_id: UUID,
):
    db_collection = db.get(
        Collection,
        collection_id,
    )

    if db_collection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found",
        )

    return db_collection


def get_collection_by_name(
    db: Session,
    collection_name: str,
):
    return db.query(Collection).filter(
        Collection.name == collection_name
    ).first()






def get_all_collections(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
):
    query = db.query(Collection)

    if search:
        query = query.filter(
            Collection.name.ilike(f"%{search}%")
        )

    total = query.count()

    collections = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "data": collections,
    }







def create_collection(
    db: Session,
    collection_data: CollectionCreate,
):
    db_collection = Collection(
        **collection_data.model_dump()
    )

    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)

    return db_collection


def update_collection(
    db: Session,
    db_collection: Collection,
    collection_data: CollectionUpdate,
):
    update_data = collection_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update.",
        )

    for key, value in update_data.items():
        setattr(
            db_collection,
            key,
            value,
        )

    db.commit()
    db.refresh(db_collection)

    return db_collection


def delete_collection(
    db: Session,
    db_collection: Collection,
):
    db_collection.is_active = False

    db.commit()

    return {
        "message": "Collection deleted successfully."
    }




