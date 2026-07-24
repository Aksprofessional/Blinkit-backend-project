#for user to delete its own account



from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.dependencies.auth import get_current_user

from app.models.user import User

from app.repositories.user import delete_user

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.delete("/me")
def delete_my_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_user(
        db,
        current_user,
    )