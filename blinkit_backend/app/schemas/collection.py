from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class CollectionCreate(BaseModel):
    name: str
    display_order: int = 0
    is_active: bool = True


class CollectionUpdate(BaseModel):
    name: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


class CollectionResponse(BaseModel):
    name: str
    id: UUID
    display_order: int


class CollectionResponse(BaseModel):
    id: UUID
    name: str
    display_order: int


class CollectionListResponse(BaseModel):
    collections: list[CollectionResponse]