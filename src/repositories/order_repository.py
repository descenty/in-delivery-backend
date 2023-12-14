from abc import abstractmethod
from uuid import UUID
from asyncpg import Connection
from repositories import Repository
from schemas.order import OrderDB


class OrderRepository(Repository):
    @abstractmethod
    async def get_user_orders(
        self,
        user_id: UUID,
        conn: Connection,
    ) -> list[OrderDB]:
        ...

    @abstractmethod
    async def get_order_by_id(
        self,
        order_id: UUID,
        conn: Connection,
    ) -> list[OrderDB]:
        ...

    @abstractmethod
    async def create_order(
        self,
        user_id: UUID,
        # order: OrderCreateDTO
        conn: Connection,
    ) -> list[OrderDB]:
        ...

    @abstractmethod
    async def get_all_subcategories(
        self,
        category_slug: str,
        conn: Connection,
    ) -> list[OrderDB]:
        ...