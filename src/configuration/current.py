from repositories.category_repository import CategoryRepositoryImpl
from repositories.product_repository import ProductRepositoryImpl
from services.category_service import CategoryServiceImpl

from configuration.app import AppConfiguration
from configuration.repository import RepositoriesConfiguration
from configuration.service import ServicesConfiguration
from services.product_service import ProductServiceImpl

app_configuration = AppConfiguration(
    repositories=RepositoriesConfiguration(
        category_repository=CategoryRepositoryImpl,
        product_repository=ProductRepositoryImpl,
    ),
    services=ServicesConfiguration(
        category_service=CategoryServiceImpl,
        product_service=ProductServiceImpl,
    ),
)
