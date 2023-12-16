from uuid import UUID
from pydantic import BaseModel


class CartProductDB(BaseModel):
    product_id: UUID
    user_id: int
    quantity: int
    is_active: bool


class CartProductDTO(CartProductDB):
    ...


class CartProductUpdateDTO(BaseModel):
    quantity: int
    is_active: bool
