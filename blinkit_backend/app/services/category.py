from fastapi import HTTPException
from uuid import UUID
from app.repositories.collection import get_collection_user
from app.repositories.category import get_all_categories_user
from app.schemas.category import CategoryListResponse,CategoryResponse,SubCategoryResponse



# Retrieve categories, optionally filtered by a collection
def get_categories_service(
    db,
    collection: UUID | None,
):

    # Return all categories when no collection filter is provided
    if collection is None:

        # Fetch all categories from the repository
        categories = get_all_categories_user(db)

        # Build the response with active subcategories only
        return CategoryListResponse(
            categories=[
                CategoryResponse(
                    id=category.id,
                    name=category.name,
                    sub_categories=[
                        SubCategoryResponse(
                            id=sub.id,
                            name=sub.name,
                        )
                        for sub in category.sub_categories
                        if sub.is_active
                    ],
                )
                for category in categories
            ]
        )

    # Retrieve the specified collection
    collection_obj = get_collection_user(
        db=db,
        collection_id=collection,
    )

    # Raise an exception if the collection does not exist
    if collection_obj is None:
        raise HTTPException(
            status_code=404,
            detail="Collection not found.",
        )

    # Store categories while grouping their subcategories
    category_map = {}

    # Iterate through collection subcategories in display order
    for item in sorted(
        collection_obj.collection_subcategories,
        key=lambda x: x.display_order,
    ):

        # Retrieve the associated subcategory
        sub = item.subcategory

        # Skip inactive subcategories
        if not sub.is_active:
            continue

        # Retrieve the parent category
        category = sub.categories

        # Skip inactive categories
        if not category.is_active:
            continue

        # Create the category response if it has not been added yet
        if category.id not in category_map:
            category_map[category.id] = CategoryResponse(
                id=category.id,
                name=category.name,
                sub_categories=[],
            )

        # Add the subcategory to its parent category
        category_map[category.id].sub_categories.append(
            SubCategoryResponse(
                id=sub.id,
                name=sub.name,
            )
        )

    # Return the grouped categories and their subcategories
    return CategoryListResponse(
        categories=list(category_map.values())
    )