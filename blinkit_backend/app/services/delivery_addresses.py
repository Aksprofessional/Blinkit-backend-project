from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.delivery_address import delivery_address_exists,add_address,get_address_all,get_address_by_id,check_address_first_by_user,update_current_default_address_user_to_false,delivery_address_exists_model_address
from app.utils.db import commit_or_500
from app.schemas.delivery_address import AddAddress,UpdateAddressModel
from uuid import UUID
from fastapi import HTTPException, status
from app.models.delivery_address import AddressType


# Add a new delivery address for the authenticated user
def add_delivery_address(db: Session,current_user: User,delivery_address: AddAddress):

    # Ensure the same address does not already exist
    delivery_address_exists(db,delivery_address,current_user.id)

    # Check whether this is the user's first address
    first_address=check_address_first_by_user(db,current_user.id)

    # Validate custom address type for OTHER addresses
    if delivery_address.address_type == AddressType.OTHER:
        if not delivery_address.custom_address_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="custom_address_type is required when address_type is OTHER."
            )

    # Ensure custom address type is not provided for predefined address types
    else:
        if delivery_address.custom_address_type is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="custom_address_type must be null unless address_type is OTHER."
            )

    # Create the delivery address
    address=add_address(db,delivery_address,current_user.id,first_address)

    # Commit the transaction
    message='delivery address could not be added'
    commit_or_500(db,message)

    return address


# Retrieve all delivery addresses for the authenticated user
def get_delivery_address(db: Session,current_user_id: UUID):

    # Fetch all delivery addresses
    addresses=get_address_all(db,current_user_id)

    return addresses



# Retrieve a delivery address by its id
def get_delivery_address_by_id(db: Session,current_user_id: UUID, address_id: UUID):

    # Fetch the requested delivery address
    address=get_address_by_id(db,address_id,current_user_id)

    return address

    


# Update an existing delivery address
def update_delivery_address(db: Session,current_user: User,delivery_address: UpdateAddressModel,address_id: UUID):

    # Retrieve the delivery address to update
    address=get_address_by_id(db,address_id,current_user.id)

    # Validate custom address type for OTHER addresses
    if delivery_address.address_type == AddressType.OTHER:
        if not delivery_address.custom_address_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="custom_address_type is required when address_type is OTHER."
            )

    # Ensure custom address type is not provided for predefined address types
    else:
        if delivery_address.custom_address_type is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="custom_address_type must be null unless address_type is OTHER."
            )

    # Extract only the fields provided in the request
    updated_data=delivery_address.model_dump(exclude_unset=True)

    # Track whether any field has changed
    changed= False

    # Update only modified fields
    for field, value in updated_data.items():
        if getattr(address, field) != value:
            changed = True
            setattr(address,field,value)

    # Reject the request if no changes were made
    if not changed:
        raise HTTPException(
            status_code=400,
            detail="No changes detected."
        )

    # Ensure the updated address does not duplicate another address
    delivery_address_exists_model_address(db,address,current_user.id)

    # Commit the transaction
    message='delivery address could not be updated'
    commit_or_500(db,message)

    return address



# Update the user's default delivery address
def update_delivery_address_default(db: Session,current_user: User,address_id: UUID):

    # Retrieve the selected address
    address_new=get_address_by_id(db,address_id,current_user.id)

    # Return immediately if it is already the default address
    if address_new.is_default:
        return address_new

    # Remove the default flag from the current default address
    row_updated=update_current_default_address_user_to_false(db,current_user.id)

    # Mark the selected address as the new default
    address_new.is_default= True

    # Commit the transaction
    message='delivery address default could not be updated'
    commit_or_500(db,message)

    return address_new

        
# Delete a delivery address
def delete_delivery_address(db: Session,current_user: User,address_id: UUID):

    # Retrieve the delivery address
    address=get_address_by_id(db,address_id,current_user.id)

    # Prevent deletion of the default address
    if address.is_default:
        raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='the default address can not be deleted.choose another default for address to delete the current address.'
                )

    # Delete the address
    db.delete(address)

    # Commit the transaction
    message='delivery address could not be deleted'
    commit_or_500(db,message)

    return address