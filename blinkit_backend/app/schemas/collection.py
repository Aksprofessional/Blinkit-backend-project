from pydantic import BaseModel
from typing import Optional

class CollectionCreate(BaseModel):
    name: str
    display_order: int = 0
    is_active: bool = True


class CollectionUpdate(BaseModel):
    name: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None