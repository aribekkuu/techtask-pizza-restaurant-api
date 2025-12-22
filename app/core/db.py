from __future__ import annotations


from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


# PostgreSQL URL (async)

DB_URL = "postgresql+asyncpg://alibekzhazit@localhost:5432/techtaskdb"


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


# Создаём асинхронный движок PostgreSQL
engine = create_async_engine(
    DB_URL,
    echo=True,  # включай True если хочешь видеть SQL
    future=True,
)

# Фабрика сессий
AsyncSessionMaker = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


# Dependency для FastAPI
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionMaker() as session:
        yield session


# Создание таблиц
async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
