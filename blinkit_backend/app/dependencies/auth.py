from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import Setting
from app.db.database import get_db
from app.models.user import User

#its just extracting token 
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"    #swagger knows to get a token call this
)

def get_current_user(
    token: str = Depends(oauth2_scheme),       #dependency injection that ,,fastapi looks at incoming request extract token from it.
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(     
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    #decoding the token
    try:
        payload = jwt.decode(
            token,
            Setting.SECRET_KEY,
            algorithms=[Setting.ALGORITHM],
        )
# extracting user id from parameter of token having sub.
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.get(User, UUID(user_id))

    if user is None or user.isdeleted:
        raise credentials_exception
    

    return user