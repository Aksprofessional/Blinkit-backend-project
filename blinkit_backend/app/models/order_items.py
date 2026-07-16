from sqlalchemy import Column,Integer,ForeignKey,UUID,DECIMAL,UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid





class order_items(Base):
    __tablename__='order_items'
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_variant_id = Column(UUID(as_uuid=True),ForeignKey("product_variant.id"),nullable=False)
    order_id=Column(UUID(as_uuid=True),ForeignKey('orders.id'),nullable=False)
    quantitiy=Column(Integer,nullable=False)
    bought_price=Column(DECIMAL(10,2),nullable=False)

    #relationship
    orders=relationship(
        'order',
        back_populates='order_item'
    )
    product_variants = relationship(
        'product_variant',
        back_populates="order_item"
    )

    __table_args__ = (
        UniqueConstraint(
            "product_variant_id",
            "order_id",
            name="uq_product_order"
        ),
    )