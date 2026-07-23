from sqlalchemy.orm import Session,joinedload
from sqlalchemy import or_,and_
from app.models.delivery_address import delivery_address,AddressType
from fastapi import HTTPException, status
from uuid import UUID
from app.models.orders import FilterOrderStatus,OrderStatus
from app.models.orders import Order
from app.models.order_items import order_items
from app.models.product_variant import product_variant
from decimal import Decimal
from datetime import datetime

def order_create(db: Session,delivery_address:delivery_address, current_user_id: UUID,total_amount: Decimal):
    user_order=Order(
        user_id=current_user_id,
        address=delivery_address.address,
        reciever_name=delivery_address.reciever_name,
        mobile_no=delivery_address.mobile_no,
        pincode=delivery_address.pincode,
        city=delivery_address.city,
        state=delivery_address.state,
        address_type= delivery_address.address_type,
        custom_address_type = delivery_address.custom_address_type,
        total_amount=total_amount
    )
    db.add(user_order)
    db.flush()
    return user_order


def get_order(db: Session, current_user_id: UUID, order_id: UUID):
    user_order=db.query(Order).options(joinedload(Order.order_item).joinedload(order_items.product_variants).joinedload(product_variant.product)).filter(Order.id==order_id, Order.user_id==current_user_id).first()
    if user_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user does not have a order with the current order id.'
        )
    return user_order


def get_all_order_pagination(limit: int, db: Session, current_user_id: UUID, cursor_created_at: datetime | None = None, cursor_id: UUID | None = None, order_status: FilterOrderStatus | None = None):
    query = (
        db.query(Order).options(joinedload(Order.order_item).joinedload(order_items.product_variants).joinedload(product_variant.product)).filter(Order.user_id == current_user_id))

    if order_status:
        if order_status == FilterOrderStatus.ACTIVE:
            query = query.filter(
                Order.status.in_([OrderStatus.PENDING, order_status.CONFIRMED])
            )
        else:
            query = query.filter(Order.status == order_status)

    if cursor_created_at and cursor_id:
        query=query.filter( or_( Order.created_at < cursor_created_at, and_( Order.created_at == cursor_created_at, Order.id < cursor_id ) ) )

    return (
        query.order_by( Order.created_at.desc(), Order.id.desc() ).limit(limit + 1).all()
    )


def get_order_by_id(db: Session, current_user_id: UUID, order_id: UUID):
    user_order=db.query(Order).filter(Order.user_id==current_user_id,Order.id == order_id).first()
    if user_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user does not have a order with the current order id.'
        )
    return user_order
