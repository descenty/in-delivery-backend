from dataclasses import dataclass

from repositories.address_repository import AddressRepository
from repositories.cart_repository import CartRepository
from repositories.category_repository import CategoryRepository
from repositories.customer_repository import CustomerRepository
from repositories.order_repository import OrderRepository
from repositories.product_repository import ProductRepository
from repositories.restaurant_repository import RestaurantRepository

from configuration import Configuration


@dataclass
class RepositoriesConfiguration(Configuration):
    category_repository: type[CategoryRepository]
    product_repository: type[ProductRepository]
    cart_repository: type[CartRepository]
    order_repository: type[OrderRepository]
    address_repository: type[AddressRepository]
    customer_repository: type[CustomerRepository]
    restaurant_repository: type[RestaurantRepository]
