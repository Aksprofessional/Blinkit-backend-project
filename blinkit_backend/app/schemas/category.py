from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class CategoryCreate(BaseModel):
    name: str
    is_active: bool = True


class CategoryUpdate(BaseModel):
    name: Optional[str]= None
    is_active: Optional[bool] = None



from uuid import UUID
from pydantic import BaseModel


class SubCategoryResponse(BaseModel):
    id: UUID
    name: str


class CategoryResponse(BaseModel):
    id: UUID
    name: str
    sub_categories: list[SubCategoryResponse]


class CategoryListResponse(BaseModel):
    categories: list[CategoryResponse]