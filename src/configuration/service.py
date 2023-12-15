from dataclasses import dataclass
from configuration import Configuration
from services.auth_service import AuthService

from services.category_service import CategoryService
from services.product_service import ProductService


@dataclass
class ServicesConfiguration(Configuration):
    auth_service: type[AuthService]
    category_service: type[CategoryService]
    product_service: type[ProductService]
