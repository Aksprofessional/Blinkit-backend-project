import uuid

from sqlalchemy import Boolean, Column, Integer, String, UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from app.db.database import Base


class MainCategory(Base):
    __tablename__ = "main_categories"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name = Column(
        String,
        unique=True,
        nullable=False,
    )

    display_order = Column(
        Integer,
        default=0,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )
    collection_id = Column(
        UUID(as_uuid=True),
        ForeignKey("collections.id"),
        nullable=False,
    )

    #relationship
    categories = relationship(
        "Category",
        back_populates="main_category",
    )

    collection = relationship(
        "Collection",
        back_populates="main_categories",
    )

    