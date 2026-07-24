from app.db.database import Base
from sqlalchemy import Column,String,UUID,ForeignKey,Boolean
from sqlalchemy.orm import relationship
import uuid


class SubCategory(Base):
    __tablename__='subcategory'
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name= Column(String,unique=True)
    category_id=Column(UUID,ForeignKey('category.id'),nullable=False)
    is_active=Column(Boolean,default=True,nullable=False)

    #relationship
    categories=relationship(
        'Category',
        back_populates='sub_categories'
    )

    product=relationship(
        'Products',
        back_populates='sub_categories'
    )

    collection_subcategories = relationship(
        "CollectionSubCategory",
        back_populates="subcategory"
    )