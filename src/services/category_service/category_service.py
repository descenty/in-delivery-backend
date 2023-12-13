from abc import ABC
from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from db.session import get_session
from repositories.category_repository import CategoryRepository
from schemas.category import CategoryDTO
from services import Service


class CategoryService(Service,):
    def __init__(self, repository: CategoryRepository):
        self.repository: CategoryRepository = repository

    async def get_all_parent_categories(self) -> list[CategoryDTO]:
        async with get_session() as session:
            return await self.repository.get_all_parent_categories(session)

    async def get_all_subcategories(self) -> list[CategoryDTO]:
        async with get_session() as session:
            return await self.repository.get_all_subcategories(session)


@lru_cache
def category_service(
    repository: CategoryRepository = Depends(CategoryRepository),
) -> CategoryService:
    return CategoryServiceImpl(repository)
