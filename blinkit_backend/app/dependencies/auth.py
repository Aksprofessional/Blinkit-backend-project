from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import Setting
from app.db.database import get_db
from app.models.user import User

from app.exceptions.custom_exception import UnauthorizedException

#its just extracting token 
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"    #swagger knows to get a token call this
)

#to get current user
def get_current_user(
    token: str = Depends(oauth2_scheme),       #dependency injection that ,,fastapi looks at incoming request extract token from it.
    db: Session = Depends(get_db),
):

    #decoding the token
    try:
        payload = jwt.decode(
            token,
            Setting.SECRET_KEY,
            algorithms=[Setting.ALGORITHM],
        )
# extracting user id from parameter of token having sub.
        user_id = payload.get("sub")

        if payload.get("type") != "access":
            raise UnauthorizedException(
                    "Could not validate credentials"
                )

        if user_id is None:
            raise UnauthorizedException(
                    "Could not validate credentials"
                )

    except JWTError:
        raise UnauthorizedException(
                "Could not validate credentials"
            )

    user = db.get(User, UUID(user_id))

    if user is None or user.isdeleted:
        raise UnauthorizedException(
                "Could not validate credentials"
            )
    

    return user