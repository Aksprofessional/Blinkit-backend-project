from pydantic import BaseModel
from typing import Optional
from fastapi import Form

class BrandCreate(BaseModel):
    name: str
    is_active: bool = True
def add_brand_pydantic(
    name: str = Form(...),
    is_active: bool = Form(True)
):
    return BrandCreate(
        name=name,
        is_active=is_active
        
    )


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


def update_brand_pydantic(
    name: str| None = Form(None),
    is_active: bool | None = Form(None)
):
    return BrandCreate(
        name=name,
        is_active=is_active
        
    )
