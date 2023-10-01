from fastapi_keycloak import FastAPIKeycloak
from .config import keycloak_settings

idp = FastAPIKeycloak(
    server_url=keycloak_settings.server_url,
    realm=keycloak_settings.realm,
    client_id=keycloak_settings.client_id,
    client_secret=keycloak_settings.client_secret,
    admin_client_secret=keycloak_settings.admin_client_secret,
    callback_uri=keycloak_settings.callback_uri,
)

'''
idp.add_swagger_config(app)

@app.get("/admin")
def admin(user: OIDCUser = Depends(idp.get_current_user(required_roles=["admin"]))):
    return f'Hi premium user {user}'


@app.get("/user/roles")
def user_roles(user: OIDCUser = Depends(idp.get_current_user)):
    return f'{user.roles}'
'''
