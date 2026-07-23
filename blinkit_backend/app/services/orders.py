from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.orders import OrderResponseAll
from app.schemas.cursor import CursorResponse
from app.models.orders import OrderStatus,FilterOrderStatus
from datetime import datetime
from app.services.cart import check_cart_exists
from fastapi import HTTPException,status
from app.utils.db import commit_or_500
from app.repositories.delivery_address import get_current_default_address_user
from app.repositories.cart_item import get_cart_items_for_order,delete_cart_items_list,get_cart_items_reorder,add_product_cart_item
from app.services.cart import check_cart_exists,cart_create_or_get
from uuid import UUID
from decimal import Decimal
from app.repositories.order_items import creat_order_item
from app.repositories.orders import order_create,get_order,get_all_order_pagination,get_order_by_id
from app.repositories.product_variant import lock_product_variant_for_order
from app.utils.cursor import decode_cursor,encode_cursor
from fastapi.encoders import jsonable_encoder



def place_order(db: Session,current_user: User,unavailable_cart_item_ids: set[UUID]):

    user_cart=check_cart_exists(db,current_user.id)
    user_delivery_address=get_current_default_address_user(db,current_user.id)

    user_cart_items=get_cart_items_for_order(db,user_cart.id)
    if user_cart_items == []:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='the cart has no products'
        )
    
    cart_item_ids_check = set()
    product_variant_ids = []

    for item in user_cart_items:
        cart_item_ids_check.add(item.cart_item_id)
        product_variant_ids.append(item.product_variant_id)
    if not unavailable_cart_item_ids.issubset(cart_item_ids_check):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid unavailable cart item ids."
        )
    product_variants=lock_product_variant_for_order(db,product_variant_ids)
    variant_map={variant.id:variant for variant in product_variants}
    products_not_available=[]
    product_quantity_insufficient=[]
    products_out_of_stock_id= set()
    total_amount=Decimal("0.00")

    for user_cart_item in user_cart_items:

        if user_cart_item.product_variant_deleted or user_cart_item.product_deleted:
            if user_cart_item.cart_item_id not in unavailable_cart_item_ids:
                product_variant_data = {
                    "product_variant_id": user_cart_item.product_variant_id,
                    "product_variant_name": user_cart_item.product_variant_name,
                    "product_name": user_cart_item.product_name,
                    "product_image": user_cart_item.product_image,
                    "cart_item_id": user_cart_item.cart_item_id,
                    "requested_quantity": user_cart_item.cart_item_quantity,
                    "available_quantity": 0,
                    "reason": "DISCONTINUED ",
                }
                products_not_available.append(product_variant_data)

            products_out_of_stock_id.add(user_cart_item.cart_item_id)
            continue

        lock_product_variant_stock=variant_map[user_cart_item.product_variant_id]
        if lock_product_variant_stock.stock_quantity>0:
            
            if lock_product_variant_stock.stock_quantity < user_cart_item.cart_item_quantity:
                product_variant_data={
                    "product_variant_id":user_cart_item.product_variant_id,
                    "product_variant_name":user_cart_item.product_variant_name,
                    "product_name": user_cart_item.product_name,
                    "product_image":user_cart_item.product_image,
                    "cart_item_id": user_cart_item.cart_item_id,
                    "requested_quantity":user_cart_item.cart_item_quantity,
                    "available_quantity": lock_product_variant_stock.stock_quantity,
                    "reason": "INSUFFICIENT STOCK"
                }

                
                product_quantity_insufficient.append(product_variant_data)
            else:
                total_amount += user_cart_item.cart_item_quantity * user_cart_item.product_variant_price

                    


            
        else:
            if user_cart_item.cart_item_id not in unavailable_cart_item_ids:
                
                product_variant_data={
                    "product_variant_id":user_cart_item.product_variant_id,
                    "product_variant_name":user_cart_item.product_variant_name,
                    "product_name": user_cart_item.product_name,
                    "product_image":user_cart_item.product_image,
                    "cart_item_id": user_cart_item.cart_item_id,
                    "requested_quantity":user_cart_item.cart_item_quantity,
                    "available_quantity": lock_product_variant_stock.stock_quantity,
                    "reason": "OUT OF STOCK",
                }
                products_not_available.append(product_variant_data)
            
            
            
            products_out_of_stock_id.add(user_cart_item.cart_item_id)


        
    
        


    if product_quantity_insufficient or (products_out_of_stock_id != unavailable_cart_item_ids):
        # if products_out_of_stock_id:
        #     delete_cart_items(db,products_out_of_stock_id)
        #     commit_or_500(db,'some items are out of stock but could not be removed')

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=jsonable_encoder({"message":"Your cart has changed. Please review it before placing the order.",
                    "product affected":products_not_available,
                    "insufficient quantity": product_quantity_insufficient
                    
                    })
        )

            
    if total_amount == Decimal("0.00"):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No purchasable items remain in the cart."
        )


    user_order=order_create(db,user_delivery_address,current_user.id,total_amount)

    for user_cart_item in user_cart_items:

        if user_cart_item.cart_item_id in unavailable_cart_item_ids:
            continue
        user_product_variant=variant_map[user_cart_item.product_variant_id]
        user_product_variant.stock_quantity -= user_cart_item.cart_item_quantity
        total_price=user_cart_item.cart_item_quantity * user_cart_item.product_variant_price
        creat_order_item(db,user_order.id,user_cart_item.cart_item_quantity,user_cart_item.product_variant_id,user_cart_item.product_variant_price,total_price)


    delete_cart_items_list(db,cart_item_ids_check)
    commit_or_500(db,'could not place the order')
    return user_order



