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


app = FastAPI(
    title="Blinkit Backend API"
)

app.include_router(auth_router)
app.include_router(cart_item.router, prefix='/api/cart-items')
app.include_router(delivery_addresses.router, prefix='/api/address')
