from typing import Optional
from uuid import UUID
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from sqlalchemy import or_

from app.models.user import User


def get_all_users(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
):
    query = db.query(User)

    if search:
        query = query.filter(
            or_(
                User.name.ilike(f"%{search}%"),
                User.mail.ilike(f"%{search}%"),
            )
        )

    total = query.count()

    users = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "data": users,
    }





def get_user_by_id(
    db: Session,
    user_id: UUID,
):
    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user





def disable_user(
    db: Session,
    user: User,
):
    user.is_active = False

    db.commit()
    db.refresh(user)

    return user









def enable_user(
    db: Session,
    user: User,
):
    user.is_active = True

    db.commit()
    db.refresh(user)

    return user







def delete_user(
    db: Session,
    user: User,
):
    user.isdeleted = True
    user.delete_timestamp = datetime.now(
        timezone.utc
    )

    db.commit()
    db.refresh(user)

    return {
        "message": "User deleted successfully."
    }