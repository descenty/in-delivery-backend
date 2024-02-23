from __future__ import annotations
from pydantic import BaseModel, model_validator, validator
from core.config import settings

from schemas.product import ProductDTO


class ParentCategoryDTO(BaseModel):
    slug: str
    title: str
    image: str = ""
    product_count: int

    @model_validator(mode="after")
    def validator(self):
        self.image = f"{settings.s3_url}/categories/{self.slug}.png"
        return self


class SubcategoryCascadeDTO(BaseModel):
    slug: str
    title: str
    image: str = ""
    product_count: int
    products: list[ProductDTO] | None

    @validator("products")
    def products_validator(cls, products: list[ProductDTO] | None):
        return products or []

    @model_validator(mode="after")
    def validator(self):
        self.image = f"{settings.s3_url}/categories/{self.slug}.png"
        return self


class CategoryCascadeDTO(BaseModel):
    slug: str
    title: str
    image: str = ""
    product_count: int
    subcategories: list[SubcategoryCascadeDTO] | None = None

    @validator("subcategories")
    def subacategories_validator(
        cls, subcategories: list[SubcategoryCascadeDTO] | None
    ):
        return subcategories or []

    @model_validator(mode="after")
    def validator(self):
        self.image = f"{settings.s3_url}/categories/{self.slug}.png"
        return self
