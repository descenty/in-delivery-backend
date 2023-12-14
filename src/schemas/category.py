from __future__ import annotations
from pydantic import BaseModel


class CategoryDB(BaseModel):
    slug: str
    title: str
    parent_slug: str | None = None
    subcategories: list[CategoryDB] | None = None


class CategoryDTO(BaseModel):
    slug: str
    title: str
    parent_slug: str | None = None
    subcategories: list[CategoryDTO] | None = None
