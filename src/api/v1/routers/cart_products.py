from uuid import UUID
from fastapi import APIRouter, Depends
from core.context import app_configuration
from schemas.product import ProductDTO
from schemas.request import QueryProductsRequest
from services.product_service import ProductService

router = APIRouter(tags=["products"])


@router.get(
    "/products/{product_id}/add_to_cart",
    name="add-product-to-cart",
)
async def add_product_to_cart(
    product_id: UUID, user_id: UUID = Depends()
):
    ...


@router.get("/cart/products")
async def get_cart_products():


@router.patch("cart/products/{product_id}")
async def update_cart_product():