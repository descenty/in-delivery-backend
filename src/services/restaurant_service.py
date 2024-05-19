from abc import abstractmethod
from typing import Optional

from asyncpg import Pool

from repositories.restaurant_repository import RestaurantRepository

from schemas.restaurant import RestaurantDB, RestaurantDTO
from services import Service


class RestaurantService(Service):
    def __init__(self, repository: RestaurantRepository, conn_pool: Pool):
        self.repository: RestaurantRepository = repository
        self.conn_pool = conn_pool

    @abstractmethod
    async def get_city_restaurants(self, city_id: str) -> list[RestaurantDB]: ...

    @abstractmethod
    async def get_restaurant(self, restaurant_id: str) -> Optional[RestaurantDTO]: ...

    @abstractmethod
    async def get_admin_restaurants(self, admin_user_id: str) -> list[RestaurantDB]: ...


class RestaurantServiceImpl(RestaurantService):
    async def get_city_restaurants(self, city_id: str) -> list[RestaurantDB]:
        async with self.conn_pool.acquire() as conn:
            return await self.repository.get_city_restaurants(conn, city_id)

    async def get_restaurant(self, restaurant_id: str) -> Optional[RestaurantDTO]:
        async with self.conn_pool.acquire() as conn:
            if restaurant := await self.repository.get_restaurant(conn, restaurant_id):
                return restaurant
            return None

    async def get_admin_restaurants(self, admin_user_id: str) -> list[RestaurantDB]:
        async with self.conn_pool.acquire() as conn:
            return [
                RestaurantDB.model_validate(restaurant.model_dump())
                for restaurant in await self.repository.get_admin_restaurants(
                    conn, admin_user_id
                )
            ]
