from abc import ABC
from asyncpg import Connection
from asyncpg.pool import PoolConnectionProxy

from fastapi import BackgroundTasks


class Repository(ABC):
    def __init__(
        self, background_tasks: BackgroundTasks, conn: Connection | PoolConnectionProxy
    ):
        self.background_tasks = background_tasks
