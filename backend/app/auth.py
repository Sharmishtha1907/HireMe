from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer

from app import config
from app.keycloak import KeycloakError, keycloak_client
from app.schemas import CurrentUser


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=(
        f"{config.KEYCLOAK_SERVER_URL}/realms/{config.KEYCLOAK_REALM}"
        "/protocol/openid-connect/auth"
    ),
    tokenUrl=(
        f"{config.KEYCLOAK_SERVER_URL}/realms/{config.KEYCLOAK_REALM}"
        "/protocol/openid-connect/token"
    ),
    scopes={
        "openid": "OpenID"
    },
)


async def get_current_user(
    token: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
) -> CurrentUser:

    try:
        payload = await keycloak_client.verify_token(token)

    except KeycloakError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={
                "WWW-Authenticate": "Bearer",
            },
        ) from exc

    keycloak_id = payload.get("sub")

    if not keycloak_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token does not contain user ID",
        )

    resource_access = payload.get("resource_access", {})

    client_roles = (
        resource_access
        .get(config.KEYCLOAK_BACKEND_CLIENT_ID, {})
        .get("roles", [])
    )

    realm_access = payload.get("realm_access", {})

    realm_roles = realm_access.get("roles", [])

    roles = list(set(realm_roles + client_roles))

    groups = payload.get("groups", [])

    return CurrentUser(
        keycloak_id=keycloak_id,
        username=payload.get("preferred_username"),
        email=payload.get("email"),
        first_name=payload.get("given_name"),
        last_name=payload.get("family_name"),
        groups=groups,
        roles=roles,
    )


CurrentUserDependency = Annotated[
    CurrentUser,
    Depends(get_current_user),
]


async def require_premium(
    user: CurrentUserDependency,
) -> CurrentUser:

    if "premium" not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required",
        )

    return user