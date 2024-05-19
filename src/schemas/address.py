from uuid import UUID
from pydantic import BaseModel


class AddressDTO(BaseModel):
    name: str
    latitude: float
    longitude: float
    city_id: UUID


class AddressRequest(BaseModel):
    address: str


class DeliveryAddressDTO(BaseModel):
    id: UUID
    name: str
    city: str
    city_id: UUID
