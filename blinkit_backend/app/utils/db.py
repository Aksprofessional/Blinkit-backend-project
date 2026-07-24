from sqlalchemy.orm import Session
from fastapi import HTTPException,status


def commit_or_500(db: Session, message: str):
    try:
        db.commit()
    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{message}.{e}"
        )