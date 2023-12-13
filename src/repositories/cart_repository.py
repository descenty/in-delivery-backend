from abc import abstractmethod
from uuid import UUID
from asyncpg import Connection
from models.category import Category
from repositories import Repository


class CartRepository(Repository):
    @abstractmethod
    async def get_user_cart(
        self,
        user_id: UUID,
        conn: Connection,
    ) -> list[Category]:
        ...

    @abstractmethod
    async def get_all_subcategories(
        self,
        category_slug: str,
        conn: Connection,
    ) -> list[Category]:
        ...
