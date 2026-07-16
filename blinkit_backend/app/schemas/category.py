from pydantic import BaseModel
from typing import Optional


class CategoryCreate(BaseModel):
    name: str
    is_active: bool = True


class CategoryUpdate(BaseModel):
    name: Optional[str]= None
    is_active: Optional[bool] = None