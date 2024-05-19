from abc import abstractmethod
from typing import Optional
from uuid import UUID

from asyncpg import Pool

from repositories.order_repository import OrderRepository

from schemas.order import OrderDTO

from services import Service
from services.cart_service import CartService


class OrderService(Service):
    def __init__(
        self, repository: OrderRepository, cart_service: CartService, conn_pool: Pool
    ):
        self.repository: OrderRepository = repository
        self.cart_service: CartService = cart_service
        self.conn_pool = conn_pool

    @abstractmethod
    async def get_user_orders(self, user_id: UUID) -> list[OrderDTO]: ...

    @abstractmethod
    async def get_user_order_by_id(
        self, user_id: UUID, order_id: UUID
    ) -> Optional[OrderDTO]: ...

    @abstractmethod
    async def create_order_from_cart(self, user_id: UUID) -> Optional[OrderDTO]: ...

    @abstractmethod
    async def is_order_restaurant_admin(
        self, order_id: UUID, user_id: UUID
    ) -> bool: ...

    @abstractmethod
    async def complete_order(self, order_id: UUID, user_id: UUID) -> Optional[str]: ...


class OrderServiceImpl(OrderService):
    async def get_user_orders(self, user_id: UUID) -> list[OrderDTO]:
        async with self.conn_pool.acquire() as conn:
            return await self.repository.get_user_orders(user_id, conn)

    async def get_user_order_by_id(
        self, user_id: UUID, order_id: UUID
    ) -> Optional[OrderDTO]:
        async with self.conn_pool.acquire() as conn:
            if order := await self.repository.get_user_order_by_id(
                user_id, order_id, conn
            ):
                return order
            return None

    async def create_order_from_cart(self, user_id: UUID) -> Optional[OrderDTO]:
        async with self.conn_pool.acquire() as conn:
            if order := await self.repository.create_order_from_cart(user_id, conn):
                await self.cart_service.delete_active_cart_products(user_id)
                return OrderDTO.model_validate(order, from_attributes=True)
            return None

    async def is_order_restaurant_admin(self, order_id: UUID, user_id: UUID) -> bool:
        async with self.conn_pool.acquire() as conn:
            return await self.repository.is_order_restaurant_admin(
                order_id, user_id, conn
            )

    async def complete_order(self, order_id: UUID, user_id: UUID) -> Optional[str]:
        async with self.conn_pool.acquire() as conn:
            if await self.is_order_restaurant_admin(order_id, user_id):
                return await self.repository.complete_order(order_id, user_id, conn)
            return None