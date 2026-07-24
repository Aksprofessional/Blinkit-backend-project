from fastapi import HTTPException,status
from sqlalchemy.orm import Session,joinedload
from uuid import UUID
from app.models.cart import Cart
from app.models.cart_item import CartItem

def get_cart_by_user_id(db: Session,user_id: UUID):
    cart=db.query(Cart).filter(Cart.user_id==user_id).first()
    return cart


def create_cart(db: Session, userid: UUID):
    try:
        user_cart=Cart(user_id=userid)
        db.add(user_cart)
        db.flush()
        return user_cart
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="could not create a cart due to database error"
        )


