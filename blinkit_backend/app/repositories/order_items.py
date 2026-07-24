from sqlalchemy.orm import Session
from app.models.delivery_address import delivery_address,AddressType
from fastapi import HTTPException, status
from uuid import UUID
from app.models.order_items import order_items
from decimal import Decimal

def creat_order_item(db: Session, orderid: UUID, quantity: int,productvariantid: UUID, unit_price: Decimal ,total_price: Decimal ):
    user_order_item=order_items(
        product_variant_id=productvariantid,
        order_id=orderid,
        quantity=quantity,
        unit_price=unit_price,
        total_price=total_price
    )
    db.add(user_order_item)


