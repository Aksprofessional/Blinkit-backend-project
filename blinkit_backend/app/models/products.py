from sqlalchemy import Column,UUID,String,ForeignKey,Boolean,DateTime
from app.db.database import Base
from sqlalchemy.orm import relationship
import uuid

class Products(Base):
    __tablename__="products"
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name= Column(String, unique=True)
    image= Column(String,nullable=False)
    description= Column(String)
    brand_id= Column(UUID(as_uuid=True),ForeignKey('brands.id'),nullable=False)
    sub_category_id= Column(UUID(as_uuid=True), ForeignKey('subcategory.id'),nullable=False)
    isdeleted= Column(Boolean,default=False,nullable=False)
    delete_timestamp=Column(DateTime(timezone=True),nullable=True)


    

    #relationship
    sub_categories= relationship(
        'SubCategory',
        back_populates='product'
    )

    product_variants=relationship(
        'product_variant',
        back_populates='product'
    )

    brand=relationship(
        'brand',
        back_populates='product'
    )
