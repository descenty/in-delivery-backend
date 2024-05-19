from abc import abstractmethod
from typing import Optional
from uuid import UUID

from asyncpg import Pool

from core.config import settings
from httpx import AsyncClient
from repositories.address_repository import AddressRepository
from schemas.address import AddressDTO, DeliveryAddressDTO

from schemas.customer import CustomerDTO
from services import Service


class AddressService(Service):
    def __init__(self, repository: AddressRepository, conn_pool: Pool):
        self.repository: AddressRepository = repository
        self.conn_pool = conn_pool

    @abstractmethod
    async def clean_address(self, address: str) -> AddressDTO: ...

    @abstractmethod
    async def add_delivery_address(
        self, address: AddressDTO, user_id: UUID
    ) -> None: ...

    @abstractmethod
    async def get_delivery_addresses(
        self, user_id: UUID
    ) -> list[DeliveryAddressDTO]: ...

    @abstractmethod
    async def delete_delivery_address(
        self, address_id: UUID, user_id: UUID
    ) -> None: ...


class AddressServiceImpl(AddressService):
    async def clean_address(self, address: str) -> AddressDTO:
        async with AsyncClient() as client:
            json_data: list[dict] = (
                await client.post(
                    url="https://cleaner.dadata.ru/api/v1/clean/address",
                    headers={
                        "Authorization": f"Token {settings.dadata.api_key}",
                        "X-Secret": settings.dadata.secret_key,
                    },
                    json=[address],
                )
            ).json()
            return AddressDTO(
                name=json_data[0]["result"],
                latitude=json_data[0]["geo_lat"],
                longitude=json_data[0]["geo_lon"],
                city_id=UUID(
                    "e87fc0af-1bc6-41b7-a5fc-76f8653549dc"
                ),  # hardcoded to Moscow city_id, should be changed in future
            )

    async def add_delivery_address(self, address: AddressDTO, user_id: UUID) -> None:
        async with self.conn_pool.acquire() as conn:
            address_id: UUID = await self.repository.add_delivery_address(
                address, user_id, conn
            )
            customer: CustomerDTO | None = await self.repository.get_customer_data(
                user_id, conn
            )
            if customer is not None and customer.delivery_address_id is None:
                await self.repository.select_delivery_address(address_id, user_id, conn)

    async def get_delivery_addresses(self, user_id: UUID) -> list[DeliveryAddressDTO]:
        async with self.conn_pool.acquire() as conn:
            return await self.repository.get_delivery_addresses(user_id, conn)

    async def delete_delivery_address(self, address_id: UUID, user_id: UUID) -> None:
        async with self.conn_pool.acquire() as conn:
            await self.repository.delete_delivery_address(address_id, user_id, conn)

    async def select_delivery_address(
        self, address_id: UUID, user_id: UUID
    ) -> Optional[CustomerDTO]:
        async with self.conn_pool.acquire() as conn:
            await self.repository.select_delivery_address(address_id, user_id, conn)
            return await self.repository.get_customer_data(user_id, conn)
