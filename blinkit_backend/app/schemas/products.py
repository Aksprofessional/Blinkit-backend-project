from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from decimal import Decimal
from fastapi import Form

class ProductCreate(BaseModel):
    name: str 
    description: str
    brand_id: UUID
    sub_category_id: UUID


def get_product(
    name: str = Form(...),
    description: str = Form(...),
    brand_id: UUID = Form(...),
    sub_category_id: UUID = Form(...),
):
    return ProductCreate(
        name=name,
        description=description,
        brand_id=brand_id,
        sub_category_id=sub_category_id,
    )


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    brand_id: Optional[UUID] = None
    sub_category_id: Optional[UUID] = None

def update_product_pydantic(
    name: str | None = Form(None),
    description: str | None = Form(None),
    brand_id: UUID | None = Form(None),
    sub_category_id: UUID | None = Form(None),
):
    return ProductUpdate(
        name=name,
        description=description,
        brand_id=brand_id,
        sub_category_id=sub_category_id,
    )

class ProductVariant(BaseModel):
    id: UUID
    price: Decimal
    variant_name: str
class SuggestionProducts(BaseModel):
    id: UUID
    name: str
    image: str
    description: str
    product_variant: list[ProductVariant]


class ListSuggestionProducts(BaseModel):
    products: list[SuggestionProducts]

class ProductVariantResponseFor(BaseModel):
    id: UUID
    variant_name: str
    price: Decimal


class ProductResponse(BaseModel):
    id: UUID
    name: str
    image: str
    description: str | None
    variants: list[ProductVariantResponseFor]


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    next_cursor: str | None = None
    has_next: bool