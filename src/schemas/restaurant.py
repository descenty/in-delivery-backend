from uuid import UUID
from pydantic import BaseModel

from schemas.order import OrderDTO


class RestaurantDB(BaseModel):
    id: UUID
    city_id: UUID
    address: str
    admin_user_id: UUID


class RestaurantDTO(RestaurantDB):
    orders: list[OrderDTO]