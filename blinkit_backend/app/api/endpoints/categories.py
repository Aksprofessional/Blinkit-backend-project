from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.category import CategoryListResponse
from uuid import UUID

from app.services.category import get_categories_service

router = APIRouter()


# Retrieve all categories, optionally filtered by collection
@router.get( "/{collection_id}",response_model=CategoryListResponse,dependencies=[Depends(get_current_user)])
def get_categories(collection_id: UUID , db: Session = Depends(get_db)):

    # Delegate the category retrieval logic to the service layer
    return get_categories_service(
        db=db,
        collection=collection_id,
    )