from abc import abstractmethod
from typing import Optional
from uuid import UUID
from asyncpg import Record
from asyncpg.pool import PoolConnectionProxy

from repositories import Repository
from schemas.address import AddressDTO, DeliveryAddressDTO
from schemas.customer import CustomerDTO


class AddressRepository(Repository):
    @abstractmethod
    async def add_delivery_address(
        self, address: AddressDTO, user_id: UUID, conn: PoolConnectionProxy
    ) -> UUID: ...

    @abstractmethod
    async def get_delivery_addresses(
        self, user_id: UUID, conn: PoolConnectionProxy
    ) -> list[DeliveryAddressDTO]: ...

    @abstractmethod
    async def delete_delivery_address(
        self, address_id: UUID, user_id: UUID, conn: PoolConnectionProxy
    ) -> None: ...

    @abstractmethod
    async def get_customer_data(
        self, user_id: UUID, conn: PoolConnectionProxy
    ) -> Optional[CustomerDTO]: ...

    @abstractmethod
    async def select_delivery_address(
        self, address_id: UUID, user_id: UUID, conn: PoolConnectionProxy
    ) -> None: ...


class AddressRepositoryImpl(AddressRepository):
    async def add_delivery_address(
        self, address: AddressDTO, user_id: UUID, conn: PoolConnectionProxy
    ) -> UUID:
        query = "INSERT INTO customer_delivery_address (user_id, name, latitude, longitude) VALUES ($1, $2, $3, $4) RETURNING id"
        result = await conn.fetchrow(
            query, user_id, address.name, address.latitude, address.longitude
        )
        if result is None:
            raise ValueError("Failed to add delivery address")
        return UUID(str(result[0]))

    async def get_delivery_addresses(
        self, user_id: UUID, conn: PoolConnectionProxy
    ) -> list[DeliveryAddressDTO]:
        query = "SELECT id, name FROM customer_delivery_address WHERE user_id = $1"
        result = await conn.fetch(query, user_id)
        return [DeliveryAddressDTO.model_validate({**address}) for address in result]

    async def delete_delivery_address(
        self, address_id: UUID, user_id: UUID, conn: PoolConnectionProxy
    ) -> None:
        query = "DELETE FROM customer_delivery_address WHERE id = $1 AND user_id = $2"
        await conn.execute(query, address_id, user_id)

    async def get_customer_data(
        self, user_id: UUID, conn: PoolConnectionProxy
    ) -> Optional[CustomerDTO]:
        query = "SELECT * FROM customer WHERE user_id = $1"
        result: Optional[Record] = await conn.fetchrow(query, user_id)
        if result is None:
            await conn.execute("INSERT INTO customer (user_id) VALUES ($1)", user_id)
            result = await conn.fetchrow(query, user_id)
            if result is None:
                return None
        return CustomerDTO.model_validate({**result})

    async def select_delivery_address(
        self, address_id: UUID, user_id: UUID, conn: PoolConnectionProxy
    ) -> None:
        query = "UPDATE customer SET delivery_address_id = $1 WHERE user_id = $2"
        await conn.execute(query, str(address_id), str(user_id))
