from abc import abstractmethod
from asyncpg import Connection

from models.category import Category
from repositories import Repository


class ProductRepository(Repository):
    @abstractmethod
    async def query_products(
        self,
        conn: Connection,
        text: str | None = None,
        category_slug: str | None = None,
    ) -> list[Category]:
        ...


class ProductRepositoryImpl(ProductRepository):
    async def query_products(
        self,
        conn: Connection,
        text: str | None = None,
        category_slug: str | None = None,
    ) -> list[Category]:
        query = "SELECT * FROM product WHERE \
            ( \
                ($1 IS NULL OR title ILIKE $1) OR \
                ($1 IS NULL OR description ILIKE $1) \
            ) \
            AND ($2 IS NULL OR category_slug = $2)"
        return [
            Category.model_validate(category)
            for category in await conn.fetch(query, text, category_slug)
        ]
