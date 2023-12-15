from abc import abstractmethod
from os import getenv

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
                f"{getenv('KC_URL')}/realms/{getenv("KC_REALM")}/protocol/openid-connect/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": getenv("KC_CLIENT_ID"),
                    "client_secret": getenv("KC_CLIENT_SECRET"),
                },
            )
            if response.status_code == 200:
                return TokenResponse.model_validate(response.json())
        return None

    async def signin(self, auth_request: AuthRequest) -> TokenResponse | None:
        async with AsyncClient() as client:
            response: Response = await client.post(
                f"{getenv('KC_URL')}/realms/{getenv('KC_REALM')}/protocol/openid-connect/token",
                data={
                    "client_id": getenv("KC_CLIENT_ID"),
                    "client_secret": getenv("KC_CLIENT_SECRET"),
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
            if response.status_code == 200:
                return TokenResponse.model_validate(response.json())
        return None

    async def signup(self, auth_request: AuthRequest) -> str | None:
        client_auth: TokenResponse | None = await self.client_auth()
        if client_auth is None:
            print("Keycloak client is not authenticated")
            return None
        async with AsyncClient() as client:
            response: Response = await client.post(
                f"{getenv('KC_URL')}/admin/realms/{getenv('KC_REALM')}/users",
                headers={"Authorization": f"Bearer {client_auth.access_token}"},
                json={
                    "email": auth_request.username,
                    "enabled": True,
                    "credentials": [
                        {"type": "password", "value": auth_request.password}
                    ],
                },
            )
            match(response.status_code):
                case 201:
                    return response.headers["Location"].split('/')[7]
                case 409:
                    print("User already exists")
                case 400:
                    print("Invalid request")
        return None
