from abc import abstractmethod
from typing import Optional

from asyncpg import Pool

from repositories.category_repository import CategoryRepository

from schemas.category import CategoryCascadeDTO, ParentCategoryDTO

from services import Service


class CategoryService(Service):
    def __init__(self, repository: CategoryRepository, conn_pool: Pool):
        self.repository: CategoryRepository = repository
        self.conn_pool = conn_pool

    @abstractmethod
    async def get_all_parent_categories(self) -> list[ParentCategoryDTO]:
        ...

    @abstractmethod
    async def get_category(self, category_slug: str) -> Optional[CategoryCascadeDTO]:
        ...


class CategoryServiceImpl(CategoryService):
    async def get_all_parent_categories(self) -> list[ParentCategoryDTO]:
        async with self.conn_pool.acquire() as conn:
            return [
                ParentCategoryDTO.model_validate(category.model_dump())
                for category in await self.repository.get_all_parent_categories(conn)
            ]

    async def get_category(self, category_slug: str) -> Optional[CategoryCascadeDTO]:
        async with self.conn_pool.acquire() as conn:
            if category := await self.repository.get_category(category_slug, conn):
                return category
            return None
