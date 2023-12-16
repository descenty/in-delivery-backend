from uuid import UUID

from pydantic import BaseModel


class OrderProductDB(BaseModel):
    order_id: UUID
    product_id: UUID
    quantity: int


class OrderProductDTO(OrderProductDB):
    ...
