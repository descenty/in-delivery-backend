from abc import ABC
from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from db.session import get_session
from repositories.menu_repository import MenuRepository
from schemas.menu import MenuCascadeDTO, MenuCreate, MenuDTO


class CategoryService(ABC):
    def __init__(self, repository: Repository):
        self.repository = repository

    async def get_all_parent_categories(self) -> list[MenuDTO]:
        async with get_session() as session:
            return await self.repository.get_all_parent_categories(session)

    async def get_all_subcategories(self) -> list[MenuCascadeDTO]:
        async with get_session() as session:
            return await self.repository.get_all_subcategories(session)


@lru_cache
def menu_service(repository: CategoryRepository = Depends(CategoryRepository)) -> MenuService:
    return MenuService(repository)
