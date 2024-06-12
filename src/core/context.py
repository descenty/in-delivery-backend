import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from cache.redis import redis_client
from configuration.app import AppConfiguration
from configuration.current import app_configuration

from db import get_connection_pool
from core.config import settings


# from repositories.category_repository import CategoryRepository, CategoryRepositoryImpl
# from repositories.product_repository import ProductRepository, ProductRepositoryImpl
# from services.category_service import CategoryService, CategoryServiceImpl


# class AppRepositories:
#     background_tasks: BackgroundTasks
#     category_repository: CategoryRepository
#     product_repository: ProductRepository

#     def __init__(
#         self,
#         background_tasks: BackgroundTasks,
#         **kwargs,
#     ):
#         self.background_tasks = background_tasks
#         for repository, repository_type in kwargs.items():
#             setattr(self, repository, repository_type(background_tasks))


# class AppServices:
#     repositories: AppRepositories
#     category_service: CategoryService
#     # product_service: ProductService

#     def __init__(
#         self,
#         repositories: AppRepositories,
#         conn_pool: Pool,
#         **kwargs,
#     ):
#         self.repositories = repositories
#         self.conn_pool: Pool = conn_pool
#         for service, service_type in kwargs.items():
#             setattr(self, service, service_type(repositories, conn_pool))


# @dataclass
# class AppContext:
#     services: AppServices
#     repositories: AppRepositories


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client()
    app_configuration.conn_pool = await get_connection_pool(settings.postgres)
    yield
    await app_configuration.conn_pool.close()
