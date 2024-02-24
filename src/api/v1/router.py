from fastapi import APIRouter

from .routers.auth import router as auth_router
from .routers.categories import router as categories_router
from .routers.products import router as products_router
from .routers.cart import router as cart_router
from .routers.geo import router as geo_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(categories_router, prefix="/categories", tags=["categories"])
api_router.include_router(products_router, prefix="/products", tags=["products"])
api_router.include_router(cart_router, tags=["cart"])
api_router.include_router(geo_router, prefix="/geo", tags=["geo"])
