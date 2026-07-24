from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.collection import get_all_collection_customer



def get_all_collection(db: Session):
    collection=get_all_collection_customer(db)
    return collection


from sqlalchemy.orm import Session, selectinload

from app.models.category import Category
from app.models.collection import Collection
from app.models.collection_subcategory import CollectionSubCategory
from app.models.sub_category import SubCategory


def get_all_categories(db: Session):
    return (
        db.query(Category)
        .options(
            selectinload(Category.sub_categories)
        )
        .filter(
            Category.is_active.is_(True)
        )
        .all()
    )


def get_collection(
    db: Session,
    collection: str,
):
    return (
        db.query(Collection)
        .options(
            selectinload(Collection.collection_subcategories)
            .selectinload(CollectionSubCategory.subcategory)
            .selectinload(SubCategory.categories)
        )
        .filter(
            Collection.name == collection,
            Collection.is_active.is_(True),
        )
        .first()
    )