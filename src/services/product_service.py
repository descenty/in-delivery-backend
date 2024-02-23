from abc import abstractmethod

from asyncpg import Pool

from repositories.product_repository import ProductRepository
from schemas.product import ProductDTO

from services import Service
from thefuzz import fuzz


class ProductService(Service):
    def __init__(self, repository: ProductRepository, conn_pool: Pool):
        self.repository: ProductRepository = repository
        self.conn_pool = conn_pool

    @abstractmethod
    async def query_products(
        self, text: str = "", category_slug: str = ""
    ) -> list[ProductDTO]: ...

    @abstractmethod
    async def search_products(self, text: str = "") -> list[ProductDTO]: ...


class ProductServiceImpl(ProductService):
    async def query_products(
        self, text: str = "", category_slug: str = ""
    ) -> list[ProductDTO]:
        async with self.conn_pool.acquire() as conn:
            return [
                ProductDTO.model_validate(product.model_dump())
                for product in await self.repository.query_products(
                    conn, text, category_slug
                )
            ]

    async def search_products(
        self, text: str = "", threshold: int = 80
    ) -> list[ProductDTO]:
        def search_function(title, description, text):
            return max(
                fuzz.token_set_ratio(text, title),
                fuzz.token_set_ratio(text, description),
            ) + (
                50
                if max(fuzz.ratio(text, word) for word in title.split(r" ")) > 50
                else (
                    20
                    if max(fuzz.ratio(text, word) for word in description.split(r" "))
                    > 50
                    else 0
                )
            )

        async with self.conn_pool.acquire() as conn:
            search_result: list[tuple[int, ProductDTO]] = [
                (
                    search_function(product.title, product.description, text),
                    ProductDTO.model_validate(product.model_dump()),
                )
                for product in await self.repository.query_products(conn)
                if (
                    search_function(product.title, product.description, text)
                    >= threshold
                )
            ]
            search_result.sort(key=lambda x: x[0], reverse=True)
            return [product for _, product in search_result][:5]
