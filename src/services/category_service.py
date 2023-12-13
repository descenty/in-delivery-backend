from abc import abstractmethod
from functools import lru_cache

from core.config import settings
from db import get_connection_pool
from fastapi import Depends
from repositories.category_repository import CategoryRepository, CategoryRepositoryImpl
from schemas.category import CategoryDTO

from services import Service


class CategoryService(Service[CategoryRepository]):
    @abstractmethod
    async def get_all_parent_categories(self) -> list[CategoryDTO]:
        ...

    @abstractmethod
    async def get_all_subcategories(self, category_slug) -> list[CategoryDTO]:
        ...


class CategoryServiceImpl(CategoryService):
    async def get_all_parent_categories(self) -> list[CategoryDTO]:
        async with self.conn_pool.acquire() as conn:
            return [
                CategoryDTO.model_validate(category)
                for category in await self.repository.get_all_parent_categories(conn)
            ]

    async def get_all_subcategories(self, category_slug) -> list[CategoryDTO]:
        async with self.conn_pool.acquire() as conn:
            return [
                CategoryDTO.model_validate(category)
                for category in await self.repository.get_all_subcategories(
                    category_slug, conn
                )
            ]


@lru_cache
async def menu_service(
    repository: CategoryRepository = Depends(CategoryRepositoryImpl),
) -> CategoryService:
    return CategoryServiceImpl(repository, await get_connection_pool(settings.postgres))
