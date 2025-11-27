from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


DB_URL = "sqlite+aiosqlite:///./techtask.db"


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


engine = create_async_engine(DB_URL, echo=False)
AsyncSessionMaker = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionMaker() as session:
        yield session


async def init_db() -> None:
    """Create tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


