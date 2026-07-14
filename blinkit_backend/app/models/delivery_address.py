from sqlalchemy import Column,ForeignKey,UUID,String
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.user import User
import uuid

class delivery_address(Base):
    __tablename__='delivery_address'
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id=Column(UUID,ForeignKey('users.id'),nullable=False)
    address=Column(String,nullable=False)

    #relationship
    users=relationship(
        User,
        back_populates='delivery_addresses'
    )
