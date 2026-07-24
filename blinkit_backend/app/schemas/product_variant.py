from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ProductVariantCreate(BaseModel):
    product_id: UUID
    variant_name: str
    sku: str
    price: Decimal = Field(gt=0)
    stock_quantity: int = Field(ge=0)


class ProductVariantUpdate(BaseModel):
    variant_name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[Decimal] = Field(default=None, gt=0)
    stock_quantity: Optional[int] = Field(default=None, ge=0)