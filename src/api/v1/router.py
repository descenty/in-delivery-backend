from fastapi import APIRouter

from .routers import categories

api_router = APIRouter()
api_router.include_router(
    menus_endpoints.router, prefix='/categories', tags=['categories']
)
# api_router.include_router(
#     submenus_endpoints.router, prefix='/menus', tags=['submenus']
# )
# api_router.include_router(
#     dishes_endpoints.router, prefix='/menus', tags=['dishes']
# )
