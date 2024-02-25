from repositories.cart_repository import CartRepositoryImpl
from repositories.category_repository import CategoryRepositoryImpl
from repositories.customer_repository import CustomerRepositoryImpl
from repositories.order_repository import OrderRepositoryImpl
from repositories.product_repository import ProductRepositoryImpl
from repositories.address_repository import AddressRepositoryImpl
from services.address_service import AddressServiceImpl
from services.auth_service import AuthServiceImpl
from services.cart_service import CartServiceImpl
from services.category_service import CategoryServiceImpl
from services.customer_service import CustomerServiceImpl
from services.order_service import OrderServiceImpl
from services.product_service import ProductServiceImpl

from configuration.app import AppConfiguration
from configuration.repository import RepositoriesConfiguration
from configuration.service import ServicesConfiguration

app_configuration = AppConfiguration(
    repositories=RepositoriesConfiguration(
        category_repository=CategoryRepositoryImpl,
        product_repository=ProductRepositoryImpl,
        cart_repository=CartRepositoryImpl,
        order_repository=OrderRepositoryImpl,
        address_repository=AddressRepositoryImpl,
        customer_repository=CustomerRepositoryImpl,
    ),
    services=ServicesConfiguration(
        auth_service=AuthServiceImpl,
        category_service=CategoryServiceImpl,
        product_service=ProductServiceImpl,
        cart_service=CartServiceImpl,
        order_service=OrderServiceImpl,
        address_service=AddressServiceImpl,
        customer_service=CustomerServiceImpl,
    ),
)
