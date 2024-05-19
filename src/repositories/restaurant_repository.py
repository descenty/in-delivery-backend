import json
from abc import abstractmethod
from typing import Optional

from asyncpg import Record
from asyncpg.pool import PoolConnectionProxy
from schemas.restaurant import RestaurantDB, RestaurantDTO

from repositories import Repository


class RestaurantRepository(Repository):
    @abstractmethod
    async def get_city_restaurants(
        self,
        conn: PoolConnectionProxy,
        city_id: str,
    ) -> list[RestaurantDB]: ...

    @abstractmethod
    async def get_restaurant(
        self,
        conn: PoolConnectionProxy,
        restaurant_id: str,
    ) -> Optional[RestaurantDTO]: ...

    @abstractmethod
    async def get_admin_restaurants(
        self,
        conn: PoolConnectionProxy,
        admin_user_id: str,
    ) -> list[RestaurantDB]: ...


class RestaurantRepositoryImpl(RestaurantRepository):
    async def get_city_restaurants(
        self,
        conn: PoolConnectionProxy,
        city_id: str,
    ) -> list[RestaurantDB]:
        query = "SELECT * FROM restaurant WHERE city_id = $1"
        return [
            RestaurantDB.model_validate({**restaurant})
            for restaurant in await conn.fetch(query, city_id)
        ]

    async def get_restaurant(
        self,
        conn: PoolConnectionProxy,
        restaurant_id: str,
    ) -> Optional[RestaurantDTO]:
        query = """
        SELECT JSON_BUILD_OBJECT(
                    'id', r.id,
                    'city_id', r.city_id,
                    'address', r.address,
                    'admin_user_id', r.admin_user_id,
                    'orders', (
                        SELECT JSON_AGG(
                            JSON_BUILD_OBJECT(
                                'id', o.id,
                                'user_id', o.user_id,
                                'created_at', o.created_at,
                                'status', o.status,
                                'delivery_address', o.delivery_address,
                                'total_price', o.total_price,
                                'products', (
                                    SELECT JSON_AGG(
                                        JSON_BUILD_OBJECT(
                                        'product', JSON_BUILD_OBJECT(
                                            'id', p.id,
                                            'title', p.title,
                                            'price', p.price,
                                            'description', p.description
                                        ), 'quantity', op.quantity)
                                    )
                                    FROM product AS p
                                    join order_product op on p.id = op.product_id
                                    WHERE p.id = op.product_id
                                )
                            )
                        )
                        FROM orders AS o
                        WHERE o.restaurant_id = r.id
                    )
                )
                FROM restaurant AS r
                WHERE r.id = $1
        """
        result: Optional[Record] = await conn.fetchrow(query, restaurant_id)
        if result is None:
            return None
        print(result)
        return RestaurantDTO.model_validate(json.loads(result["json_build_object"]))

    async def get_admin_restaurants(
        self,
        conn: PoolConnectionProxy,
        admin_user_id: str,
    ) -> list[RestaurantDB]:
        query = "SELECT * FROM restaurant WHERE admin_user_id = $1"
        return [
            RestaurantDB.model_validate({**restaurant})
            for restaurant in await conn.fetch(query, admin_user_id)
        ]
