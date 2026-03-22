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

        # Generate TTS audio for all practices without audio_url
        from app.services.tts_service import generate_audio

        result = await session.execute(
            select(Practice).where(Practice.audio_url.is_(None))
        )
        practices_without_audio = list(result.scalars().all())

        if practices_without_audio:
            print(f"🔊 Generating TTS audio for {len(practices_without_audio)} practices...")
            for i, practice in enumerate(practices_without_audio):
                audio_url = await generate_audio(practice.text, practice.id)
                if audio_url:
                    practice.audio_url = audio_url
                    print(f"  [{i+1}/{len(practices_without_audio)}] ✓ {practice.id}")
                else:
                    print(f"  [{i+1}/{len(practices_without_audio)}] ✗ {practice.id} (failed)")
                # Rate limiting delay
                await asyncio.sleep(0.2)
            await session.commit()
            print(f"✓ TTS audio generation complete.")
        else:
            print("✓ All practices already have audio.")

    await engine.dispose()


async def seed_admin(email: str, password: str):
    """Create an admin user if one doesn't exist."""
    from app.models.db_models import User
    from app.services.auth_service import hash_password

    database_url = os.getenv(
        "DATABASE_URL", "postgresql+asyncpg://heart@localhost:5432/sayhi"
    )
    engine = create_async_engine(database_url)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        result = await session.execute(select(User).where(User.email == email))
        existing = result.scalar_one_or_none()

        if existing:
            if existing.role != "admin":
                existing.role = "admin"
                await session.commit()
                print(f"✓ User '{email}' upgraded to admin.")
            else:
                print(f"✓ Admin user '{email}' already exists.")
        else:
            user = User(
                email=email,
                password_hash=hash_password(password),
                role="admin",
            )
            session.add(user)
            await session.commit()
            print(f"✓ Created admin user '{email}'.")

    await engine.dispose()


if __name__ == "__main__":
    force = "--force" in sys.argv

    # Seed practices
    asyncio.run(seed_practices(force=force))

    # Seed admin user: --admin email password
    if "--admin" in sys.argv:
        idx = sys.argv.index("--admin")
        if idx + 2 < len(sys.argv):
            admin_email = sys.argv[idx + 1]
            admin_password = sys.argv[idx + 2]
            asyncio.run(seed_admin(admin_email, admin_password))
        else:
            # Try env vars
            admin_email = os.getenv("ADMIN_EMAIL")
            admin_password = os.getenv("ADMIN_PASSWORD")
            if admin_email and admin_password:
                asyncio.run(seed_admin(admin_email, admin_password))
            else:
                print("Usage: python -m scripts.seed_db --admin <email> <password>")
