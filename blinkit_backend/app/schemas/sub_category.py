from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class SubCategoryCreate(BaseModel):
    name: str
    category_id: UUID
    is_active: bool = True


class SubCategoryUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[UUID] = None
    is_active: Optional[bool] = None