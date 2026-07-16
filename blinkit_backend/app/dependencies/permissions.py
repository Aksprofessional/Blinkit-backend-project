from app.models.user import User,User_role
from fastapi import HTTPException

def require_admin(current_user: User):
    if current_user.role == User_role.ADMIN:
        return current_user
    raise HTTPException(status_code=403, detail='only admins can perform this action')
    
