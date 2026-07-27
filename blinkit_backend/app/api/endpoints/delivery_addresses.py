from fastapi import APIRouter,Depends,Body
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.services.delivery_addresses import add_delivery_address,get_delivery_address,update_delivery_address,update_delivery_address_default,delete_delivery_address,get_delivery_address_by_id
from app.schemas.delivery_address import AddAddressResponse,ListAddressModel,AddAddress,UpdateAddressModel,AddressDefaultUpdate
from uuid import UUID



router=APIRouter()

# Add a new delivery address for the authenticated user
@router.post('/add',response_model=AddAddressResponse)
def add_delivery_address_api(delivery_address: AddAddress, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    # Create a new delivery address
    address=add_delivery_address(db,current_user,delivery_address)
    return address



# Retrieve a specific delivery address by its id
@router.get('/{address_id}',response_model=AddAddressResponse)
def get_delivery_address_api(address_id: UUID, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    # Fetch the requested delivery address
    delivery_address=get_delivery_address_by_id(db,current_user.id,address_id)
    return delivery_address


# Retrieve all delivery addresses for the authenticated user
@router.get('',response_model=ListAddressModel)
def get_delivery_address_all_api(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    # Fetch all delivery addresses associated with the user
    addresses=get_delivery_address(db,current_user.id)
    return ListAddressModel(addresses=addresses)


# Update an existing delivery address
@router.patch('/update/{address_id}',response_model=AddAddressResponse)
def update_delivery_address_api(address_id:UUID,delivery_address: UpdateAddressModel,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    # Update the specified delivery address
    address=update_delivery_address(db,current_user,delivery_address,address_id)
    return address


# Mark a delivery address as the default address
@router.patch('/default/{address_id}',response_model= AddressDefaultUpdate)
def update_delivery_address_default_api(address_id:UUID,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    # Update the user's default delivery address
    addresses=update_delivery_address_default(db,current_user,address_id)
    return addresses


# Delete a delivery address
@router.delete('/delete/{address_id}')
def delete_address_api(address_id:UUID,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    # Remove the specified delivery address
    address=delete_delivery_address(db,current_user,address_id)
    return {
        "id":address.id,
        "user_id":address.user_id,
        "removed":True,
        "message":"address is removed"
    }