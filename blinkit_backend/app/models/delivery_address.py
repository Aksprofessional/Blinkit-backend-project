from sqlalchemy import Column,ForeignKey,UUID,String,Boolean,UniqueConstraint,Index,text,Integer,CheckConstraint,Enum,DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid
from enum import Enum as pyEnum

class AddressType(str,pyEnum):
    HOME="home"
    WORK="work"
    HOSTEL="hostel"
    OTHER="other"


class delivery_address(Base):
    __tablename__='delivery_address'
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True),ForeignKey('users.id'),nullable=False)
    reciever_name=Column(String,nullable=False)
    address=Column(String,nullable=False)
    mobile_no=Column(Integer,nullable=False)
    pincode=Column(Integer,nullable=False)
    city=Column(String,nullable=False)
    state=Column(String,nullable=False)
    is_default=Column(Boolean,nullable=False,default=False)
    address_type= Column(Enum(AddressType , name="address_type_enum"), nullable=False, default=AddressType.HOME)
    custom_address_type = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())



    #relationship
    users=relationship(
        'User',
        back_populates='delivery_addresses'
    )
    __table_args__ = (
        CheckConstraint(
            "mobile_no BETWEEN 1000000000 AND 9999999999 "
            "AND pincode BETWEEN 100000 AND 999999",
            name="ck_mobile_pincode",
        ),
        
        Index(
            "ix_one_default_address",
            "user_id",
            unique=True,
            postgresql_where=text("is_default = true"),
        ),
            UniqueConstraint(
                "user_id",
                "address",
                "pincode",
                "state",
                "city",
                name="uq_user_address"
            ),
        )
