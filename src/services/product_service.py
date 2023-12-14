from abc import abstractmethod

from asyncpg import Pool

from repositories.product_repository import ProductRepository
from schemas.product import ProductDTO

from services import Service


class ProductService(Service):
    def __init__(self, repository: ProductRepository, conn_pool: Pool):
        super().__init__(conn_pool)
        self.repository: ProductRepository = repository

    @abstractmethod
    async def query_products(
        self, text: str | None, category_slug: str | None
    ) -> list[ProductDTO]:
        ...


class ProductServiceImpl(ProductService):
    async def query_products(self, text: str | None, category_slug: str | None) -> list[ProductDTO]:
        async with self.conn_pool.acquire() as conn:
            return [
                ProductDTO.model_validate(category.model_dump())
                for category in await self.repository.query_products(
                    conn, text, category_slug
                )
            ]
