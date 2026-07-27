from app.repositories.cart import get_cart_by_user_id,create_cart
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status




# Retrieve the user's cart or create a new one if it does not exist
def cart_create_or_get(db: Session, current_user_id: UUID):

    # Indicates whether a new cart was created
    created=False

    # Fetch the user's cart
    user_cart=get_cart_by_user_id(db,current_user_id)

    # Create a new cart if none exists
    if user_cart is None:
        user_cart=create_cart(db,current_user_id)
        created=True

    return user_cart,created



# Ensure that the user has an existing cart
def check_cart_exists(db: Session, current_user_id: UUID):

    # Retrieve the user's cart
    user_cart=get_cart_by_user_id(db,current_user_id)

    # Raise an exception if the cart does not exist
    if user_cart is None:
        raise HTTPException(
                     status_code=status.HTTP_404_NOT_FOUND,
                     detail="cart not found"
                )
    return user_cart