from pydantic_settings import BaseSettings, SettingsConfigDict


class KeyCloakSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='_',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='allow',
    )
    server_url: str = 'http://localhost:8080/auth'
    realm: str = 'master'
    client_id: str = 'admin-cli'
    client_secret: str = 'f9a2b2d1-5d5c-4e7a-9a2e-5f2e5e2a0f9e'
    admin_client_secret: str = 'f9a2b2d1-5d5c-4e7a-9a2e-5f2e5e2a0f9e'
    callback_uri: str = 'http://localhost:8081/auth/callback'


keycloak_settings = KeyCloakSettings()
