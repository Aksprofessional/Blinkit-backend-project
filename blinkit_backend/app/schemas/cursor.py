from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CursorResponse(BaseModel):
    cursor: str 
