from typing import AsyncGenerator
from urllib.parse import quote_plus
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from src.config import settings
from src.model.entity import *

postgres_url = settings.database_url

engine = create_async_engine(
    postgres_url,
    echo=settings.DB_ECHO_LOG,
    future=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True,
    poolclass=AsyncAdaptedQueuePool
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )

    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()