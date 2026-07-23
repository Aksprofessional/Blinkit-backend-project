from sqlalchemy import Column, Integer, ForeignKey,UUID,DateTime,UniqueConstraint
from sqlalchemy.orm import relationship
import uuid
from app.db.database import Base
from sqlalchemy.sql import func


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    cart_id = Column(UUID(as_uuid=True),ForeignKey("cart.id",ondelete="CASCADE"),nullable=False)
    product_variant_id = Column(UUID(as_uuid=True),ForeignKey("product_variant.id"),nullable=False)
    quantity = Column(Integer,nullable=False,default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    #relationship

    cart = relationship(
        'Cart',
        back_populates="cart_items"
        )

    product_variants = relationship(
        'product_variant',
        back_populates="cart_items"
        )
    
    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "product_variant_id",
            name="uq_cart_product"
        ),
    )