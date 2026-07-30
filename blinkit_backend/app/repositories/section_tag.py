from uuid import UUID
from datetime import datetime, timezone
from fastapi import HTTPException, status,UploadFile
from sqlalchemy.orm import Session,joinedload
from typing import Optional 
from app.schemas.tag import SectionTagMapping


def create_section_tag_row(db,tag_id: UUID ,section_id: UUID, group_no: int):
    row={
        "section_id": section_id,
        "tag_id": tag_id,
        "group_no": group_no
    }
    return row
