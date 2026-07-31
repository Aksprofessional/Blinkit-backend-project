from pydantic import BaseModel,Field,ConfigDict
from typing import Optional
from uuid import UUID
from decimal import Decimal



class SectionTagMapping(BaseModel):
    id: list[UUID] = Field(...,min_length=1)



class SectionTagMappingRequest(BaseModel):
    tags: list[SectionTagMapping] 



class SectionTagSchema(BaseModel):
    id: UUID
    tag_id: UUID
    group_no: int
    
    model_config = ConfigDict(from_attributes=True)



class SectionTagListResponse(BaseModel):
    tags: list[SectionTagSchema]
    section_id: UUID