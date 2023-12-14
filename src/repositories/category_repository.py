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
    async def get_category(
        self, category_slug: str, conn: PoolConnectionProxy
    ) -> CategoryDB | None:
        ...


class CategoryRepositoryImpl(CategoryRepository):
    async def get_all_parent_categories(
        self,
        conn: PoolConnectionProxy,
    ) -> list[CategoryDB]:
        query = "SELECT * FROM category WHERE parent_slug is NULL"
        return [
            CategoryDB.model_validate({**category})
            for category in await conn.fetch(query)
        ]

    async def get_category_subcategories(
        self,
        category_slug: str,
        conn: PoolConnectionProxy,
    ) -> CategoryDB | None:
        query = "WITH RECURSIVE CategoryHierarchy AS \
            (SELECT slug, title, parent_slug FROM category \
                WHERE slug = $1 UNION ALL \
                    SELECT c.slug, c.title, c.parent_slug FROM category c \
                        INNER JOIN CategoryHierarchy ch ON c.parent_slug = ch.slug ) \
                            SELECT * FROM CategoryHierarchy"
        result = await conn.fetch(query, category_slug)
        print(result[1:])
        category = CategoryDB.model_validate(
            {**result[0]} | {"subcategories": [{**category} for category in result[1:]]}
        )
        return category
