from uuid import UUID
from pydantic import BaseModel


class CartProductDTO(BaseModel):
    product_id: UUID
    # user_id: int
    quantity: int
    # is_active: bool


class CartProductAddDTO(BaseModel):
    id: UUID
    quantity: int


class CartProductUpdateDTO(BaseModel):
    quantity: int
    is_active: bool
