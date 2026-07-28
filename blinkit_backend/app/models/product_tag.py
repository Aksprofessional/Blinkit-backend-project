import uuid

from sqlalchemy import (
    Column,
    ForeignKey,
    UUID,
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class ProductTag(Base):
    __tablename__ = "product_tags"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id"),
        nullable=False,
    )

    tag_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tags.id"),
        nullable=False,
    )

    product = relationship(
        "Products",
        back_populates="tags",
    )

    tag = relationship(
        "Tag",
        back_populates="products",
    )