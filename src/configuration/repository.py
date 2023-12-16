from dataclasses import dataclass
from configuration import Configuration
from repositories.cart_repository import CartRepository

from repositories.category_repository import CategoryRepository
from repositories.order_repository import OrderRepository
from repositories.product_repository import ProductRepository


@dataclass
class RepositoriesConfiguration(Configuration):
    category_repository: type[CategoryRepository]
    product_repository: type[ProductRepository]
    cart_repository: type[CartRepository]
    order_repository: type[OrderRepository]
