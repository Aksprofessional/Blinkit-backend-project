from sqlalchemy import Column,Integer,String,ForeignKey,Float,UUID,func,DateTime,Enum
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid
from enum import Enum as pyEnum
from app.models.products import Products
from app.models.orders import order



class order_items(Base):
    __tablename__='order_items'
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id=Column(UUID,ForeignKey('products.id'),nullable=False)
    order_id=Column(UUID,ForeignKey('orders.id'),nullable=False)
    quantitiy=Column(Integer,nullable=False)

    #relationship
    products=relationship(
        Products,
        back_populates='order_itmes'
    )
    orders=relationship(
        order,
        back_populates='order_items'
    )