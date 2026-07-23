from pydantic import BaseModel,ConfigDict
from typing import Optional
from uuid import UUID
from enum import Enum
from decimal import Decimal

class CartItemAction(str,Enum):
    INCREMENT = "increment"
    DECREMENT = "decrement"



class CartItemRespone(BaseModel):
    id: UUID
    cart_id: UUID
    product_variant_id: UUID
    quantity: int

    model_config = ConfigDict(from_attributes=True)



class AddItemResponse(BaseModel):
    message: str
    cart_item: CartItemRespone

    model_config = ConfigDict(from_attributes=True)


class UpdateCartItem(BaseModel):
    action: CartItemAction


class UpdateItemResponse(BaseModel):
    cart_item_id: UUID 
    quantity: int
    removed: bool
    message: str


class GetCartItemResponse(BaseModel):
    cart_item_id: UUID
    cart_item_quantity: int

    product_variant_id: UUID
    product_variant_price: int
    variant_name: str
    product_variant_stock_quantity: int
    item_total: Decimal | None = None

    product_name: str
    product_image: str 

    is_available: bool
    unavailable_reason: str | None = None


class GetItemCartResponeFinal(BaseModel):
    cartitmes: list[GetCartItemResponse]
    total: int
    total_price: Decimal
    unavailable_cart_item_ids: set[UUID]