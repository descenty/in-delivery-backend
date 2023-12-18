from abc import abstractmethod
import json
from typing import Optional
from asyncpg.pool import PoolConnectionProxy
from repositories import Repository
from schemas.category import CategoryCascadeDTO, ParentCategoryDTO


class CategoryRepository(Repository):
    @abstractmethod
    async def get_all_parent_categories(
        self,
        conn: PoolConnectionProxy,
    ) -> list[ParentCategoryDTO]:
        ...

    @abstractmethod
    async def get_category(
        self, category_slug: str, conn: PoolConnectionProxy
    ) -> CategoryCascadeDTO | None:
        ...


class CategoryRepositoryImpl(CategoryRepository):
    async def get_all_parent_categories(
        self,
        conn: PoolConnectionProxy,
    ) -> list[ParentCategoryDTO]:
        query = """
        SELECT json_build_object(
            'slug', c.slug,
            'title', c.title,
            'product_count', (
            SELECT COALESCE(SUM(sub_product_count), 0)
            FROM (
                SELECT COUNT(*) AS sub_product_count
                FROM product p
                JOIN category sc ON p.category_slug = sc.slug
                WHERE sc.parent_slug = c.slug
                GROUP BY p.category_slug
            ) AS subcategory_counts
        )
        ) FROM category c WHERE parent_slug is NULL
        """
        return [
            ParentCategoryDTO.model_validate(json.loads({**category}["json_build_object"]))
            for category in await conn.fetch(query)
        ]

    async def get_category(
        self,
        category_slug: str,
        conn: PoolConnectionProxy,
    ) -> Optional[CategoryCascadeDTO]:
        query = """
SELECT
    json_build_object(
        'slug', c.slug,
        'title', c.title,
        'product_count', (
            SELECT COALESCE(SUM(sub_product_count), 0)
            FROM (
                SELECT COUNT(*) AS sub_product_count
                FROM product p
                JOIN category sc ON p.category_slug = sc.slug
                WHERE sc.parent_slug = c.slug
                GROUP BY p.category_slug
            ) AS subcategory_counts
        ),
        'subcategories', (
            SELECT json_agg(json_build_object(
                'slug', sc.slug,
                'title', sc.title,
                'product_count', (
                    SELECT COUNT(*)
                    FROM product p
                    WHERE p.category_slug = sc.slug
                ),
                'products', (
                    SELECT json_agg(p)
                    FROM product p
                    WHERE p.category_slug = sc.slug
                )
            ))
            FROM category sc
            WHERE sc.parent_slug = c.slug
        )
    )
FROM category c
WHERE c.slug = $1
        """
        result = await conn.fetchrow(query, category_slug)
        if result is None:
            return None
        category = CategoryCascadeDTO.model_validate(
            json.loads({**result}["json_build_object"])
        )
        return category
