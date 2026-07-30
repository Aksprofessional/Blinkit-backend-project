from pydantic import BaseModel,Field
from typing import Optional
from uuid import UUID
from decimal import Decimal



class SectionTagMapping(BaseModel):
    id: list[UUID] = Field(...,min_length=1)



class SectionTagMappingRequest(BaseModel):
    tags: list[SectionTagMapping] 