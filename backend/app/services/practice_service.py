import logging
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import Practice

logger = logging.getLogger(__name__)


async def get_all_practices(
    db: AsyncSession,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
) -> List[Practice]:
    """Get all practices from DB, optionally filtered."""
    query = select(Practice)
    if category:
        query = query.where(Practice.category == category)
    if difficulty:
        query = query.where(Practice.difficulty == difficulty)
    query = query.order_by(Practice.id)

    result = await db.execute(query)
    return list(result.scalars().all())


async def get_practice_by_id(db: AsyncSession, practice_id: str) -> Optional[Practice]:
    """Get a single practice by ID."""
    result = await db.execute(select(Practice).where(Practice.id == practice_id))
    return result.scalar_one_or_none()
