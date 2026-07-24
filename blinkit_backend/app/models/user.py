from app.db.database import Base
from sqlalchemy import Column,Integer,String,DateTime,Enum,UUID,func,Boolean
from enum import Enum as pyEnum
from sqlalchemy.orm import relationship

import uuid
class User_role(str,pyEnum):
    ADMIN="admin"
    CUSTOMER="customer"



class User(Base):
    __tablename__="users"

    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name= Column(String,nullable=False)
    mail=Column(String, unique=True,nullable=False)
    hashed_password= Column(String,nullable=False)
    created_at= Column(DateTime,server_default=func.now())
    blinkit_money=Column(Integer,nullable=True)
    role= Column(Enum(User_role , name="user_role_enum"), nullable=False, default=User_role.CUSTOMER)
    isdeleted= Column(Boolean,default=False,nullable=False)
    delete_timestamp=Column(DateTime(timezone=True),nullable=True)
    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    #ralationship
    orders = relationship(
        'order',
        back_populates='users',
    )

    delivery_addresses=relationship(
        'delivery_address',
        back_populates='users',
    )
    cart=relationship(
        'Cart',
        back_populates='users',
    )
