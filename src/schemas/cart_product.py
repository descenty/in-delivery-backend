from uuid import UUID
from pydantic import BaseModel

from schemas.product import ProductShortDTO


class CartProductDTO(BaseModel):
    product: ProductShortDTO
    # user_id: int
    quantity: int
    # is_active: bool


class CartProductAddDTO(BaseModel):
    id: UUID
    quantity: int


class CartProductUpdateDTO(BaseModel):
    quantity: int
    is_active: bool
