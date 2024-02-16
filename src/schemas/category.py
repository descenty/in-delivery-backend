from __future__ import annotations
from pydantic import BaseModel, validator

from schemas.product import ProductDTO

class ParentCategoryDTO(BaseModel):
    slug: str
    title: str
    product_count: int

class SubcategoryCascadeDTO(BaseModel):
    slug: str
    title: str
    product_count: int
    products: list[ProductDTO] | None

    @validator("products")
    def products_validator(cls, products: list[ProductDTO] | None):
        return products or []


class CategoryCascadeDTO(BaseModel):
    slug: str
    title: str
    product_count: int
    subcategories: list[SubcategoryCascadeDTO] | None = None

    @validator("subcategories")
    def subacategories_validator(cls, subcategories: list[SubcategoryCascadeDTO] | None):
        return subcategories or []
