from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session,Query

from app.db.database import get_db

from app.schemas.category import (
    CategoryListResponse
)

from app.services.category import (
    get_categories_service,
)

router = APIRouter(
    tags=["Customer Discovery"],
)


@router.get(
    "/categories",
    response_model=CategoryListResponse,
)
def get_categories(
    db: Session = Depends(get_db),
    collection: str | None = Query(None),
):
    return get_categories_service(
        db=db,
        collection=collection,
    )