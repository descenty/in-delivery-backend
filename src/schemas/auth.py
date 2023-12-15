from pydantic import BaseModel


class AuthRequest(BaseModel):
    username: str
    password: str
    refresh_token: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    expires_in: int
    refresh_token: str | None = None
    refresh_expires_in: int
