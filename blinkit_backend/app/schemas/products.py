from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class ProductCreate(BaseModel):
    name: str
    image: str
    description: str
    brand_id: UUID
    sub_category_id: UUID


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    brand_id: Optional[UUID] = None
    sub_category_id: Optional[UUID] = None