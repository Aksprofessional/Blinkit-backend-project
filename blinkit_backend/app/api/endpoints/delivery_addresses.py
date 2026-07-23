from fastapi import APIRouter,Depends,Body
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.services.delivery_addresses import add_delivery_address,get_delivery_address,update_delivery_address,update_delivery_address_default,delete_delivery_address,get_delivery_address_by_id
from app.schemas.delivery_address import AddAddressResponse,ListAddressModel,AddAddress,UpdateAddressModel,UpdateListAddressResponse,AddressDefaultUpdate
from uuid import UUID



router=APIRouter()

@router.post('/add',response_model=AddAddressResponse)
def add_delivery_address_api(delivery_address: AddAddress, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    address=add_delivery_address(db,current_user,delivery_address)
    return address



@router.get('/{address_id}',response_model=AddAddressResponse)
def get_delivery_address_api(address_id: UUID, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    delivery_address=get_delivery_address_by_id(db,current_user.id,address_id)
    return delivery_address


@router.get('',response_model=ListAddressModel)
def get_delivery_address_all_api(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    addresses=get_delivery_address(db,current_user.id)
    return ListAddressModel(addresses=addresses)


@router.patch('/update/{address_id}',response_model=AddAddressResponse)
def update_delivery_address_api(address_id:UUID,delivery_address: UpdateAddressModel,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    address=update_delivery_address(db,current_user,delivery_address,address_id)
    return address


@router.patch('/default/{address_id}',response_model= AddressDefaultUpdate)
def update_delivery_address_default_api(address_id:UUID,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    addresses=update_delivery_address_default(db,current_user,address_id)
    return addresses


@router.delete('/delete/{address_id}')
def delete_address_api(address_id:UUID,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    address=delete_delivery_address(db,current_user,address_id)
    return {
        "id":address.id,
        "user_id":address.user_id,
        "removed":True,
        "message":"address is removed"
    }

