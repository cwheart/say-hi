import logging
import re
from typing import List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import Practice

logger = logging.getLogger(__name__)


async def get_practices(
    db: AsyncSession,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
) -> Tuple[List[Practice], int]:
    """Get all practices from DB, optionally filtered. Returns (items, total)."""
    query = select(Practice)
    count_query = select(func.count()).select_from(Practice)

    if category:
        query = query.where(Practice.category == category)
        count_query = count_query.where(Practice.category == category)
    if difficulty:
        query = query.where(Practice.difficulty == difficulty)
        count_query = count_query.where(Practice.difficulty == difficulty)

    query = query.order_by(Practice.id)

    total = (await db.execute(count_query)).scalar() or 0
    result = await db.execute(query)
    return list(result.scalars().all()), total


# Keep backward compatibility
async def get_all_practices(
    db: AsyncSession,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
) -> List[Practice]:
    """Get all practices from DB, optionally filtered."""
    practices, _ = await get_practices(db, category, difficulty)
    return practices


async def get_practice_by_id(db: AsyncSession, practice_id: str) -> Optional[Practice]:
    """Get a single practice by ID."""
    result = await db.execute(select(Practice).where(Practice.id == practice_id))
    return result.scalar_one_or_none()


def _generate_id(text: str) -> str:
    """Generate a slug-based ID from text."""
    slug = re.sub(r'[^a-z0-9]+', '-', text.lower().strip())
    slug = slug.strip('-')[:40]
    return slug


async def create_practice(db: AsyncSession, data) -> Practice:
    """Create a new practice item."""
    practice_id = _generate_id(data.text)

    # Check for conflict, append suffix if needed
    existing = await get_practice_by_id(db, practice_id)
    if existing:
        import uuid
        practice_id = f"{practice_id}-{uuid.uuid4().hex[:6]}"

    practice = Practice(
        id=practice_id,
        text=data.text,
        category=data.category,
        difficulty=data.difficulty,
        hint=data.hint,
    )
    db.add(practice)
    await db.flush()
    await db.refresh(practice)
    return practice


async def update_practice(db: AsyncSession, practice_id: str, data) -> Optional[Practice]:
    """Update an existing practice item."""
    practice = await get_practice_by_id(db, practice_id)
    if not practice:
        return None

    if data.text is not None:
        practice.text = data.text
    if data.category is not None:
        practice.category = data.category
    if data.difficulty is not None:
        practice.difficulty = data.difficulty
    if data.hint is not None:
        practice.hint = data.hint

    await db.flush()
    await db.refresh(practice)
    return practice


async def delete_practice(db: AsyncSession, practice_id: str) -> bool:
    """Delete a practice item. Returns True if deleted."""
    practice = await get_practice_by_id(db, practice_id)
    if not practice:
        return False
    await db.delete(practice)
    await db.flush()
    return True
