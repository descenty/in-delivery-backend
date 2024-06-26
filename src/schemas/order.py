from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID
from pydantic import BaseModel

from schemas.order_product import OrderProductDTO


class ORDER_STATUS(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    DELIVERED = "delivered"
    REFUNDED = "refunded"


class OrderDB(BaseModel):
    id: UUID
    user_id: UUID
    delivery_address: str
    total_price: Decimal
    status: ORDER_STATUS
    created_at: datetime


class OrderDTO(OrderDB):
    products: list[OrderProductDTO]
