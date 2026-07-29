from sqlalchemy import Column, UUID, String, Boolean, Integer
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid

class Collection(Base):
    __tablename__ = "collections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, unique=True, nullable=False)

    display_order = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)

    main_categories = relationship(
        "MainCategory",
        back_populates="collection",
    )
    
    sections = relationship(
        "Section",
        back_populates="collection",
        cascade="all, delete-orphan",
    )