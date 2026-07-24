from fastapi import HTTPException

from app.repositories.collection import (
    get_all_categories,
    get_collection,
)

from app.schemas.category import (
    DiscoveryCategoryResponse,
    CategoryResponse,
    SubCategoryResponse,
)


def get_categories_service(
    db,
    collection: str | None,
):

    # Return all categories
    if collection is None:

        categories = get_all_categories(db)

        return DiscoveryCategoryResponse(
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

    # Return categories for a collection
    collection_obj = get_collection(
        db=db,
        collection=collection,
    )

    if collection_obj is None:
        raise HTTPException(
            status_code=404,
            detail="Collection not found.",
        )

    category_map = {}

    for item in sorted(
        collection_obj.collection_subcategories,
        key=lambda x: x.display_order,
    ):

        sub = item.subcategory

        if not sub.is_active:
            continue

        category = sub.categories

        if not category.is_active:
            continue

        if category.id not in category_map:

            category_map[category.id] = CategoryResponse(
                id=category.id,
                name=category.name,
                sub_categories=[],
            )

        category_map[category.id].sub_categories.append(
            SubCategoryResponse(
                id=sub.id,
                name=sub.name,
            )
        )

    return DiscoveryCategoryResponse(
        categories=list(category_map.values())
    )