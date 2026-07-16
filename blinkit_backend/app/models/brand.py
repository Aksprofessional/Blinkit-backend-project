from sqlalchemy import Column,ForeignKey,UUID,Integer,DECIMAL,Boolean,String,DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid


class brand(Base):
    __tablename__='brands'
    id= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    is_active= Column(Boolean,default=True,nullable=False)
    name= Column(String,nullable=False)
    logo= Column(String, nullable=True)


    #relationship
    product=relationship(
        'Products',
        back_populates='brand'
    )