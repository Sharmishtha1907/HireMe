from typing import Any

import httpx
from jose import jwt
from jose.exceptions import JWTError

from app import config


class KeycloakError(Exception):
    pass


class KeycloakClient:
    def __init__(self) -> None:
        self.issuer = config.KEYCLOAK_ISSUER
        self.client_id = config.KEYCLOAK_CLIENT_ID

        self._configuration: dict[str, Any] | None = None
        self._jwks: dict[str, Any] | None = None

    async def get_configuration(self) -> dict[str, Any]:
        if self._configuration is not None:
            return self._configuration

        async with httpx.AsyncClient() as client:
            response = await client.get(
                config.KEYCLOAK_OPENID_CONFIG_URL
            )

        response.raise_for_status()

        self._configuration = response.json()

        return self._configuration

    async def get_jwks(self) -> dict[str, Any]:
        if self._jwks is not None:
            return self._jwks

        configuration = await self.get_configuration()

        jwks_uri = configuration["jwks_uri"]

        async with httpx.AsyncClient() as client:
            response = await client.get(jwks_uri)

        response.raise_for_status()

        self._jwks = response.json()

        return self._jwks

    async def verify_token(
        self,
        token: str,
    ) -> dict[str, Any]:

        try:
            configuration = await self.get_configuration()
            jwks = await self.get_jwks()

            unverified_header = jwt.get_unverified_header(token)

            kid = unverified_header.get("kid")

            if not kid:
                raise KeycloakError(
                    "Token does not contain a key ID"
                )

            key = None

            for jwk in jwks["keys"]:
                if jwk.get("kid") == kid:
                    key = jwk
                    break

            if key is None:
                # Key rotation may have happened.
                self._jwks = None

                jwks = await self.get_jwks()

                for jwk in jwks["keys"]:
                    if jwk.get("kid") == kid:
                        key = jwk
                        break

            if key is None:
                raise KeycloakError(
                    "Unable to find signing key"
                )

            payload = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                audience=self.client_id,
                issuer=self.issuer,
            )

            return payload

        except JWTError as exc:
            raise KeycloakError(
                "Invalid Keycloak token"
            ) from exc

        except httpx.HTTPError as exc:
            raise KeycloakError(
                "Unable to communicate with Keycloak"
            ) from exc


keycloak_client = KeycloakClient()