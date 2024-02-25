from abc import abstractmethod
import json
from typing import Optional
from uuid import UUID
from asyncpg import Record
from repositories import Repository
from schemas.cart import CartDTO
from schemas.cart_product import CartProductDTO, CartProductUpdateRequest
from asyncpg.pool import PoolConnectionProxy

from schemas.product import ProductShortDTO


class CartRepository(Repository):
    @abstractmethod
    async def get_user_cart(
        self,
        user_id: UUID,
        conn: PoolConnectionProxy,
    ) -> CartDTO: ...

    @abstractmethod
    async def add_product_to_cart(
        self, user_id: UUID, product_id: UUID, quantity: int, conn: PoolConnectionProxy
    ) -> Optional[UUID]: ...

    @abstractmethod
    async def update_cart_product(
        self,
        user_id: UUID,
        product_id: UUID,
        cart_product_update: CartProductUpdateRequest,
        conn: PoolConnectionProxy,
    ) -> None: ...

    @abstractmethod
    async def delete_cart_product(
        self, user_id: UUID, product_id: UUID, conn: PoolConnectionProxy
    ) -> Optional[UUID]: ...

    @abstractmethod
    async def delete_active_cart_products(
        self, user_id: UUID, conn: PoolConnectionProxy
    ) -> None: ...


class CartRepositoryImpl(CartRepository):
    async def get_user_cart(self, user_id: UUID, conn: PoolConnectionProxy) -> CartDTO:
        query = "SELECT JSON_AGG \
            (JSON_BUILD_OBJECT('product', JSON_BUILD_OBJECT('id', p.id, 'title', p.title, 'price', p.price, 'description', p.description), 'quantity', cp.quantity)), \
                SUM(p.price * cp.quantity) total_price FROM cart_product cp \
                    LEFT JOIN product p ON p.id = cp.product_id \
                        WHERE cp.user_id = $1 GROUP BY cp.user_id"
        result: Optional[Record] = await conn.fetchrow(query, user_id)
        if result is None:
            return CartDTO.model_validate({"products": [], "total_price": 0})
        return CartDTO.model_validate(
            {
                "products": [
                    CartProductDTO.model_validate(
                        {
                            "product": ProductShortDTO.model_validate(
                                cart_product["product"]
                            ),
                            "quantity": cart_product["quantity"],
                        }
                    )
                    for cart_product in json.loads({**result}["json_agg"])
                ],
                "total_price": {**result}["total_price"],
            }
        )

    async def add_product_to_cart(
        self, user_id: UUID, product_id: UUID, quantity: int, conn: PoolConnectionProxy
    ) -> Optional[UUID]:
        query = "INSERT INTO cart_product (user_id, product_id, quantity) \
            VALUES ($1, $2, $3) RETURNING product_id"
        result: Optional[Record] = await conn.fetchrow(
            query, user_id, product_id, quantity
        )
        if result is None:
            return None
        return result[0]

    async def update_cart_product(
        self,
        user_id: UUID,
        product_id: UUID,
        cart_product_update: CartProductUpdateRequest,
        conn: PoolConnectionProxy,
    ) -> None:
        query = "UPDATE cart_product SET quantity = $3, is_active = $4 WHERE user_id = $1 AND product_id = $2 RETURNING product_id, quantity, is_active"
        result = await conn.fetchrow(
            query,
            user_id,
            product_id,
            cart_product_update.quantity,
            cart_product_update.is_active,
        )
        if result is None:
            raise Exception("Cart product not found")

    async def delete_cart_product(
        self, user_id: UUID, product_id: UUID, conn: PoolConnectionProxy
    ) -> Optional[UUID]:
        query = "DELETE FROM cart_product WHERE user_id = $1 AND product_id = $2 RETURNING product_id"
        result = await conn.fetchrow(query, user_id, product_id)
        if result is None:
            return None
        return result[0]

    async def delete_active_cart_products(
        self, user_id: UUID, conn: PoolConnectionProxy
    ) -> None:
        query = "DELETE FROM cart_product WHERE user_id = $1 AND active = TRUE"
        await conn.execute(query, user_id)
