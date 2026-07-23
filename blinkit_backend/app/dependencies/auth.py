from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import Setting
from app.db.database import get_db
from app.models.user import User

# It's just extracting the token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"  # Swagger knows to call this endpoint to get a token
)


def get_current_user(
    token: str = Depends(oauth2_scheme),  # FastAPI extracts the token from the request
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    # Decode the token
    try:
        payload = jwt.decode(
            token,
            Setting.SECRET_KEY,
            algorithms=[Setting.ALGORITHM],
        )

        # Extract user ID from the "sub" claim
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.get(User, UUID(user_id))

    if user is None or user.isdeleted:
        raise credentials_exception

    return user