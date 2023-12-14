from dataclasses import dataclass
from configuration import Configuration

from repositories.category_repository import CategoryRepository
from repositories.product_repository import ProductRepository


@dataclass
class RepositoriesConfiguration(Configuration):
    category_repository: type[CategoryRepository]
    product_repository: type[ProductRepository]
