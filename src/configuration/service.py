from dataclasses import dataclass
from configuration import Configuration
from services.auth_service import AuthService
from services.cart_service import CartService

from services.category_service import CategoryService
from services.geo_service import GeoService
from services.order_service import OrderService
from services.product_service import ProductService


@dataclass
class ServicesConfiguration(Configuration):
    auth_service: type[AuthService]
    category_service: type[CategoryService]
    product_service: type[ProductService]
    cart_service: type[CartService]
    order_service: type[OrderService]
    geo_service: type[GeoService]
