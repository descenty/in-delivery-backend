from uuid import UUID
from pydantic import BaseModel


class CustomerDTO(BaseModel):
    user_id: UUID
    delivery_address_id: UUID | None = None
