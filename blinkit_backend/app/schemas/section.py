from uuid import UUID

from pydantic import BaseModel, Field


class SectionCreate(BaseModel):
    title: str = Field(..., min_length=2)
    display_order: int = 0
    collection_id: UUID


class SectionUpdate(BaseModel):
    title: str | None = None
    display_order: int | None = None
    is_active: bool | None = None


class SectionResponse(BaseModel):
    id: UUID
    title: str
    display_order: int

    model_config = {
        "from_attributes": True
    }