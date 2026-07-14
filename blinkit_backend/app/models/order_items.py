from sqlalchemy import Column,Integer,ForeignKey,UUID,DECIMAL,UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid
from app.models.products import Products
from app.models.orders import order



class order_items(Base):
    __tablename__='order_items'
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id=Column(UUID,ForeignKey('products.id'),nullable=False)
    order_id=Column(UUID,ForeignKey('orders.id'),nullable=False)
    quantitiy=Column(Integer,nullable=False)
    bought_price=Column(DECIMAL(10,2),nullable=False)

    #relationship
    products=relationship(
        Products,
        back_populates='order_itme'
    )
    orders=relationship(
        order,
        back_populates='order_item'
    )

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "order_id",
            name="uq_product_name_size"
        ),
    )