from uuid import UUID

from pydantic import BaseModel

from schemas.product import ProductShortDTO


class OrderProductDB(BaseModel):
    order_id: UUID
    product_id: UUID
    quantity: int


class OrderProductDTO(BaseModel):
    product: ProductShortDTO
    quantity: int
