from app.db.database import Base
from sqlalchemy import Column,Integer,String,DateTime,Enum,UUID,func
from enum import Enum as pyEnum
from sqlalchemy.orm import relationship
import uuid
from app.models.orders import order
class User_role(str,pyEnum):
    ADMIN="admin"
    CUSTOMER="customer"



class User(Base):
    __tablename__="users"

    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name= Column(String,nullable=False)
    mail=Column(String, unique=True,nullable=False)
    hashed_password= Column(String,nullable=False)
    created_at= Column(DateTime,server_default=func.nowa())
    blinkit_money=Column(Integer,nullable=True)
    role= Column(Enum(User_role , name="user_role_enum"), nullable=False, default=User_role.CUSTOMER)

    #ralationship
    orders=relationship(
        order,
        back_populates='users'
    )
