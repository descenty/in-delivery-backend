from decimal import Decimal
from pydantic import BaseModel

from schemas.cart_product import CartProductDTO


class CartDTO(BaseModel):
    total_price: Decimal
    products: list[CartProductDTO]

