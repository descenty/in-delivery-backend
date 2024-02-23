from abc import abstractmethod
from asyncpg.pool import PoolConnectionProxy

from repositories import Repository
from schemas.product import ProductDB


class ProductRepository(Repository):
    @abstractmethod
    async def query_products(
        self,
        conn: PoolConnectionProxy,
        text: str = "",
        category_slug: str = "",
    ) -> list[ProductDB]: ...


class ProductRepositoryImpl(ProductRepository):
    async def query_products(
        self,
        conn: PoolConnectionProxy,
        text: str = "",
        category_slug: str = "",
    ) -> list[ProductDB]:
        text = f"%{text}%"
        query = "SELECT * FROM product WHERE \
            ( \
                (title ILIKE $1) OR \
                (description ILIKE $1) \
            ) \
            AND $2 = '' OR (category_slug = $2)"
        print(f"Text: {text}, Category: {category_slug}")
        return [
            ProductDB.model_validate({**product})
            for product in await conn.fetch(query, text, category_slug)
        ]
