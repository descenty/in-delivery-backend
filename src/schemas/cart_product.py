from uuid import UUID
from pydantic import BaseModel


class CartProductDB(BaseModel):
    product_id: UUID
    user_id: int
    quantity: int


class CartProductDTO(CartProductDB):
    ...
