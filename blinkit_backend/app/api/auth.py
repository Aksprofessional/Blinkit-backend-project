from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User, User_role
from app.schemas.user import UserRegister, UserResponse
from app.core.security import hash_password


from uuid import UUID
from jose import JWTError, jwt

from app.core.config import Setting
from app.schemas.user import RefreshTokenRequest

from app.schemas.user import UserLogin, Token
from app.core.security import verify_password, create_access_token, create_refresh_token,create_email_verification_token
from jose import JWTError, jwt

from app.utils.email import send_verification_email

from exceptions.custom_exception import UnauthorizedException, BadRequestException, NotFoundException

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    # Check if email already exists
    existing_user = db.query(User).filter(
        User.mail == user.mail
    ).first()

    if existing_user:
        raise BadRequestException(
        "Email already registered"
        )

    hashed_password = hash_password(
        user.password
    )

    new_user = User(
        name=user.name,
        mail=user.mail,
        hashed_password=hashed_password,
        role=User_role.CUSTOMER,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_email_verification_token(
        new_user.mail,
    )

    await send_verification_email(
        new_user.mail,
        token,
    )

    return {
        "message": "Registration successful. Please verify your email before logging in.",
    }




@router.post(
    "/login",
    response_model=Token
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    # Find user by email first 
    db_user = db.query(User).filter(
        User.mail == user.mail
    ).first()

    # if User not found
    if not db_user:
        raise UnauthorizedException()

    # check account status
    if db_user.isdeleted:
        raise HTTPException(
            status_code=403,
            detail="This account has been deleted."
        )

    if not db_user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Please verify your email before logging in."
        )

    if not db_user.is_active:
        raise HTTPException(
            status_code=403,
            detail="This account has been disabled by admin."
        )

    # Verify password
    if not verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT
    access_token = create_access_token(
        str(db_user.id)
    )

    refresh_token = create_refresh_token(
        str(db_user.id)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }









@router.post("/refresh")
def refresh_access_token(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(
            token_data.refresh_token,
            Setting.SECRET_KEY,
            algorithms=[Setting.ALGORITHM],
        )

        if payload.get("type") != "refresh":
            raise UnauthorizedException()

        user_id = payload.get("sub")

        if user_id is None:
            raise UnauthorizedException()

    except JWTError:
        raise UnauthorizedException()

    user = db.get(
        User,
        UUID(user_id),
    )

    if (
        user is None
        or user.isdeleted
        or not user.is_active
    ):
        raise UnauthorizedException()

    access_token = create_access_token(
        str(user.id),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }







@router.get("/verify-email")
def verify_email(
    token: str,
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(
            token,
            Setting.SECRET_KEY,
            algorithms=[Setting.ALGORITHM],
        )

        if payload.get("type") != "verify":
            raise HTTPException(
                status_code=400,
                detail="Invalid token",
            )

        email = payload.get("sub")

    except JWTError:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired token.",
        )

    user = db.query(User).filter(
        User.mail == email
    ).first()

    if not user:
        raise NotFoundException(
            "User not found."
        )

    user.is_verified = True

    db.commit()

    return {
        "message": "Email verified successfully."
    }