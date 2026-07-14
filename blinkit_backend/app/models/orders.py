from sqlalchemy import Column,Integer,String,ForeignKey,Float,UUID,func,DateTime,Enum
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid
from enum import Enum as pyEnum
from app.models.order_items import order_product
from app.models.user import User

class status(str,pyEnum):
    PENDING="pending"
    COMPLETE="compelete"
    CANCELED="canceled"

class order(Base):
    __tablename__='orders'
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id=Column(UUID,ForeignKey('users.id'),index=True,nullable=False)
    status=Column(Enum(status ,name='order_status'), nullable=False, default=status.PENDING)
    created_at=Column(DateTime,server_default=func.now())
    total_price=Column(Float,nullable=False)
    #relationship

    order_items=relationship(
        order_product,
        back_populates='orders'
    )
    users=relationship(
        User,
        back_populates='orders'
    )