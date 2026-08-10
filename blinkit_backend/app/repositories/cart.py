from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.cart import Cart
from app.exceptions.custom_exception import InternalServerException
from app.core.logger import logger


def get_cart_by_user_id(db: Session,user_id: UUID):
    cart=db.query(Cart).filter(Cart.user_id==user_id).first()
    return cart


def create_cart(db: Session, userid: UUID):
    try:
        user_cart=Cart(user_id=userid)
        db.add(user_cart)
        # Flush to generate cart ID without committing the transaction.
        db.flush()
        return user_cart
    except Exception:
        db.rollback()

        raise InternalServerException(
            "Failed to create cart"
        )