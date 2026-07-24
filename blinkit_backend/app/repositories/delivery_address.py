from sqlalchemy.orm import Session
from app.models.delivery_address import delivery_address,AddressType
from fastapi import HTTPException, status
from uuid import UUID
from app.schemas.delivery_address import AddAddress,UpdateAddressModel

def delivery_address_exists(db: Session, address: AddAddress,current_user_id: UUID):
    addresses=db.query(delivery_address).filter(delivery_address.address==address.address,
                                                delivery_address.user_id==current_user_id,
                                                delivery_address.city==address.city,
                                                delivery_address.state==address.state,
                                                delivery_address.pincode==address.pincode,).first()
    if addresses:
        raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='address already exists'
                )
    return 


def add_address(db: Session, address: AddAddress,current_user_id: UUID,first_address: bool):
    
    

    addresses=delivery_address(
        reciever_name=address.reciever_name,
        mobile_no=address.mobile_no,
        user_id=current_user_id,
        address=address.address,
        is_default= first_address,
        city=address.city,
        state=address.state,
        pincode=address.pincode,
        address_type = address.address_type,
        custom_address_type = address.custom_address_type
    )
        

        
    db.add(addresses)
    return addresses



def get_address_all(db: Session,current_user_id: UUID):
    addresses=db.query(delivery_address).filter(delivery_address.user_id==current_user_id).order_by(delivery_address.is_default.desc(),delivery_address.created_at.desc(),delivery_address.id.desc()).all()
    return addresses


def get_address_by_id(db: Session,address_id: UUID,current_user_id: UUID):
    address=db.query(delivery_address).filter(delivery_address.id==address_id,delivery_address.user_id==current_user_id).first()
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='address id with the current user does not exist.'
        )
    return address

def check_address_first_by_user(db: Session,current_user_id: UUID):
    user_address_exist=db.query(delivery_address).filter(delivery_address.user_id==current_user_id).first() is None
    return user_address_exist

def get_current_default_address_user(db: Session,current_user_id: UUID):
    user_address=db.query(delivery_address).filter(delivery_address.user_id==current_user_id,delivery_address.is_default==True).first()
    if user_address is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='user has no default as address.please contact admin.'
        )
    return user_address


def update_current_default_address_user_to_false(db: Session,current_user_id: UUID):
    row_updated=db.query(delivery_address).filter(delivery_address.user_id==current_user_id,delivery_address.is_default==True).update(
        {delivery_address.is_default: False},
        synchronize_session=False
    )
    db.flush()
    return row_updated



def delivery_address_exists_model_address(db: Session, address: delivery_address,current_user_id: UUID):
    addresses=db.query(delivery_address).filter(delivery_address.address==address.address,
                                                delivery_address.user_id==current_user_id,
                                                delivery_address.city==address.city,
                                                delivery_address.state==address.state,
                                                delivery_address.pincode==address.pincode,
                                                delivery_address.id != address.id).first()
    
    if addresses:
        raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='address already exists with the same information.cannot be updated.'
                )
    return 

