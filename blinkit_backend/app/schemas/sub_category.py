from pydantic import BaseModel



class SubCategoryCreate(BaseModel):
    name: str
    is_active: bool = True