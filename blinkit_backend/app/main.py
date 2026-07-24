import app.models.user
import app.models.orders
import app.models.order_items
import app.models.products
import app.models.product_variant
import app.models.category
import app.models.cart
import app.models.cart_item
import app.models.delivery_address
import app.models.brand
import app.models.sub_category
import app.models.collection
import app.models.collection_subcategory
import app.models.collection
import app.models.collection_subcategory

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.endpoints.admin.category import (
    router as admin_category_router,
)
from app.api.endpoints.admin.brand import router as brand_router
from app.api.endpoints.admin.product import router as product_router
from app.api.endpoints.admin.sub_category import router as subcategory_router
from app.api.endpoints.admin.product_variant import router as product_variant_router
from app.api.endpoints.admin.collection import router as collection_router
from app.api.endpoints.admin.collection_subcategory import router as collection_subcategory_router


app = FastAPI(
    title="Blinkit Backend API"
)

app.include_router(auth_router)

app.include_router(
    admin_category_router,
    prefix="/admin"
)

app.include_router(
    brand_router,
    prefix="/admin"
)

app.include_router(
    product_router,
    prefix="/admin"
)

app.include_router(
    subcategory_router,
    prefix="/admin"
)

app.include_router(
    product_variant_router,
    prefix="/admin"
)

app.include_router(
    collection_router,
    prefix="/admin",
)

app.include_router(
    collection_subcategory_router,
    prefix="/admin",
)