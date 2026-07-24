from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class SubCategoryCreate(BaseModel):
    name: str
    is_active: bool = True
    category_id: UUID



class SubCategoryUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[UUID] = None
    is_active: Optional[bool] = None
