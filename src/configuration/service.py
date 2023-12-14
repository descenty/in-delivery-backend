from dataclasses import dataclass
from configuration import Configuration

from services.category_service import CategoryService
from services.product_service import ProductService


@dataclass
class ServicesConfiguration(Configuration):
    category_service: type[CategoryService]
    product_service: type[ProductService]
