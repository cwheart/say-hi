"""
Seed database with practice data from practices.json.

Usage:
    python -m scripts.seed_db          # Insert if table is empty
    python -m scripts.seed_db --force  # Delete all and re-insert
"""

import asyncio
import json
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
from sqlalchemy import func, select, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv()

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "app", "data", "practices.json")


async def seed_practices(force: bool = False):
    """Seed the practices table from practices.json."""
    from app.models.db_models import Practice

    database_url = os.getenv(
        "DATABASE_URL", "postgresql+asyncpg://heart@localhost:5432/sayhi"
    )
    engine = create_async_engine(database_url)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        # Check existing count
        result = await session.execute(select(func.count()).select_from(Practice))
        count = result.scalar() or 0

        if count > 0 and not force:
            print(f"✓ Practices table already has {count} items. Skipping.")
            print("  Use --force to delete and re-insert.")
            await engine.dispose()
            return

        if count > 0 and force:
            print(f"⚠ Deleting {count} existing practice items...")
            await session.execute(delete(Practice))
            await session.commit()

        # Load JSON data
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Insert practices
        for item in data:
            practice = Practice(
                id=item["id"],
                text=item["text"],
                category=item["category"],
                difficulty=item["difficulty"],
                hint=item.get("hint"),
            )
            session.add(practice)

        await session.commit()
        print(f"✓ Inserted {len(data)} practice items into the database.")

    await engine.dispose()


if __name__ == "__main__":
    force = "--force" in sys.argv
    asyncio.run(seed_practices(force=force))
