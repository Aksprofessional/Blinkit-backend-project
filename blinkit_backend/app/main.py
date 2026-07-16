import app.models.user
import app.models.orders
import app.models.order_items
import app.models.products
import app.models.product_variant
import app.models.category
import app.models.cart
import app.models.cart_item
import app.models.delivery_address
from fastapi import FastAPI

from app.api.auth import router as auth_router


app = FastAPI(
    title="Blinkit Backend API"
)

app.include_router(auth_router)