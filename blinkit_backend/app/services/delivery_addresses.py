from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.delivery_address import delivery_address_exists,add_address,get_address_all,get_address_by_id,check_address_first_by_user,update_current_default_address_user_to_false,delivery_address_exists_model_address
from app.utils.db import commit_or_500
from app.schemas.delivery_address import AddAddress,UpdateAddressModel
from uuid import UUID
from fastapi import HTTPException, status
from app.models.delivery_address import AddressType


def add_delivery_address(db: Session,current_user: User,delivery_address: AddAddress):
    delivery_address_exists(db,delivery_address,current_user.id)      
    first_address=check_address_first_by_user(db,current_user.id)
    if delivery_address.address_type == AddressType.OTHER:
        if not delivery_address.custom_address_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="custom_address_type is required when address_type is OTHER."
            )
    else:
        if delivery_address.custom_address_type is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="custom_address_type must be null unless address_type is OTHER."
            )
    address=add_address(db,delivery_address,current_user.id,first_address)
    message='delivery address could not be added'
    commit_or_500(db,message)
    return address


def get_delivery_address(db: Session,current_user_id: UUID):
    addresses=get_address_all(db,current_user_id)

    return addresses



def get_delivery_address_by_id(db: Session,current_user_id: UUID, address_id: UUID):
    address=get_address_by_id(db,address_id,current_user_id)

    return address

    


def update_delivery_address(db: Session,current_user: User,delivery_address: UpdateAddressModel,address_id: UUID):
    address=get_address_by_id(db,address_id,current_user.id)
    if delivery_address.address_type == AddressType.OTHER:
        if not delivery_address.custom_address_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="custom_address_type is required when address_type is OTHER."
            )
    else:
        if delivery_address.custom_address_type is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="custom_address_type must be null unless address_type is OTHER."
            )
    
    updated_data=delivery_address.model_dump(exclude_unset=True)
    changed= False
    for field, value in updated_data.items():
        if getattr(address, field) != value:
            changed = True
            setattr(address,field,value)
    if not changed:
        raise HTTPException(
            status_code=400,
            detail="No changes detected."
        )
    delivery_address_exists_model_address(db,address,current_user.id)
    message='delivery address could not be updated'
    commit_or_500(db,message)
    return address



def update_delivery_address_default(db: Session,current_user: User,address_id: UUID):

    address_new=get_address_by_id(db,address_id,current_user.id)
    if address_new.is_default:
        return address_new

    
    row_updated=update_current_default_address_user_to_false(db,current_user.id)
    
    address_new.is_default= True

    message='delivery address default could not be updated'
    commit_or_500(db,message)
    
    return address_new

        
def delete_delivery_address(db: Session,current_user: User,address_id: UUID):
    address=get_address_by_id(db,address_id,current_user.id)
    if address.is_default:
        raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='the default address can not be deleted.choose another default for address to delete the current address.'
                )
    db.delete(address)
    message='delivery address could not be deleted'
    commit_or_500(db,message)
    return address
