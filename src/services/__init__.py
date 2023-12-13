from abc import ABC
from typing import TypeVar, Generic

from asyncpg import Pool

from repositories import Repository

R = TypeVar("R", bound=Repository)


class Service(ABC, Generic[R]):
    def __init__(self, repository: R, conn_pool: Pool):
        self.repository: R = repository
        self.conn_pool: Pool = conn_pool
