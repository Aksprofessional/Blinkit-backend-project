from sqlalchemy import Column, Integer, ForeignKey,UUID
from app.db.database import Base
from sqlalchemy.orm import relationship

import uuid

from sqlalchemy import Column, ForeignKey, Integer, UUID, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.cart import Cart
from app.models.products import Products


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    cart_id = Column(
        UUID(as_uuid=True),
        ForeignKey("cart.id"),
        nullable=False
    )

    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1
    )

    cart = relationship(
        Cart,
        back_populates="cart_items"
    )

    product = relationship(
        Products,
        back_populates="cart_items"
    )

    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "product_id",
            name="uq_cart_product"
        ),
    )