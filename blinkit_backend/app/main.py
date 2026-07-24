from app.models.user import User
from app.models.category import Category
from app.models.sub_category import SubCategory
from app.models.products import Products
from app.models.brand import brand
from app.models.product_variant import product_variant
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.orders import Order
from app.models.order_items import order_items
from app.models.delivery_address import delivery_address
from app.models.collection import Collection
from app.models.collection_subcategory import CollectionSubCategory
from app.api.endpoints import cart_item,delivery_addresses,orders
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
from app.api.endpoints.admin.user import router as admin_user_router

from app.api.endpoints.user1 import router as user_router


app = FastAPI(
    title="Blinkit Backend API"
)

app.include_router(auth_router)
app.include_router(cart_item.router, prefix='/api/cart-items')
app.include_router(delivery_addresses.router, prefix='/api/address')
app.include_router(orders.router, prefix='/api/order')

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

app.include_router(
    admin_user_router,
    prefix="/admin",
)

app.include_router(
    user_router,
)
