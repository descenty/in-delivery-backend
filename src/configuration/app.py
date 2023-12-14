import re
from typing import Any, TypeVar

from asyncpg import Pool
from configuration.repository import RepositoriesConfiguration
from configuration.service import ServicesConfiguration
from repositories import Repository
from services import Service
from inspect import signature


camel_pattern: re.Pattern[str] = re.compile(r"(?<!^)(?=[A-Z])")

S = TypeVar("S", bound=Service)
R = TypeVar("R", bound=Repository)


class AppConfiguration:
    repositories: RepositoriesConfiguration
    services: ServicesConfiguration
    conn_pool: Pool | None
    repositories_instances: dict[type[Repository], Any] = {}
    services_instances: dict[type[Service], Any] = {}

    def __init__(
        self,
        repositories: RepositoriesConfiguration,
        services: ServicesConfiguration,
        conn_pool: Pool | None = None,
    ):
        self.repositories = repositories
        self.services = services
        self.conn_pool = conn_pool

    def get_repository(self, repository_type: type[R]) -> R:
        target_repository = getattr(
            self.repositories,
            re.sub(camel_pattern, "_", repository_type.__name__).lower(),
        )
        if repository_type not in self.repositories_instances:
            self.repositories_instances[repository_type] = target_repository()
        return self.repositories_instances[repository_type]

    def get_service(self, service_type: type[S]) -> S:
        target_service = getattr(
            self.services, re.sub(camel_pattern, "_", service_type.__name__).lower()
        )
        if service_type not in self.services_instances:
            self.services_instances[service_type] = target_service(
                repository=self.get_repository(
                    signature(target_service.__init__)
                    .parameters["repository"]
                    .annotation
                ),
                conn_pool=self.conn_pool,
            )
        return self.services_instances[service_type]
