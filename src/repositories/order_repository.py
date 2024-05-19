from abc import abstractmethod
import json
from typing import Optional
from uuid import UUID

from asyncpg import Record
from asyncpg.pool import PoolConnectionProxy
from schemas.cart_product import CartProductDB
from schemas.order import ORDER_STATUS, OrderDB, OrderDTO

from repositories import Repository
from schemas.order_product import OrderProductDTO


class OrderRepository(Repository):
    @abstractmethod
    async def get_user_orders(
        self,
        user_id: UUID,
        conn: PoolConnectionProxy,
    ) -> list[OrderDTO]: ...

    @abstractmethod
    async def get_user_order_by_id(
        self,
        user_id: UUID,
        order_id: UUID,
        conn: PoolConnectionProxy,
    ) -> Optional[OrderDTO]: ...

    @abstractmethod
    async def create_order_from_cart(
        self,
        user_id: UUID,
        conn: PoolConnectionProxy,
    ) -> Optional[OrderDB]: ...

    @abstractmethod
    async def is_order_restaurant_admin(
        self,
        order_id: UUID,
        user_id: UUID,
        conn: PoolConnectionProxy,
    ) -> bool: ...

    @abstractmethod
    async def complete_order(
        self,
        order_id: UUID,
        user_id: UUID,
        conn: PoolConnectionProxy,
    ) -> Optional[str]: ...


