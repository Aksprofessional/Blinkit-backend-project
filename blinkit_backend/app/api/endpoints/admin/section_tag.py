from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_admin
from app.db.database import get_db
from app.models.user import User
from app.services.admin.section import change_section_tag
from app.schemas.tag import SectionTagMappingRequest



router=APIRouter()

@router.put('/{section_id}/tags')
def add_tag_section_api(section_id: UUID, tag_data: SectionTagMappingRequest,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    require_admin(current_user)
    return change_section_tag(db,tag_data,section_id)

@router.get('/section_id/tags')


