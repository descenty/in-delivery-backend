from abc import ABC

from asyncpg import Pool


class Service(ABC):
    def __init__(self, conn_pool: Pool):
        self.conn_pool: Pool = conn_pool
