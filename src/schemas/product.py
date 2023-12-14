from uuid import UUID
from pydantic import BaseModel


class ProductDB(BaseModel):
    id: UUID | None = None
    title: str
    description: str
    price: float
    best_before: int
    proteins: float
    fats: float
    carbohydrates: float
    energy: int
    weight: int
    category_slug: str


class ProductDTO(BaseModel):
    id: UUID | None = None
    title: str
    description: str
    price: float
    best_before: int
    proteins: float
    fats: float
    carbohydrates: float
    energy: int
    weight: int
    category_slug: str
