from app.db.database import Base
from sqlalchemy import Column,String,UUID,Boolean
from sqlalchemy.orm import relationship
import uuid

class Category(Base):
    __tablename__="category"
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name= Column(String,unique=True)
    is_active=Column(Boolean,default=True,nullable=False)

    #relationship
    

    sub_categories=relationship(
        'SubCategory',
        back_populates='categories'
    )