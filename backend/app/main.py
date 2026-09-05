from fastapi import FastAPI

from app.api.v1.routes.auth_route import router as auth_route


app = FastAPI(
    title="HireMe API",
    version="1.0.0",
)


app.include_router(
    auth_route,
    prefix="/api/v1",
)


@app.get("/health")
async def health():
    return {
        "status": "ok"
    }