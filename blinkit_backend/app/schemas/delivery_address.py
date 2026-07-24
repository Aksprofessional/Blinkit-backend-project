from pydantic import BaseModel,field_validator,ConfigDict
from typing import Optional
from uuid import UUID
from app.models.delivery_address import AddressType

class AddAddressResponse(BaseModel):
    id:  UUID
    user_id: UUID
    reciever_name: str
    address: str
    mobile_no: str
    pincode: int
    city: str
    state: str
    is_default: bool
    address_type: AddressType
    custom_address_type: Optional[str] = None

    @field_validator("mobile_no")
    @classmethod
    def validate_mobile_no(cls,value: int):
        if len(value)!=10:
            raise ValueError("Mobile number must be exactly 10 digits")
        return value

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls,value: int):
        if value < 100000 or value > 999999:
            raise ValueError("Pincode must be exactly 6 digits")
        return value
    
    model_config = ConfigDict(from_attributes=True)


class ListAddressModel(BaseModel):
    addresses: list[AddAddressResponse]


class AddAddress(BaseModel):
    reciever_name: str
    address: str
    mobile_no: str
    pincode: int
    city: str
    state: str
    address_type: AddressType
    custom_address_type: Optional[str] = None

    @field_validator("mobile_no")
    @classmethod
    def validate_mobile_no(cls,value: int):
        if len(value)!=10:
            raise ValueError("Mobile number must be exactly 10 digits")
        return value

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls,value: int):
        if value < 100000 or value > 999999:
            raise ValueError("Pincode must be exactly 6 digits")
        return value




class UpdateAddressModel(BaseModel):
    reciever_name: Optional[str] = None
    address: Optional[str] = None
    mobile_no: Optional[str] = None
    pincode: Optional[int] = None
    city: Optional[str] = None
    state: Optional[str] = None
    address_type: Optional[AddressType] = None
    custom_address_type: Optional[str] = None


    @field_validator("mobile_no")
    @classmethod
    def validate_mobile_no(cls,value: int):
        if value is None:
            return value
        if len(value)!=10:
            raise ValueError("Mobile number must be exactly 10 digits")
        return value

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls,value: int):
        if value is None:
            return value
        if value < 100000 or value > 999999:
            raise ValueError("Pincode must be exactly 6 digits")
        return value
    
    model_config = ConfigDict(from_attributes=True)


class AddressDefaultUpdate(BaseModel):
    id: UUID
    user_id: UUID
    is_default: bool
    
    model_config = ConfigDict(from_attributes=True)


class UpdateListAddressResponse(BaseModel):
    addresses: list[AddressDefaultUpdate]


