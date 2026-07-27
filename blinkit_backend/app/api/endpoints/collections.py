from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.services.collections import get_all_collection
from app.schemas.collection import CollectionListResponse





router=APIRouter()

# Retrieve all collections for the authenticated user
@router.get('',dependencies=[Depends(get_current_user)],response_model = CollectionListResponse)
def get_all_collection_api(db: Session = Depends(get_db)):

    # Debug statement indicating that the endpoint has been reached
    print('ENDPOINT REACHED')

    # Fetch all collections from the service layer
    collections_list= get_all_collection(db)

    # Return the list of collections in the response schema
    return CollectionListResponse(
        collections=collections_list
        
    )
    