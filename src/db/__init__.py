from functools import lru_cache
from asyncpg import Connection, Pool, connect, create_pool

from core.config import PostgresSettings


async def get_connection(settings: PostgresSettings) -> Connection:
    return await connect(
        user=settings.user,
        password=settings.password,
        host=settings.host,
        port=settings.port,
        database=settings.database,
    )


async def get_connection_pool(settings: PostgresSettings) -> Pool:
    async with create_pool(
        user=settings.user,
        password=settings.password,
        host=settings.host,
        port=settings.port,
        database=settings.database,
    ) as pool:
        return pool
