from fastapi import APIRouter

from .routers.auth import router as auth_router
from .routers.categories import router as categories_router
from .routers.products import router as products_router
from .routers.cart import router as cart_router
from .routers.addresses import router as addresses_router
from .routers.customer import router as customer_router
from .routers.orders import router as orders_router
from .routers.restaurants import router as restaurants_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(categories_router, prefix="/categories", tags=["categories"])
api_router.include_router(products_router, prefix="/products", tags=["products"])
api_router.include_router(cart_router, tags=["cart"])
api_router.include_router(addresses_router, tags=["addresses"])
api_router.include_router(customer_router, tags=["customer"])
api_router.include_router(orders_router, tags=["orders"])
api_router.include_router(restaurants_router, prefix="/restaurants", tags=["restaurants"])
