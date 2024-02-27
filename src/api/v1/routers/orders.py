from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends
from core.auth import get_user
from core.context import app_configuration
from schemas.order import OrderDTO
from schemas.user import User
from services.order_service import OrderService

router = APIRouter(tags=["orders"])


@router.get(
    "/orders",
    name="Get user orders",
)
async def get_user_orders(user: User = Depends(get_user)) -> list[OrderDTO]:
    return await app_configuration.get_service(OrderService).get_user_orders(user.id)


@router.get("/orders/{order_id}", name="Get user order by id")
async def get_user_order(
    order_id: UUID, user: User = Depends(get_user)
) -> OrderDTO | None:
    return await app_configuration.get_service(OrderService).get_user_order_by_id(
        user.id, order_id
    )


@router.post("/cart/create_order", name="Create order from cart")
async def create_order(user: User = Depends(get_user)) -> Optional[OrderDTO]:
    return await app_configuration.get_service(OrderService).create_order_from_cart(
        user.id
    )
