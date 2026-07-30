from app.db.database import Base
from sqlalchemy import Column,String,UUID,Boolean
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy import ForeignKey

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

    main_category = relationship(
        "MainCategory",
        back_populates="categories",
    )

    main_category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("main_categories.id"),
        nullable=False,
    )