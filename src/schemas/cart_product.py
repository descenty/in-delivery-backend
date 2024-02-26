from uuid import UUID
from pydantic import BaseModel

from schemas.product import ProductShortDTO


class CartProductDTO(BaseModel):
    product: ProductShortDTO
    # user_id: int
    quantity: int
    # is_active: bool


class CartProductDB(BaseModel):
    user_id: UUID
    product_id: UUID
    is_active: bool
    quantity: int
    price: float


class CartProductAddRequest(BaseModel):
    product_id: UUID
    quantity: int


class CartProductUpdateRequest(BaseModel):
    quantity: int
    is_active: bool = True
