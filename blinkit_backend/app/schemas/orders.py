from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import List
from pydantic import BaseModel
from app.schemas.order_items import OrderItemResponse
from app.models.orders import OrderStatus
from app.models.delivery_address import AddressType
from app.schemas.cursor import CursorResponse

class OrderCreateResponse(BaseModel):
    message: str
    order_id: UUID
    status: OrderStatus
    total_amount: Decimal


class OrderResponse(BaseModel):
    id: UUID
    status: OrderStatus
    created_at: datetime
    total_amount: Decimal

    receiver_name: str
    mobile_no: str

    address: str
    city: str
    state: str
    pincode: int

    address_type: AddressType
    custom_address_type: str | None = None

    order_item: List[OrderItemResponse]




class OrderResponseAll(BaseModel):
    id: UUID
    status: OrderStatus
    total_amount: Decimal
    created_at: datetime
    product_image: list[str]



class OrderListResponse(BaseModel):
    orders: list[OrderResponseAll]
    has_next: bool
    next_cursor: CursorResponse | None


class UnavailableProductOrderId(BaseModel):
    unavailable_cart_item_ids: set[UUID]