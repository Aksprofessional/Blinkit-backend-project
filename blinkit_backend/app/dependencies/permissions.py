from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.models.user import User, User_role


def require_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != User_role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can perform this action",
        )

    return current_user
