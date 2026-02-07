from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy import text
import os
from typing import AsyncGenerator
from contextlib import asynccontextmanager


from .config import settings

# Get database URL from settings and convert to async format
# Remove sslmode and channel_binding parameters as they're not supported by asyncpg
original_url = settings.database_url
DATABASE_URL = original_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Parse and clean URL parameters
if "?" in DATABASE_URL:
    base_url, query_string = DATABASE_URL.split("?", 1)
    original_params = query_string.split("&")

    # Filter out unsupported parameters for asyncpg
    filtered_params = [
        param for param in original_params
        if not param.startswith("sslmode=") and not param.startswith("channel_binding=")
    ]

    if filtered_params:
        DATABASE_URL = f"{base_url}?{'&'.join(filtered_params)}"
    else:
        DATABASE_URL = base_url

# Create async engine with connection pooling
# Enhanced configuration to handle schema changes and prevent cache issues
engine = create_async_engine(
    DATABASE_URL,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,        # Verify connections before use
    pool_recycle=300,          # Recycle connections to avoid stale plans
    pool_reset_on_return='commit',  # Reset connections when returned to pool
    echo=False                 # Set to True for debugging SQL queries
)

# Create async session maker
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    """
    Create database tables based on SQLModel models.
    This should be called on application startup.
    """
    async with engine.begin() as conn:
        # Create all tables - this will only create tables that don't exist
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async database session for dependency injection.
    """
    async with AsyncSessionLocal() as session:
        yield session


def get_engine():
    """
    Get the database engine instance.
    """
    return engine