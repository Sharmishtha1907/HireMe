from fastapi import APIRouter

from app.auth import CurrentUserDependency


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.get("/user")
async def get_me(
    user: CurrentUserDependency,
):
    return user