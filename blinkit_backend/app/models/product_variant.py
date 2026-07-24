from sqlalchemy import Column,ForeignKey,UUID,Integer,DECIMAL,Boolean,String,DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid


class product_variant(Base):
    __tablename__='product_variant'
    id= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id=Column(UUID(as_uuid=True), ForeignKey('products.id'),nullable=False)
    sku= Column(String,nullable=False,unique=True)
    price= Column(DECIMAL(10,2),nullable=False)
    stock_quantity= Column(Integer,nullable=False)
    isdeleted= Column(Boolean,default=False,nullable=False)
    variant_name=Column(String,nullable=False,default='STANDARD')
    delete_timestamp=Column(DateTime(timezone=True),nullable=True)

    #relationship
    product=relationship(
        'Products',
        back_populates='product_variants'
    )
    cart_items=relationship(
        'CartItem',
        back_populates='product_variants',
        )
    order_item=relationship(
        'order_items',
        back_populates='product_variants'
    )
    