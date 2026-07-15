from app.db.database import Base
from sqlalchemy import Column,String,UUID
from sqlalchemy.orm import relationship
import uuid

class Category(Base):
    __tablename__="category"
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name= Column(String,unique=True)

    #relationship
    products= relationship(
        'Products',
        back_populates='category',
        cascade="all, delete-orphan"
    )