from abc import abstractmethod
from uuid import UUID
from asyncpg import Connection
from repositories import Repository
from schemas.category import CategoryDB


class CartRepository(Repository):
    @abstractmethod
    async def get_user_cart(
        self,
        user_id: UUID,
        conn: Connection,
    ) -> list[CategoryDB]:
        ...

    @abstractmethod
    async def get_all_subcategories(
        self,
        category_slug: str,
        conn: Connection,
    ) -> list[CategoryDB]:
        ...
