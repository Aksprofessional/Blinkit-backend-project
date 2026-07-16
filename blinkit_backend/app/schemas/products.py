from fastapi import UploadFile,File,Form
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class AddProduct(BaseModel):
    id:  UUID
    name: str = Form(...)
    image: UploadFile = File(...)
    description: str = Form(...)