def get_order_by_id(db: Session, current_user_id :UUID, order_id: UUID):
    user_order=get_order(db,current_user_id,order_id)
    return user_order


def reorder_by_user(db: Session, current_user: User, order_id: UUID):
    user_cart,created=cart_create_or_get(db,current_user.id)
    user_order=get_order(db,current_user.id,order_id)
    if not created:
        user_cart_items=get_cart_items_reorder(db,user_cart.id)
    product_not_available=[]
    user_cart_items_mapping={item.product_variant_id:item for item in user_cart_items}
    for order_item in user_order.order_item:
        existing_cart_item=user_cart_items_mapping.get(order_item.product_variant_id,None)
        if existing_cart_item:
            if existing_cart_item.product_variants.isdeleted or existing_cart_item.product_variants.product.isdeleted:
                
                continue
            if existing_cart_item.product_variants.stock_quantity > 0:
                if (existing_cart_item.quantity + order_item.quantity) > existing_cart_item.product_variants.stock_quantity:
                    product_variant_data={
                        "product_variant_id": existing_cart_item.product_variant_id,
                        "product_name":existing_cart_item.product_variants.product.name,
                        "product_variant_name":existing_cart_item.product_variants.variant_name,
                        "product_image":existing_cart_item.product_variants.product.image,
                        "reason": "INSUFFICIENT_STOCK",
                        "requested_quantity": existing_cart_item.quantity + order_item.quantity,
                        "added_quantity": max(0,existing_cart_item.product_variants.stock_quantity - existing_cart_item.quantity) ,
                        "available_quantity": existing_cart_item.product_variants.stock_quantity,
                        "final_quantity": existing_cart_item.product_variants.stock_quantity,
                        "message": "some items quantity were modified because of limited stock."
                    }
                    product_not_available.append(product_variant_data)
                    existing_cart_item.quantity = existing_cart_item.product_variants.stock_quantity
                else:
                    existing_cart_item.quantity += order_item.quantity
            else:
            
                continue
        else:
            if order_item.product_variants.isdeleted or order_item.product_variants.product.isdeleted:
                product_variant_data={
                    "product_variant_id":order_item.product_variant_id,
                    "product_name":order_item.product_variants.product.name,
                    "product_variant_name":order_item.product_variants.variant_name,
                    "product_image":order_item.product_variants.product.image,
                    "reason": "Discontinued"
                }
                product_not_available.append(product_variant_data)
                continue
            if order_item.product_variants.stock_quantity >0:
                if  order_item.quantity > order_item.product_variants.stock_quantity:
                    product_variant_data={
                        "product_variant_id": order_item.product_variant_id,
                        "product_name":order_item.product_variants.product.name,
                        "product_variant_name":order_item.product_variants.variant_name,
                        "product_image":order_item.product_variants.product.image,
                        "reason": "INSUFFICIENT_STOCK",
                        "requested_quantity": order_item.quantity,
                        "added_quantity": order_item.product_variants.stock_quantity,
                        "available_quantity": order_item.product_variants.stock_quantity,
                        "message": f"Only {order_item.product_variants.stock_quantity} items were added because of limited stock."
                    }
                    product_not_available.append(product_variant_data)
                    add_product_cart_item(db,order_item.product_variant_id,user_cart.id,order_item.product_variants.stock_quantity)
                else:
                    add_product_cart_item(db,order_item.product_variant_id,user_cart.id,order_item.quantity)
            else:
                product_variant_data={
                    "product_variant_id":order_item.product_variant_id,
                    "product_name":order_item.product_variants.product.name,
                    "product_variant_name":order_item.product_variants.variant_name,
                    "product_image": order_item.product_variants.product.image,
                    "reason": "Out Of Stock"
                }
                product_not_available.append(product_variant_data)
    commit_or_500(db,'could not fetch the items from previous order')
    return product_not_available
    

            
def get_all_orders(limit: int, db: Session, current_user: User, cursor: str | None, order_status: FilterOrderStatus | None ):
    cursor_created_at=None
    cursor_id=None
    if cursor is not None:
        cursor_created_at,cursor_id=decode_cursor(cursor)
    
    user_orders=get_all_order_pagination(limit,db,current_user.id,cursor_created_at,cursor_id,order_status)
    has_next = len(user_orders) > limit
    next_cursor=None
    if has_next:
        user_orders = user_orders[ :limit]
        last_order=user_orders[-1]
        encoded_cursor=encode_cursor(last_order.created_at,last_order.id)
        next_cursor=CursorResponse(
            cursor=encoded_cursor
        )
        
    user_orders_list=[]
    for user_order in user_orders:
        order_response=OrderResponseAll(
            id=user_order.id,
            status=user_order.status,
            total_amount=user_order.total_amount,
            created_at=user_order.created_at,
            product_image = [item.product_variants.product.image for item in user_order.order_item]
        )
        user_orders_list.append(order_response)
    
    return user_orders_list, has_next, next_cursor



def cancel_order(db: Session, current_user_id :UUID, order_id: UUID):
    user_order=get_order_by_id(db,current_user_id,order_id)
    if user_order.status == OrderStatus.CANCELLED:
        raise HTTPException(
            status_code=409,
            detail="Order has already been cancelled."
        )

    if user_order.status == OrderStatus.COMPLETED:
        raise HTTPException(
            status_code=409,
            detail="Completed orders cannot be cancelled."
        )

    if user_order.status == OrderStatus.CONFIRMED:
        raise HTTPException(
            status_code=409,
            detail="Confirmed orders can no longer be cancelled."
        )
    user_order.status = OrderStatus.CANCELED
    commit_or_500(db,'could not cancel the order due to server issue')
    return user_order





            