from abc import abstractmethod
from uuid import UUID
from asyncpg.pool import PoolConnectionProxy

from repositories import Repository
from schemas.address import AddressDTO


class UserRepository(Repository):
    @abstractmethod
    async def add_saved_address(
        self, conn: PoolConnectionProxy, address: AddressDTO
    ) -> None: ...

    @abstractmethod
    async def get_saved_addresses(
        self, conn: PoolConnectionProxy
    ) -> list[AddressDTO]: ...

    @abstractmethod
    async def delete_saved_address(
        self, address_id: UUID, conn: PoolConnectionProxy
    ) -> None: ...

    @abstractmethod
    async def get_user(self, user_id: UUID, conn: PoolConnectionProxy) -> dict: ...


class UserRepositoryImpl(UserRepository): ...
