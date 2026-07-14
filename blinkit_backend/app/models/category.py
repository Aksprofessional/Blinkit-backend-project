from app.db.database import Base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship
from app.models.products import Products

class Category(Base):
    __tablename__="category"
    id=Column(Integer, primary_key=True)
    name= Column(String,unique=True)

    #relationship
    products= relationship(
        Products,
        back_populates='category'
    )