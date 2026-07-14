from app.db.database import Base
from sqlalchemy import Column,Integer,String,DateTime
from enum import Enum
class User_role(str,Enum):
    ADMIN="admin"
    CUSTOMER="customer"



class User(Base):
    __table_name__="users"

    id=Column(Integer, primary_key=True)
    name= Column(String)
    mail=Column(String, unique=True)
    hashed_password= Column(String)
    created_at= Column(DateTime)
    blinkit_money=Column(Integer,nullable=True)
    role= Column(Enum(User_role , name="user_role_enum"), nullable=False, default=User_role.CUSTOMER)


