from uuid import UUID

from pydantic import BaseModel, Field


class TagCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )


class TagUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )


class TagResponse(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True
    }