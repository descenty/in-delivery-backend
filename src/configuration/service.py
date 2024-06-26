from dataclasses import dataclass

from services.address_service import AddressService
from services.auth_service import AuthService
from services.cart_service import CartService
from services.category_service import CategoryService
from services.customer_service import CustomerService
from services.order_service import OrderService
from services.product_service import ProductService
from services.restaurant_service import RestaurantService

from configuration import Configuration


@dataclass
class ServicesConfiguration(Configuration):
    auth_service: type[AuthService]
    category_service: type[CategoryService]
    product_service: type[ProductService]
    cart_service: type[CartService]
    order_service: type[OrderService]
    address_service: type[AddressService]
    customer_service: type[CustomerService]
    restaurant_service: type[RestaurantService]
