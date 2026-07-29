from pydantic import BaseModel, Field
from uuid import UUID



class MainCategoryCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    collection_id: UUID

    display_order: int = 0


class MainCategoryUpdate(BaseModel):
    name: str | None = None

    collection_id: UUID | None = None

    display_order: int | None = None

    is_active: bool | None = None


class MainCategoryResponse(BaseModel):
    id: UUID
    name: str
    collection_id: UUID
    display_order: int
    is_active: bool

    model_config = {
        "from_attributes": True
    }