from abc import abstractmethod

from asyncpg import Pool

from repositories.category_repository import CategoryRepository

from schemas.category import CategoryDTO

from services import Service


class CategoryService(Service):
    def __init__(self, repository: CategoryRepository, conn_pool: Pool):
        super().__init__(conn_pool)
        self.repository: CategoryRepository = repository

    @abstractmethod
    async def get_all_parent_categories(self) -> list[CategoryDTO]:
        ...

    @abstractmethod
    async def get_category(self, category_slug: str) -> CategoryDTO | None:
        ...


class CategoryServiceImpl(CategoryService):
    async def get_all_parent_categories(self) -> list[CategoryDTO]:
        async with self.conn_pool.acquire() as conn:
            return [
                CategoryDTO.model_validate(category.model_dump())
                for category in await self.repository.get_all_parent_categories(conn)
            ]

    async def get_category(self, category_slug: str) -> CategoryDTO | None:
        async with self.conn_pool.acquire() as conn:
            if category := await self.repository.get_category(category_slug, conn):
                return CategoryDTO.model_validate(category, from_attributes=True)
            return None
