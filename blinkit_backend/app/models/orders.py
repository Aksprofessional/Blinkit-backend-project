from sqlalchemy import Column,ForeignKey,DECIMAL,UUID,func,DateTime,Enum
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid
from enum import Enum as pyEnum



class status(str,pyEnum):
    PENDING="pending"
    COMPLETE="complete"
    CANCELED="canceled"

class order(Base):
    __tablename__='orders'
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True),ForeignKey('users.id'),index=True,nullable=False)
    status=Column(Enum(status ,name='order_status'), nullable=False, default=status.PENDING)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    total_price=Column(DECIMAL(10,2),nullable=False)

    #relationship
    order_item=relationship(
        'order_items',
        back_populates='orders'
    )

    users=relationship(
        'User',
        back_populates='orders'
    )