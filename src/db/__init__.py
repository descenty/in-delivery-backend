from functools import lru_cache
from asyncpg import Connection, Pool, connect, create_pool


async def get_connection(
    user: str, password: str, host: str, port: int, database: str
) -> Connection:
    return await connect(
        user=user, password=password, host=host, port=port, database=database
    )


@lru_cache
async def get_pool(
    user: str, password: str, host: str, port: int, database: str
) -> Pool | None:
    return await create_pool(
        user=user, password=password, host=host, port=port, database=database
    )
