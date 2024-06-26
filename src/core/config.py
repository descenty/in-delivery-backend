from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseModel):
    user: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: int = 5432
    database: str = "in_delivery"


class RedisSettings(BaseModel):
    host: str = "redis"
    port: int = 6379
    password: str = ""
    default_ttl: int = 3600
    enabled: bool = True


class CelerySettings(BaseModel):
    broker: str = "amqp://localhost:5672"
    backend: str = "redis://localhost:6379"


class KeyCloakSettings(BaseModel):
    url: str = "https://127.0.0.1:8443"
    realm: str = "in-delivery"
    client_id: str = "backend"
    client_secret: str = "client-secret"
    # admin_client_secret: str = "admin-client-secret"


class DadataSettings(BaseModel):
    api_key: str = ""
    secret_key: str = ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )
    app_url: str = "http://localhost:8000"
    app_title: str = "in-delivery"
    cors_allow_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    postgres: PostgresSettings = PostgresSettings()
    keycloak: KeyCloakSettings = KeyCloakSettings()
    redis: RedisSettings = RedisSettings()
    celery: CelerySettings = CelerySettings()
    dadata: DadataSettings = DadataSettings()
    s3_url: str = "http://localhost:9000/in-delivery"
    menus_xl_path: str = "admin/Menu.xlsx"


settings = Settings()
