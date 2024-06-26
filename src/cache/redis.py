import asyncio
import logging
import pickle
from functools import lru_cache, wraps
from typing import Any, Callable

import redis.asyncio as aioredis  # type: ignore[import]
from fastapi import BackgroundTasks

from core.config import settings

logger = logging.getLogger("uvicorn")


def redis() -> aioredis.Redis:
    return aioredis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        password=settings.redis.password,
    )


class RedisClient:
    is_available: bool | None = None

    def __init__(self):
        asyncio.create_task(self.check_redis())
        asyncio.create_task(asyncio.sleep(2)).add_done_callback(
            lambda _: asyncio.create_task(self.flush())
        )

    async def check_redis(self):
        while True:
            try:
                if self.is_available != await redis().ping():
                    self.is_available = True
                    logger.info("Redis is available")
            except Exception as e:
                if self.is_available:
                    self.is_available = False
                logger.error("Redis is unavailable")
                logger.error(f"Redis error: {e}")
            await asyncio.sleep(60)

    async def flush(self):
        try:
            if self.is_available:
                await redis().flushall()
        except Exception as e:
            logger.error(f"Redis flush error: {e}")

    async def get(self, key: str, **kwargs) -> Any | None:
        try:
            if self.is_available and (data := await redis().get(key, **kwargs)):
                logger.info(f"get cache [{key}]")
                return data
        except Exception as e:
            logger.error(f"Redis get error: {e}")
        return None

    async def set(
        self, key: str, value, ex: int = settings.redis.default_ttl, **kwargs
    ) -> Any | None:
        try:
            if self.is_available:
                logger.info(f"set cache [{key}]")
                await redis().set(
                    key,
                    value,
                    ex=ex,
                )
        except Exception as e:
            logger.error(f"Redis set error: {e}")
        return None

    async def delete(self, keys: str | list[str]) -> Any | None:
        try:
            if self.is_available:
                r = redis()
                for key in keys if isinstance(keys, list) else [keys]:
                    for key_match in await r.keys(key):
                        await r.delete(key_match)
                        deleted_key = (
                            key_match
                            if isinstance(key_match, str)
                            else key_match.decode()
                        )
                        logger.info(f"invalidate cache [{deleted_key}]")
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
        return None


@lru_cache
def redis_client():
    return RedisClient()


def cached(key: str, **cache_kwargs):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            kwargs.update(zip(func.__code__.co_varnames, args))
            if (
                not settings.redis.enabled
                or not (rclient := redis_client()).is_available
            ):
                return await func(**kwargs)
            key_format = key.format(**kwargs) # TODO add optional kwargs
            if data := await rclient.get(key_format):
                return pickle.loads(data)
            result = await func(**kwargs)
            # background_tasks: BackgroundTasks = args[0].background_tasks
            # background_tasks.add_task(
            #     rclient.set, key_format, pickle.dumps(result), **cache_kwargs
            # )
            # TODO fix background_tasks
            await rclient.set(key_format, pickle.dumps(result), **cache_kwargs)
            return result

        return wrapper

    return decorator


def invalidate(keys: list[str] | str, **cache_kwargs):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            kwargs.update(zip(func.__code__.co_varnames, args))
            result = await func(**kwargs)
            if (
                not settings.redis.enabled
                or not (rclient := redis_client()).is_available
            ):
                return result
            keys_format = (
                [key.format(**kwargs) for key in keys]
                if isinstance(keys, list)
                else [keys.format(**kwargs)]
            )
            background_tasks: BackgroundTasks = args[0].background_tasks
            background_tasks.add_task(rclient.delete, keys_format, **cache_kwargs)
            return result

        return wrapper

    return decorator
