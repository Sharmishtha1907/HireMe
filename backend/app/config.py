import os
import dotenv

dotenv.load_dotenv()



MODEL="llama3.2"

LLM_PROVIDER="ollama"

DB_URL = os.environ["DATABASE_URL"]

KEYCLOAK_SERVER_URL = os.getenv(
    "KEYCLOAK_SERVER_URL",
    "http://localhost:8080",
)

KEYCLOAK_REALM = os.getenv(
    "KEYCLOAK_REALM",
    "HireMe",
)

KEYCLOAK_CLIENT_ID = os.getenv(
    "KEYCLOAK_CLIENT_ID",
    "hireme-frontend",
)
KEYCLOAK_BACKEND_CLIENT_ID = os.getenv(
    "KEYCLOAK_BACKEND_CLIENT_ID",
    "hireme-backend",
)
KEYCLOAK_ISSUER = (
    f"{KEYCLOAK_SERVER_URL}"
    f"/realms/{KEYCLOAK_REALM}"
)

KEYCLOAK_OPENID_CONFIG_URL = (
    f"{KEYCLOAK_ISSUER}"
    "/.well-known/openid-configuration"
)