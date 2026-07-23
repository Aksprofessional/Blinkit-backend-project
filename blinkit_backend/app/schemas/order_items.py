from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    product_variant_id: UUID

    product_name: str
    product_image: str 
    variant_name: str

    quantity: int
    unit_price: Decimal
    total_price: Decimal

    
