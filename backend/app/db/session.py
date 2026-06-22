from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# 1. The engine: one per app, manages the connection pool
engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_size=20,        # base connections kept open (default was 5)
    max_overflow=30,     # extra burst connections (default was 10) -> 50 max
    pool_timeout=30,     # seconds to wait for a free connection before erroring
    pool_pre_ping=True,  # check a connection is alive before using (avoids stale-conn errors)
)

# 2. A factory that produces AsyncSession objects
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# 3. Base class that all our table models will inherit from
class Base(DeclarativeBase):
    pass


# 4. Dependency: hands a session to a route, guarantees cleanup
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session