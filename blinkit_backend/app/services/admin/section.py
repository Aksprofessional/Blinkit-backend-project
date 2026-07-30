from sqlalchemy.orm import Session
from app.schemas.tag import SectionTagMappingRequest
from uuid import UUID
from sqlalchemy import insert
from app.repositories.section import get_section_by_id,section_tag_mapping_delete
from app.repositories.tag import get_all_tag_by_id
from app.repositories.section_tag import create_section_tag_row
from app.models.section_tag import SectionTag
from app.models.user import User
from fastapi import HTTPException,status
from app.utils.db import commit_or_500
from app.schemas.section import SectionCreate
from app.repositories.collection import get_collection_by_id
from app.repositories.section import create_section
from app.repositories.tag import get_all_tag_by_id


# def add_section_service(db: Session, section_data: SectionCreate):
#     get_collection_by_id(db,section_data.collection_id)
#     db_section=create_section(db,section_data)
#     if section_data.tags:
#         tag_ids=section_data.tags
#         get_all_tag_by_id(db,tag_ids)
#         for id in tag_ids


def change_section_tag(db: Session, tag_data: SectionTagMappingRequest, section_id: UUID):
    db_section=get_section_by_id(db,section_id)
    tag_ids={id 
             for tags in tag_data.tags
             for id in tags.tag_id}
    get_all_tag_by_id(db,tag_ids)
    section_tag_mapping_delete(db,section_id)
    group_no=1
    rows=[]
    for tag_group in tag_data.tags:
        for tag_id in tag_group:
            rows.append(create_section_tag_row(db,tag_id,section_id,group_no))
        group_no+=1

    db.execute(insert(SectionTag),rows)
    commit_or_500(db,"could not add tags to section")
    return{
        "message":"tags added succesfully to section"
    }





