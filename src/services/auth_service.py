from abc import abstractmethod

from fastapi import HTTPException
from core.config import settings

from httpx import AsyncClient, Response

from schemas.auth import AuthRequest, TokenResponse

from services import Service


class AuthService(Service):
    @abstractmethod
    async def client_auth(self) -> TokenResponse | None:
        ...

    @abstractmethod
    async def signin(self, auth_request: AuthRequest) -> TokenResponse | None:
        ...

    @abstractmethod
    async def signup(self, auth_request: AuthRequest) -> str | None:
        ...


class AuthServiceImpl(AuthService):
    async def client_auth(self) -> TokenResponse | None:
        async with AsyncClient() as client:
            response: Response = await client.post(
                f"{settings.keycloak.url}/realms/{settings.keycloak.realm}/protocol/openid-connect/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": settings.keycloak.client_id,
                    "client_secret": settings.keycloak.client_secret,
                },
            )
            if response.status_code == 200:
                return TokenResponse.model_validate(response.json())
        return None

    async def signin(self, auth_request: AuthRequest) -> TokenResponse | None:
        async with AsyncClient() as client:
            response: Response = await client.post(
                f"{settings.keycloak.url}/realms/{settings.keycloak.realm}/protocol/openid-connect/token",
                data={
                    "client_id": settings.keycloak.client_id,
                    "client_secret": settings.keycloak.client_secret,
                }
                | (
                    {
                        "grant_type": "refresh_token",
                        "refresh_token": auth_request.refresh_token,
                    }
                    if auth_request.refresh_token
                    else {
                        "grant_type": "password",
                        "username": auth_request.username,
                        "password": auth_request.password,
                    }
                ),
            )
            match (response.status_code):
                case 200:
                    return TokenResponse.model_validate(response.json())
                case 400:
                    raise HTTPException(400, "Invalid request")
                case 401:
                    raise HTTPException(401, "Invalid credentials")
        return None

    async def signup(self, auth_request: AuthRequest) -> str | None:
        client_auth: TokenResponse | None = await self.client_auth()
        if client_auth is None:
            raise Exception("Keycloak client is not authenticated")
        async with AsyncClient() as client:
            response: Response = await client.post(
                f"{settings.keycloak.url}/admin/realms/{settings.keycloak.realm}/users",
                headers={"Authorization": f"Bearer {client_auth.access_token}"},
                json={
                    "email": auth_request.username,
                    "enabled": True,
                    "credentials": [
                        {"type": "password", "value": auth_request.password}
                    ],
                },
            )
            match (response.status_code):
                case 201:
                    return response.headers["Location"].split("/")[7]
                case 409:
                    raise HTTPException(400, "User already exists")
                case 400:
                    raise HTTPException(400, "Invalid request")
        return None
