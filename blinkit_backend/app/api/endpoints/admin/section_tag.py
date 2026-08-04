from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_admin
from app.db.database import get_db
from app.models.user import User
from app.services.admin.section_tag import change_section_tag
from app.schemas.tag import SectionTagMappingRequest
from app.services.admin.section_tag import get_section_tag_service

from app.schemas.section_tag import SectionTagListResponse

router=APIRouter()

@router.put('/{section_id}/tags')
def change_tag_section_api(section_id: UUID, tag_data: SectionTagMappingRequest,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    require_admin(current_user)
    return change_section_tag(db,tag_data,section_id)


@router.get('/{section_id}/tags')
def get_tag_section_api(section_id: UUID,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    require_admin(current_user)
    tag_with_group_no=get_section_tag_service(db,section_id)
    
    return SectionTagListResponse(
        tags=tag_with_group_no,
        section_id=section_id
    )

