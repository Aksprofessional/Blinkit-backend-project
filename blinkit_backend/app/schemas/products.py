from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from decimal import Decimal

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



from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel


class ProductVariantResponse(BaseModel):
    id: UUID
    variant_name: str
    price: Decimal


class ProductResponse(BaseModel):
    id: UUID
    name: str
    image: str
    description: str | None
    variants: list[ProductVariantResponse]


class ProductListResponse(BaseModel):
    products: list[ProductResponse]