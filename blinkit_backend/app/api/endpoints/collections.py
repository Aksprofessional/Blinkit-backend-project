from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.dependencies.auth import get_current_user
from uuid import UUID
from app.services.collections import get_all_collection
from app.schemas.collection import CollectionResponse
from app.schemas.category import (
    DiscoveryCategoryResponse,
)

from app.services.collections import get


router=APIRouter()

@router.get('',dependencies=[get_current_user],response_model = CollectionResponse)
def get_all_collection_api(db: Session = Depends(get_db)):
    return get_all_collection(db)
    

