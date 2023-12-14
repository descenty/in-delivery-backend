from asyncpg import Connection, Pool, Record, connect, create_pool

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
    pool: Pool[Record] | None = await create_pool(
        user=settings.user,
        password=settings.password,
        host=settings.host,
        port=settings.port,
        database=settings.database,
    )
    if pool is None:
        raise Exception("No connection pool")
    return pool
