from app.db.database import Base
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.models.cart_item import CartItem
from app.models.user import User


class Cart(Base):
    __tablename__="cart"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_id=Column(UUID,ForeignKey("user.id"),unique=True,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship(
        User,
        back_populates="cart"
    )

    cart_items = relationship(
        CartItem,
        back_populates="cart",
        cascade="all, delete-orphan"
    )