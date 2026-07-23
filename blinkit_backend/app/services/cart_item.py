from sqlalchemy.orm import Session
from app.models.user import User
from app.models.cart import Cart
from app.models.product_variant import product_variant
from app.repositories import cart,cart_item
from fastapi import HTTPException,status
from app.utils.db import commit_or_500
from app.repositories.product_variant import get_product_variant
from app.services.products import check_product_variant_exist
from app.services.cart import cart_create_or_get,check_cart_exists
from uuid import UUID
from app.repositories.cart_item import get_cart_items,get_cart_item_by_cart_item_id,get_cart_item_by_product_variant_id
from app.schemas.cart_item import CartItemAction,GetCartItemResponse




def cart_item_exist(db: Session,cart_id: UUID, product_variant_id: UUID):
    cartitem=cart_item.get_product_from_cart(db,cart_id,product_variant_id)
    if cartitem is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='no such product in cart.'
        )
    return cartitem

def add_product(db: Session, current_user: User, product_variant_id: UUID):

    

    product_variant=check_product_variant_exist(db,product_variant_id)
    if product_variant.stock_quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The product is out of stock."
        )

    user_cart,created =cart_create_or_get(db,current_user.id)
    if not created:
        cartitem=cart_item.get_product_from_cart(db,user_cart.id,product_variant_id)
        if cartitem:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='product already exists in cart.'
            )
    cartitem=cart_item.add_product_cart_item(db,product_variant_id,user_cart.id)

    message_error='product could not be added to the cart'
    commit_or_500(db,message_error)

    
    
    return cartitem
            


def update_cart_item(db: Session, current_user: User, product_variant_id: int, action: CartItemAction):

    product_variant=check_product_variant_exist(db,product_variant_id)
    cartitem=get_cart_item_by_product_variant_id(db,current_user.id,product_variant_id)
    if action.action == CartItemAction.INCREMENT:
        if product_variant.stock_quantity>=cartitem.quantity+1:
            cartitem.quantity += 1
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Insufficient stock."
            )
    elif action.action == CartItemAction.DECREMENT:
        if cartitem.quantity == 1:
            cartitem.quantity = 0
            db.delete(cartitem)
        elif cartitem.quantity < 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='the product quantity is already 0'
            )
        else:
            cartitem.quantity -= 1
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="you cannot do the provided action."
        )

    
    message_error='product could not be updated to the cart'
    commit_or_500(db,message_error)

    return cartitem


def get_product_from_cart(db: Session, current_user_id: UUID):
    rows = get_cart_items(db, current_user_id)
    unavailable_cart_item_ids=set()
    if not rows:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no products in cart"
        )

    all_items = []
    total_price = 0

    for row in rows:
        row_data = dict(row._mapping)

        

        if row_data["product_deleted"]:
            row_data["is_available"] = False
            row_data["unavailable_reason"] = "PRODUCT_DELETED"
            unavailable_cart_item_ids.add(row_data["cart_item_id"])

        elif row_data["product_variant_deleted"]:
            row_data["is_available"] = False
            row_data["unavailable_reason"] = "VARIANT_DELETED"
            unavailable_cart_item_ids.add(row_data["cart_item_id"])

        elif row_data["product_variant_stock_quantity"] == 0:
            row_data["is_available"] = False
            row_data["unavailable_reason"] = "OUT_OF_STOCK"
            unavailable_cart_item_ids.add(row_data["cart_item_id"])

        elif row_data["cart_item_quantity"] > row_data["product_variant_stock_quantity"]:
            row_data["is_available"] = False
            row_data["unavailable_reason"] = "INSUFFICIENT_STOCK"



        else:
            
            row_data["item_total"]=(row_data["product_variant_price"]* row_data["cart_item_quantity"])
            total_price += row_data["item_total"]
            row_data["is_available"] = True
            row_data["unavailable_reason"] = None

        all_items.append(GetCartItemResponse.model_validate(row_data))

    return all_items, total_price, unavailable_cart_item_ids



def delete_cart_item(db: Session, current_user_id: UUID,cart_item_id: UUID):
    cart_item=get_cart_item_by_cart_item_id(db,current_user_id,cart_item_id)
    db.delete(cart_item)
    commit_or_500(db,'cart item could not be deleted')
    return cart_item