"""One-off: create all tables defined in models.py against the live Postgres."""
import asyncio
from app.db.session import engine, Base
from app.db import models  # noqa: F401 — importing registers all 7 tables on Base


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")


if __name__ == "__main__":
    asyncio.run(main())