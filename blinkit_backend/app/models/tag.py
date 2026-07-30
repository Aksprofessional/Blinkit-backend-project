import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    String,
    UUID,
    func,
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name = Column(String,unique=True,nullable=False)
    is_active = Column(Boolean,default=True,nullable=False)
    created_at = Column(DateTime,server_default=func.now())
    #realtionship
    products = relationship(
        "ProductTag",
        back_populates="tag",
        cascade="all, delete-orphan",
    )

    section_tags = relationship(
        "SectionTag",
        back_populates="tag",
        cascade="all, delete-orphan"
    )