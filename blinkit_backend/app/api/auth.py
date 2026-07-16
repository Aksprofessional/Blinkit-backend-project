from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User, User_role
from app.schemas.user import UserRegister, UserResponse
from app.core.security import hash_password

from app.schemas.user import UserLogin, Token
from app.core.security import verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    # Checking if email already exists,, aslo the first match
    existing_user = db.query(User).filter(
        User.mail == user.mail
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    # Create user object just a python object
    new_user = User(
        name=user.name,
        mail=user.mail,
        hashed_password=hashed_password,
        role=User_role.CUSTOMER
    )

    # adding to database
    db.add(new_user)
    # now in db
    db.commit()
    #now id is created by postgreql so refresh updates that in our python object
    db.refresh(new_user)

    return new_user

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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
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

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }