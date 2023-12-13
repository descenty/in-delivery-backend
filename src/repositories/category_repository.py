from abc import abstractmethod
from asyncpg.pool import PoolConnectionProxy
from repositories import Repository
from schemas.category import CategoryDB


class CategoryRepository(Repository):
    @abstractmethod
    async def get_all_parent_categories(
        self,
        conn: PoolConnectionProxy,
    ) -> list[CategoryDB]:
        ...

    @abstractmethod
    async def get_all_subcategories(
        self,
        category_slug: str,
        conn: PoolConnectionProxy,
    ) -> list[CategoryDB]:
        ...


class CategoryRepositoryImpl(CategoryRepository):
    async def get_all_parent_categories(
        self,
        conn: PoolConnectionProxy,
    ) -> list[CategoryDB]:
        query = "SELECT * FROM category WHERE parent_slug is NULL"
        return [
            CategoryDB.model_validate(category) for category in await conn.fetch(query)
        ]

    async def get_all_subcategories(
        self,
        category_slug: str,
        conn: PoolConnectionProxy,
    ) -> list[CategoryDB]:
        query = "SELECT * FROM category WHERE parent_slug = $1"
        return [
            CategoryDB.model_validate(category)
            for category in await conn.fetch(query, category_slug)
        ]
