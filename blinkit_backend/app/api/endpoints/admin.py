from fastapi import APIRouter,Depends,HTTPException,Body,Request,status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.products import Products
from app.models.product_variant import product_variant
from app.models.category import Category
from app.models.sub_category import SubCategory
from app.schemas.category import CategoryCreate
from app.schemas.sub_category import SubCategoryCreate
from app.schemas.products import AddProduct
from app.db.database import get_db
from app.dependencies.permissions import require_admin
from app.repositories.category import get_category_by_id, get_category_by_name,add_category
from uuid import UUID
router=APIRouter()


#admin products adding
@router.post('/add-category', response_model=CategoryCreate,dependencies=[Depends(require_admin)])
def add_category_api(
    category_data: CategoryCreate, request: Request, db: Session = Depends(get_db)

):
    category_exists=get_category_by_name(category_data.name)
    if category_exists:
        raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="category already exists"
                )
    db_category=add_category(db,category_data)
    return db_category


