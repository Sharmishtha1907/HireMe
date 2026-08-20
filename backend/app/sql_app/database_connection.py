from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from config import DB_URL


engine = create_async_engine(
    DB_URL,
    echo=True,
)

#FastAPI is designed to work well with asynchronous I/O
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[
    AsyncSession,
    None,
]:

    async with AsyncSessionLocal() as session:
        yield session