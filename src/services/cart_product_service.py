from abc import abstractmethod
from uuid import UUID

from asyncpg import Pool
from repositories.cart_repository import CartRepository

from repositories.category_repository import CategoryRepository
from schemas.cart_product import CartProductDTO

from schemas.category import CategoryDTO

from services import Service


class CartProductService(Service):
    def __init__(self, repository: CartProductRepository, conn_pool: Pool):
        self.repository: CartProductRepository = repository
        self.conn_pool = conn_pool

    @abstractmethod
    async def add_product_to_cart(
        self, user_id: UUID, product_id: UUID, quantity: int
    ) -> UUID:
        ...

    @abstractmethod
    async def update_cart_product(
        self, cart_product_id: UUID, quantity: int
    ) -> CartProductDTO:
        ...


class CartProductServiceImpl(CartProductService):
    async def add_product_to_cart(self, user_id: UUID, product_id: UUID, quantity: int) -> UUID:
        return await self.repository.add_product_to_cart