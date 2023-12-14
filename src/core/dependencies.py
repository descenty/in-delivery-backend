import re
from typing import TypeVar

from fastapi import Request
from repositories import Repository

from services import Service

camel_pattern: re.Pattern[str] = re.compile(r"(?<!^)(?=[A-Z])")

S = TypeVar("S", bound=Service)
R = TypeVar("R", bound=Repository)


def get_service(request: Request, service_type: type[S]) -> S:
    return getattr(
        request.app.state.context.services,
        re.sub(camel_pattern, "_", service_type.__name__).lower(),
    )


def get_repository(request: Request, repository_type: type[R]) -> R:
    return getattr(
        request.app.state.context.repositories,
        re.sub(camel_pattern, "_", repository_type.__name__).lower(),
    )


# def depends(func):
#     @wraps(func)
#     async def wrapper(*args, **kwargs):
#         print(args, kwargs)
#         return await func(*args, **kwargs)

#     return wrapper
