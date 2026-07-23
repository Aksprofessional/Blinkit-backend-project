from sqlalchemy import Column,ForeignKey,DECIMAL,UUID,func,DateTime,Enum,String,Integer
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid
from enum import Enum as pyEnum
from app.models.delivery_address import AddressType


class FilterOrderStatus(str,pyEnum):
    PENDING="pending"
    CONFIRMED="confirmed"
    COMPLETE="complete"
    CANCELED="canceled"
    ACTIVE="active"
class OrderStatus(str,pyEnum):
    PENDING="pending"
    CONFIRMED="confirmed"
    COMPLETE="complete"
    CANCELED="canceled"


class Order(Base):
    __tablename__='orders'
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True),ForeignKey('users.id'),index=True,nullable=False)
    status=Column(Enum(OrderStatus ,name='order_status'), nullable=False, default=OrderStatus.PENDING)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    total_amount=Column(DECIMAL(10,2),nullable=False)
    address=Column(String,nullable=False)
    reciever_name=Column(String,nullable=False)
    mobile_no=Column(String,nullable=False)
    pincode=Column(Integer,nullable=False)
    city=Column(String,nullable=False)
    state=Column(String,nullable=False)
    address_type= Column(Enum(AddressType , name="address_type_enum"), nullable=False)
    custom_address_type = Column(String, nullable=True)
    #relationship
    order_item=relationship(
        'order_items',
        back_populates='orders'
    )

    users=relationship(
        'User',
        back_populates='orders'
    )