from abc import abstractmethod
from typing import Optional
from uuid import UUID

from asyncpg import Pool
from core.config import settings
from httpx import AsyncClient, Response
from repositories.customer_repository import CustomerRepository
from schemas.auth import TokenResponse
from schemas.customer import CustomerDTO

from services import Service
from services.auth_service import AuthService


class CustomerService(Service):
    def __init__(
        self, repository: CustomerRepository, auth_service: AuthService, conn_pool: Pool
    ):
        self.repository: CustomerRepository = repository
        self.auth_service: AuthService = auth_service
        self.conn_pool = conn_pool

    @abstractmethod
    async def get_customer_data(self, user_id: UUID) -> Optional[CustomerDTO]: ...

    @abstractmethod
    async def select_delivery_address(
        self, address_id: UUID, user_id: UUID
    ) -> Optional[CustomerDTO]: ...


class CustomerServiceImpl(CustomerService):
    async def get_customer_data(self, user_id: UUID) -> Optional[CustomerDTO]:
        client_auth: TokenResponse | None = await self.auth_service.client_auth()
        if client_auth is None:
            return None
        async with AsyncClient() as client:
            response: Response = await client.get(
                f"{settings.keycloak.url}/admin/realms/{settings.keycloak.realm}/users/{user_id}",
                headers={"Authorization": f"Bearer {client_auth.access_token}"},
            )
            if response.status_code == 404:
                return None
        async with self.conn_pool.acquire() as conn:
            return await self.repository.get_customer_data(user_id, conn)

    async def select_delivery_address(
        self, address_id: UUID, user_id: UUID
    ) -> Optional[CustomerDTO]:
        async with self.conn_pool.acquire() as conn:
            await self.repository.select_delivery_address(address_id, user_id, conn)
            return await self.repository.get_customer_data(user_id, conn)
