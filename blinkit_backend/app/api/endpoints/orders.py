from fastapi import APIRouter,Depends,Query,Body
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.dependencies.auth import get_current_user
from uuid import UUID
from app.models.orders import FilterOrderStatus
from app.services.orders import place_order,get_order_by_id,reorder_by_user,get_all_orders,cancel_order
from app.schemas.orders import OrderCreateResponse,OrderResponse,OrderResponseAll,OrderListResponse,UnavailableProductOrderId
from app.schemas.order_items import OrderItemResponse



router=APIRouter()


@router.post('/place')
def place_order_api( unavailable_cart_item_ids: UnavailableProductOrderId, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    unavailable_cart_item_ids_set=unavailable_cart_item_ids.unavailable_cart_item_ids
    user_order=place_order(db,current_user,unavailable_cart_item_ids_set)
    return OrderCreateResponse(
        message='order created successfully',
        order_id=user_order.id,
        status=user_order.status,
        total_amount=user_order.total_amount

    )

@router.get('/id/{order_id}')
def get_order_api(order_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_order=get_order_by_id(db,current_user.id,order_id)
    order_item_user=[
            OrderItemResponse(
                product_variant_id=item.product_variant_id,
                product_name=item.product_variants.product.name,
                product_image=item.product_variants.product.image,
                variant_name=item.product_variants.variant_name,

                quantity=item.quantity,  
                unit_price=item.unit_price,
                total_price=item.total_price,
            )
            for item in user_order.order_item
        ]
    return OrderResponse(
        id=user_order.id,
        status=user_order.status,
        created_at=user_order.created_at,
        total_amount=user_order.total_amount,

        receiver_name=user_order.reciever_name,
        mobile_no=user_order.mobile_no,

        address=user_order.address,
        city=user_order.city,
        state=user_order.state,
        pincode=user_order.pincode,

        address_type=user_order.address_type,
        custom_address_type=user_order.custom_address_type,

        order_item=order_item_user
    )

@router.post('/reorder/{order_id}')
def reorder_by_user_api(order_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product_unavailable=reorder_by_user(db,current_user,order_id)
    if product_unavailable:
        return {
            "message":"items added to cart with some changes",
            "affected_product": product_unavailable
        }
    return {
        "message":"items were added successfully."
    }


@router.get('')
def get_orders_all_api(cursor: str | None =Query(None), limit: int = Query(1, ge=1, le= 20), current_user: User = Depends(get_current_user), db: Session = Depends(get_db), orderstatus: FilterOrderStatus | None = Query(None)):
    user_orders,has_next,next_cursor=get_all_orders(limit, db, current_user, cursor,orderstatus)
    
    return OrderListResponse(
        orders=user_orders,
        has_next=has_next,
        next_cursor=next_cursor
    )

@router.patch('/cancel/{order_id}')
def order_cancel_api(order_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    order=cancel_order(db, current_user.id, order_id)
    return {
        "message": "Order cancelled successfully.",
        "order_id": order.id,
        "status": order.status
    }





