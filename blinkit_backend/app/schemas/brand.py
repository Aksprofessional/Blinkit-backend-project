from pydantic import BaseModel
from typing import Optional


class BrandCreate(BaseModel):
    name: str
    logo: Optional[str] = None
    is_active: bool = True


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    logo: Optional[str] = None
    is_active: Optional[bool] = None