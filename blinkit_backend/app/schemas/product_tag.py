from uuid import UUID

from pydantic import BaseModel


class ProductTagCreate(BaseModel):
    product_id: UUID
    tag_id: UUID


class ProductTagResponse(BaseModel):
    id: UUID
    product_id: UUID
    tag_id: UUID

    model_config = {
        "from_attributes": True
    }