from app.repositories.collection import get_all_collection_customer
from app.schemas.collection import CollectionResponse
from sqlalchemy.orm import Session, selectinload
from app.models.category import Category
from app.models.collection import Collection
from app.models.collection_subcategory import CollectionSubCategory
from app.models.sub_category import SubCategory



# Retrieve all active collections
def get_all_collection(db: Session):

    # Fetch collections from the repository
    collections=get_all_collection_customer(db)

    # Store the converted response objects
    collections_list=[]

    # Convert each collection into the response schema
    for collection in collections:
        collection_pydantic=CollectionResponse(
            id=collection.id,
            name=collection.name,
            display_order=collection.display_order
        )
        collections_list.append(collection_pydantic)

    return collections_list



