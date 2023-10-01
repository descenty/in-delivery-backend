from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine

from core.config import settings
from models.base import BaseModel

postgres_url: str = ''.join(
    [
        'postgresql+asyncpg://',
        f'{settings.postgres.user}:',
        f'{settings.postgres.password}@',
        f'{settings.postgres.host}:',
        f'{settings.postgres.port}',
        f'/{settings.postgres.db}',
    ]
)


engine: AsyncEngine = create_async_engine(postgres_url)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
