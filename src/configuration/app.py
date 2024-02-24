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
            try:
                init_parameters = {
                    parameter_name: parameter
                    for parameter_name, parameter in signature(
                        target_service.__init__
                    ).parameters.items()
                    if parameter != "self"
                }
                self.services_instances[service_type] = target_service(
                    **(
                        {
                            parameter_name: self.get_repository(
                                parameter_type.annotation
                            )
                            for parameter_name, parameter_type in init_parameters.items()
                            if parameter_type.annotation.__base__ == Repository
                        }
                        | {
                            parameter_name: self.get_service(parameter_type.annotation)
                            for parameter_name, parameter_type in init_parameters.items()
                            if parameter_type.annotation.__base__ == Service
                        }
                        | {"conn_pool": self.conn_pool}
                    )
                )
            except Exception as _:
                self.services_instances[service_type] = target_service()
        return self.services_instances[service_type]
