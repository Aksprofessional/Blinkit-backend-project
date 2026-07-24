from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class CollectionSubCategoryCreate(BaseModel):

    collection_id: UUID

    subcategory_id: UUID

    display_order: int = 0


class CollectionSubCategoryUpdate(BaseModel):

    display_order: Optional[int] = None