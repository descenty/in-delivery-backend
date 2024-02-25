from abc import abstractmethod
from typing import Optional
from uuid import UUID
from asyncpg import Record
from asyncpg.pool import PoolConnectionProxy

from repositories import Repository
from schemas.customer import CustomerDTO


class CustomerRepository(Repository):
    @abstractmethod
    async def get_customer_data(
        self, user_id: UUID, conn: PoolConnectionProxy
    ) -> Optional[CustomerDTO]: ...

    @abstractmethod
    async def select_delivery_address(
        self, address_id: UUID, user_id: UUID, conn: PoolConnectionProxy
    ) -> None: ...


class CustomerRepositoryImpl(CustomerRepository):
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
