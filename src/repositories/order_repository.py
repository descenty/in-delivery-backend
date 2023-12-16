from abc import abstractmethod
from typing import Optional
from uuid import UUID
from asyncpg import Record
from asyncpg.pool import PoolConnectionProxy
from repositories import Repository
from schemas.order import OrderDB


class OrderRepository(Repository):
    @abstractmethod
    async def get_user_orders(
        self,
        user_id: UUID,
        conn: PoolConnectionProxy,
    ) -> list[OrderDB]:
        ...

    @abstractmethod
    async def get_user_order_by_id(
        self,
        user_id: UUID,
        order_id: UUID,
        conn: PoolConnectionProxy,
    ) -> Optional[OrderDB]:
        ...

    @abstractmethod
    async def create_order_from_cart(
        self,
        user_id: UUID,
        conn: PoolConnectionProxy,
    ) -> Optional[OrderDB]:
        ...

    @abstractmethod
    async def get_all_subcategories(
        self,
        category_slug: str,
        conn: PoolConnectionProxy,
    ) -> Optional[OrderDB]:
        ...


class OrderRepositoryImpl(OrderRepository):
    async def get_user_orders(
        self,
        user_id: UUID,
        conn: PoolConnectionProxy,
    ) -> list[OrderDB]:
        query = "SELECT * FROM orders WHERE user_id = $1"
        result = await conn.fetch(query, user_id)
        return [OrderDB.model_validate({**order}) for order in result]

    async def get_user_order_by_id(
        self,
        user_id: UUID,
        order_id: UUID,
        conn: PoolConnectionProxy,
    ) -> Optional[OrderDB]:
        query = "SELECT * FROM orders WHERE user_id = $1 AND id = $2"
        result: Optional[Record] = await conn.fetchrow(query, user_id, order_id)
        if result is None:
            return None
        return OrderDB.model_validate({**result})

    async def create_order_from_cart(
        self,
        user_id: UUID,
        conn: PoolConnectionProxy,
    ) -> Optional[OrderDB]:
        query = "INSERT INTO orders (user_id) VALUES ($1) RETURNING *"
        result: Optional[Record] = await conn.fetchrow(query, user_id)
        if result is None:
            return None
        return OrderDB.model_validate({**result})
