from abc import abstractmethod
from typing import Optional
from uuid import UUID

from asyncpg import Pool
from repositories.cart_repository import CartRepository

from schemas.cart import CartDTO
from schemas.cart_product import CartProductDTO, CartProductUpdateDTO

from services import Service


class CartService(Service):
    def __init__(self, repository: CartRepository, conn_pool: Pool):
        self.repository: CartRepository = repository
        self.conn_pool = conn_pool

    @abstractmethod
    async def get_cart(self, user_id: UUID) -> CartDTO:
        ...

    @abstractmethod
    async def add_product_to_cart(
        self, user_id: UUID, product_id: UUID, quantity: int
    ) -> Optional[UUID]:
        ...

    @abstractmethod
    async def update_cart_product(
        self, user_id: UUID, product_id: UUID, cart_product_update: CartProductUpdateDTO
    ) -> Optional[CartProductDTO]:
        ...

    @abstractmethod
    async def delete_cart_product(
        self, user_id: UUID, product_id: UUID
    ) -> Optional[UUID]:
        ...

    @abstractmethod
    async def delete_active_cart_products(self, user_id: UUID) -> None:
        ...


class CartServiceImpl(CartService):
    async def get_cart(self, user_id: UUID) -> CartDTO:
        async with self.conn_pool.acquire() as conn:
            return CartDTO.model_validate(
                (await self.repository.get_user_cart(user_id, conn)).model_dump()
            )

    async def add_product_to_cart(
        self, user_id: UUID, product_id: UUID, quantity: int
    ) -> Optional[UUID]:
        async with self.conn_pool.acquire() as conn:
            return await self.repository.add_product_to_cart(
                user_id, product_id, quantity, conn
            )

    async def update_cart_product(
        self, user_id: UUID, product_id: UUID, cart_product_update: CartProductUpdateDTO
    ) -> Optional[CartProductDTO]:
        async with self.conn_pool.acquire() as conn:
            return CartProductDTO.model_validate(
                await self.repository.update_cart_product(
                    user_id, product_id, cart_product_update, conn
                )
            )

    async def delete_cart_product(
        self, user_id: UUID, product_id: UUID
    ) -> Optional[UUID]:
        async with self.conn_pool.acquire() as conn:
            return await self.repository.delete_cart_product(user_id, product_id, conn)

    async def delete_active_cart_products(self, user_id: UUID) -> None:
        async with self.conn_pool.acquire() as conn:
            await self.repository.delete_active_cart_products(user_id, conn)
