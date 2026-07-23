from app.repositories.cart import get_cart_by_user_id,create_cart
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status




def cart_create_or_get(db: Session, current_user_id: UUID):
    created=False
    user_cart=get_cart_by_user_id(db,current_user_id)
    if user_cart is None:
        user_cart=create_cart(db,current_user_id)
        created=True

    return user_cart,created



def check_cart_exists(db: Session, current_user_id: UUID):
    user_cart=get_cart_by_user_id(db,current_user_id)
    if user_cart is None:
        raise HTTPException(
                     status_code=status.HTTP_404_NOT_FOUND,
                     detail="cart not found"
                )
    return user_cart
