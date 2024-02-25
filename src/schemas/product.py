from uuid import UUID
from pydantic import BaseModel, model_validator
from core.config import settings


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
    image: str = ""
    price: float
    best_before: int
    proteins: float
    fats: float
    carbohydrates: float
    energy: int
    weight: int
    category_slug: str

    @model_validator(mode="after")
    def validator(self):
        self.image = f"{settings.s3_url}/products/{self.id}.png"
        return self


class ProductShortDTO(BaseModel):
    id: UUID | None = None
    title: str
    price: float
    description: str
    image: str = ""

    @model_validator(mode="after")
    def validator(self):
        self.image = f"{settings.s3_url}/products/{self.id}.png"
        return self
