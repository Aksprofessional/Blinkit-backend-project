from app.models.user import User,User_role
from fastapi import HTTPException,status
from app.models.user import User
from app.models.product_variant import product_variant

def require_admin(current_user: User):
    if current_user.role == User_role.ADMIN:
        return current_user
    raise HTTPException(status_code=403, detail='only admins can perform this action')
    

def check_user_is_deleted(current_user: User):
    if current_user.isdeleted:
            raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="user not found"
                    )
    return
    



