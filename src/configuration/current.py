from repositories.cart_repository import CartRepositoryImpl
from repositories.category_repository import CategoryRepositoryImpl
from repositories.order_repository import OrderRepositoryImpl
from repositories.product_repository import ProductRepositoryImpl
from services.auth_service import AuthServiceImpl
from services.cart_service import CartServiceImpl
from services.category_service import CategoryServiceImpl

from configuration.app import AppConfiguration
from configuration.repository import RepositoriesConfiguration
from configuration.service import ServicesConfiguration
from services.order_service import OrderServiceImpl
from services.product_service import ProductServiceImpl

app_configuration = AppConfiguration(
    repositories=RepositoriesConfiguration(
        category_repository=CategoryRepositoryImpl,
        product_repository=ProductRepositoryImpl,
        cart_repository=CartRepositoryImpl,
        order_repository=OrderRepositoryImpl,
    ),
    services=ServicesConfiguration(
        auth_service=AuthServiceImpl,
        category_service=CategoryServiceImpl,
        product_service=ProductServiceImpl,
        cart_service=CartServiceImpl,
        order_service=OrderServiceImpl,
    ),
)
