from fastapi import APIRouter,Depends,Query,Body
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.dependencies.auth import get_current_user
from uuid import UUID
from app.models.orders import FilterOrderStatus
from app.services.orders import place_order,get_order_by_id,reorder_by_user,get_all_orders,cancel_order
from app.schemas.orders import OrderCreateResponse,OrderResponse,OrderListResponse,UnavailableProductOrderId
from app.schemas.order_items import OrderItemResponse



router=APIRouter()


# Place a new order for the authenticated user
@router.post('/place')
def place_order_api( unavailable_cart_item_ids: UnavailableProductOrderId, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    # Extract the unavailable cart item ids provided by the client
    unavailable_cart_item_ids_set=unavailable_cart_item_ids.unavailable_cart_item_ids

    # Create the order
    user_order=place_order(db,current_user,unavailable_cart_item_ids_set)

    # Return the created order details
    return OrderCreateResponse(
        message='order created successfully',
        order_id=user_order.id,
        status=user_order.status,
        total_amount=user_order.total_amount

    )


# Retrieve a specific order by its id
@router.get('/id/{order_id}')
def get_order_api(order_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    # Fetch the requested order
    user_order=get_order_by_id(db,current_user.id,order_id)

    # Convert order items into the response schema
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

    # Return the complete order response
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


# Reorder all items from a previous order
@router.post('/reorder/{order_id}')
def reorder_by_user_api(order_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    # Attempt to add all products from the previous order back to the cart
    product_unavailable=reorder_by_user(db,current_user,order_id)

    # Return affected products if some items could not be added as requested
    if product_unavailable:
        return {
            "message":"items added to cart with some changes",
            "affected_product": product_unavailable
        }

    # Return a success response if all items were added
    return {
        "message":"items were added successfully."
    }


# Retrieve all orders for the authenticated user with optional pagination and filtering
@router.get('')
def get_orders_all_api(cursor: str | None =Query(None), limit: int = Query(1, ge=1, le= 20), current_user: User = Depends(get_current_user), db: Session = Depends(get_db), orderstatus: FilterOrderStatus | None = Query(None)):

    # Fetch the paginated list of orders
    user_orders,has_next,next_cursor=get_all_orders(limit, db, current_user, cursor,orderstatus)
    
    # Return the paginated order response
    return OrderListResponse(
        orders=user_orders,
        has_next=has_next,
        next_cursor=next_cursor
    )


# Cancel an existing order
@router.patch('/cancel/{order_id}')
def order_cancel_api(order_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    # Cancel the specified order
    order=cancel_order(db, current_user.id, order_id)

    # Return the updated order status
    return {
        "message": "Order cancelled successfully.",
        "order_id": order.id,
        "status": order.status
    }