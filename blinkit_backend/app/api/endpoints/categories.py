from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.category import CategoryListResponse
from uuid import UUID

from app.services.category import get_categories_service

router = APIRouter()


# Retrieve all categories, optionally filtered by collection
@router.get( "/",response_model=CategoryListResponse,)
def get_categories(db: Session = Depends(get_db),collection: UUID | None = Query(None)):

    # Delegate the category retrieval logic to the service layer
    return get_categories_service(
        db=db,
        collection=collection,
    )