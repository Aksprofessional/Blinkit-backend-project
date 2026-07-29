import uuid

from sqlalchemy import (
    Column,
    UUID,
    String,
    Integer,
    ForeignKey,
    Boolean,
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class Section(Base):
    __tablename__ = "sections"


    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


    title = Column(
        String,
        nullable=False,
    )


    display_order = Column(
        Integer,
        default=0,
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


    collection = relationship(
        "Collection",
        back_populates="sections",
    )

    tags = relationship(
        "SectionTag",
        back_populates="section",
        cascade="all, delete-orphan"
    )