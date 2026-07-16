from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    mail: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    mail: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: UUID
    name: str
    mail: EmailStr

    model_config = {
        "from_attributes": True
    }