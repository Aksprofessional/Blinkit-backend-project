from sqlalchemy.orm import Session
from fastapi import HTTPException,status


# Commit the current database transaction or raise an internal server error
def commit_or_500(db: Session, message: str):
    try:

        # Commit the transaction
        db.commit()

    except Exception as e:

        # Roll back the transaction if an error occurs
        db.rollback()

        # Raise an HTTP 500 error with the provided message
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{message}.{e}"
        )