class OrderRepositoryImpl(OrderRepository):
    async def get_user_orders(
        self,
        user_id: UUID,
        conn: PoolConnectionProxy,
    ) -> list[OrderDTO]:
        query = "SELECT JSON_AGG( \
            JSON_BUILD_OBJECT( \
                'product', \
                JSON_BUILD_OBJECT( \
                    'id', p.id, \
                    'title', p.title, \
                    'price', p.price, \
                    'description', p.description \
                ), \
                'quantity', op.quantity \
            ) \
        ) AS order_info, \
        SUM(op.price * op.quantity) AS total_price, \
        o.id, \
        o.user_id, \
        o.created_at, \
        o.status, \
        o.delivery_address \
        FROM order_product AS op \
        LEFT JOIN product AS p ON p.id = op.product_id \
        LEFT JOIN orders AS o ON o.id = op.order_id \
        WHERE o.user_id = $1 \
        GROUP BY op.order_id, o.id, o.user_id, o.created_at, o.status, o.delivery_address \
        ORDER BY o.created_at DESC"
        results: list[Record] = await conn.fetch(query, user_id)
        return [
            OrderDTO.model_validate(
                {
                    "id": result["id"],
                    "user_id": result["user_id"],
                    "products": [
                        OrderProductDTO.model_validate(
                            {
                                "product": {
                                    "id": cart_product["product"]["id"],
                                    "title": cart_product["product"]["title"],
                                    "price": cart_product["product"]["price"],
                                    "description": cart_product["product"][
                                        "description"
                                    ],
                                },
                                "quantity": cart_product["quantity"],
                            }
                        )
                        for cart_product in json.loads({**result}["order_info"])
                    ],
                    "total_price": result["total_price"],
                    "created_at": result["created_at"],
                    "status": result["status"],
                    "delivery_address": result["delivery_address"],
                }
            )
            for result in results
        ]

    async def get_user_order_by_id(
        self,
        user_id: UUID,
        order_id: UUID,
        conn: PoolConnectionProxy,
    ) -> Optional[OrderDTO]:
        query = "SELECT JSON_AGG( \
            JSON_BUILD_OBJECT( \
                'product', \
                JSON_BUILD_OBJECT( \
                    'id', p.id, \
                    'title', p.title, \
                    'price', p.price, \
                    'description', p.description \
                ), \
                'quantity', op.quantity \
            ) \
        ) AS order_info, \
        SUM(op.price * op.quantity) AS total_price, \
        o.user_id, \
        o.created_at, \
        o.status, \
        o.delivery_address \
        FROM order_product AS op \
        LEFT JOIN product AS p ON p.id = op.product_id \
        LEFT JOIN orders AS o ON o.id = op.order_id \
        WHERE o.user_id = $1 AND op.order_id = $2 \
        GROUP BY op.order_id, o.user_id, o.created_at, o.status, o.delivery_address"
        result: Optional[Record] = await conn.fetchrow(query, user_id, order_id)
        if result is None:
            return None
        return OrderDTO.model_validate(
            {
                "id": order_id,
                "user_id": result["user_id"],
                "products": [
                    OrderProductDTO.model_validate(
                        {
                            "product": {
                                "id": cart_product["product"]["id"],
                                "title": cart_product["product"]["title"],
                                "price": cart_product["product"]["price"],
                                "description": cart_product["product"]["description"],
                            },
                            "quantity": cart_product["quantity"],
                        }
                    )
                    for cart_product in json.loads({**result}["order_info"])
                ],
                "total_price": result["total_price"],
                "created_at": result["created_at"],
                "status": result["status"],
                "delivery_address": result["delivery_address"],
            }
        )

    async def create_order_from_cart(
        self,
        user_id: UUID,
        conn: PoolConnectionProxy,
    ) -> Optional[OrderDB]:
        cart_products_query = "SELECT cp.product_id, cp.quantity, p.price, cp.is_active FROM cart_product cp LEFT JOIN product p ON p.id = cp.product_id WHERE cp.user_id = $1"
        cart_products: list[CartProductDB] = [
            CartProductDB.model_validate({**cart_product} | {"user_id": user_id})
            for cart_product in await conn.fetch(cart_products_query, user_id)
        ]

        total_price: float = sum(
            cart_product.price * cart_product.quantity for cart_product in cart_products
        )

        delivery_address_query = "SELECT customer_delivery_address.name FROM customer_delivery_address JOIN customer ON customer.delivery_address_id = customer_delivery_address.id WHERE customer.user_id = $1"
        delivery_address, city_id = (
            await conn.fetchval(delivery_address_query, user_id),
            "e87fc0af-1bc6-41b7-a5fc-76f8653549dc",
        )

        restaurant_id_query = (
            "SELECT id FROM restaurant WHERE city_id = $1 LIMIT 1"
        )
        restaurant_id = await conn.fetchval(restaurant_id_query, city_id)

        order_query = "INSERT INTO orders (user_id, total_price, delivery_address, status, restaurant_id) VALUES ($1, $2, $3, $4, $5) RETURNING id"
        new_order: Optional[Record] = await conn.fetchrow(
            order_query,
            user_id,
            total_price,
            delivery_address,
            "confirmed",
            restaurant_id,
        )
        if new_order is None:
            raise Exception("Order creation failed")
        order_id = new_order[0]

        order_products_query = "INSERT INTO order_product (order_id, product_id, quantity, price) VALUES ($1, $2, $3, $4)"
        for cart_product in cart_products:
            await conn.execute(
                order_products_query,
                order_id,
                cart_product.product_id,
                cart_product.quantity,
                cart_product.price,
            )

        return await self.get_user_order_by_id(user_id, order_id, conn)

    async def is_order_restaurant_admin(
        self,
        order_id: UUID,
        user_id: UUID,
        conn: PoolConnectionProxy,
    ) -> bool:
        # orders JOIN restaurant ON orders.restaurant_id = restaurant.id and restaurant.admin_id = $2
        query = "SELECT EXISTS(SELECT 1 FROM orders JOIN restaurant ON orders.restaurant_id = restaurant.id WHERE orders.id = $1 AND restaurant.admin_user_id = $2)"
        return await conn.fetchval(query, order_id, user_id)

    async def complete_order(
        self,
        order_id: UUID,
        user_id: UUID,
        conn: PoolConnectionProxy,
    ) -> Optional[str]:
        if not await self.is_order_restaurant_admin(order_id, user_id, conn):
            return None
        query = f"UPDATE orders SET status = '{ORDER_STATUS.DELIVERED.value}' WHERE id = $1 RETURNING *"
        await conn.execute(query, order_id)
        return "delivered"
