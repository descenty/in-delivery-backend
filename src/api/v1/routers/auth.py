from fastapi import APIRouter
from schemas.auth import AuthRequest, TokenResponse
from core.context import app_configuration
from services.auth_service import AuthService

router = APIRouter(tags=["auth"])


@router.post("/sign-in", name="sign-in")
async def signin(auth_request: AuthRequest) -> TokenResponse | None:
    return await app_configuration.get_service(AuthService).signin(auth_request)


@router.post("/sign-up", name="sign-up")
async def signup(auth_request: AuthRequest) -> str | None:
    return await app_configuration.get_service(AuthService).signup(auth_request)
