from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from core.auth import get_user
from core.context import app_configuration
from schemas.cart import CartDTO
from schemas.cart_product import CartProductAddRequest, CartProductUpdateRequest
from schemas.user import User
from services.cart_service import CartService

router = APIRouter(tags=["cart"])


@router.get("/cart", name="Get cart")
async def get_cart(user: User = Depends(get_user)) -> CartDTO:
    return await app_configuration.get_service(CartService).get_cart(user.id)


@router.post(
    "/cart/products",
    name="Add product to cart and fetch",
)
async def add_product_to_cart_and_fetch(
    add_request: CartProductAddRequest, user: User = Depends(get_user)
) -> CartDTO:
    result: Optional[CartDTO] = await app_configuration.get_service(
        CartService
    ).add_product_to_cart_and_fetch(
        user.id, add_request.product_id, add_request.quantity
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return result


@router.patch("/cart/products/{product_id}", name="Update cart product")
async def update_cart_product(
    product_id: UUID,
    update_request: CartProductUpdateRequest,
    user: User = Depends(get_user),
) -> None:
    await app_configuration.get_service(CartService).update_cart_product(
        user.id, product_id, update_request
    )


@router.delete("/cart/products/{product_id}", name="Delete cart product")
async def delete_cart_product(
    product_id: UUID, user: User = Depends(get_user)
) -> Optional[UUID]:
    return await app_configuration.get_service(CartService).delete_cart_product(
        user.id, product_id
    )
