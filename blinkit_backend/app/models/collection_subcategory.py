from sqlalchemy import Column, UUID, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid

class CollectionSubCategory(Base):

    __tablename__ = "collection_subcategories"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    collection_id = Column(
        UUID(as_uuid=True),
        ForeignKey("collections.id"),
        nullable=False
    )

    subcategory_id = Column(
        UUID(as_uuid=True),
        ForeignKey("subcategory.id"),
        nullable=False
    )

    display_order = Column(
        Integer,
        default=0
    )

    collection = relationship(
        "Collection",
        back_populates="collection_subcategories"
    )

    subcategory = relationship(
        "SubCategory",
        back_populates="collection_subcategories"
    )