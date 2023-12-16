from functools import lru_cache
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from httpx import AsyncClient, Response
from core.config import settings
from jwt import PyJWTError, decode as jwt_decode

from schemas.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_public_key() -> str:
    async with AsyncClient() as client:
        response: Response = await client.get(
            f"{settings.keycloak.url}/realms/{settings.keycloak.realm}"
        )
        if response.status_code == 200:
            return f"-----BEGIN PUBLIC KEY-----\n{response.json()["public_key"]}\n-----END PUBLIC KEY-----"
    raise Exception("Could not get public key from Keycloak")


async def get_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt_decode(
            token, await get_public_key(), algorithms=["RS256"], audience="account"
        )
        return User.model_validate(
            {"id": payload["sub"], "email": payload["email"], "roles": payload["realm_access"]["roles"]}
        )
    except PyJWTError:
        raise Exception("Could not validate credentials")
