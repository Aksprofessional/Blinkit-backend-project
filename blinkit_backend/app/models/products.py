from sqlalchemy import Column,Integer,UUID,String, Float,ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship
from app.models.category import Category
from app.models.order_items import order_product
import uuid

class Products(Base):
    __tablename__="products"
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name= Column(String, unique=True)
    price= Column(Float,nullable=False)
    stock_quantity= Column(Integer,nullable=False)
    image= Column(String,nullable=False)
    description= Column(String)
    category_id= Column(Integer, ForeignKey('category.id'),nullable=False)

    #relationship
    category= relationship(
        Category,
        back_populates='products'
    )

    order_items=relationship(
        order_product,
        back_populates='products'
    )
