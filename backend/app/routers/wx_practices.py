from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.db_models import User
from app.models.schemas import Practice, PracticeListResponse
from app.services.deps import get_current_user
from app.services.practice_service import get_practices, get_practice_by_id

router = APIRouter(prefix="/wx/practices", tags=["wechat-practices"])


@router.get("", response_model=PracticeListResponse)
async def list_practices(
    category: str | None = Query(None),
    difficulty: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List practices for mini program users."""
    practices, total = await get_practices(db, category=category, difficulty=difficulty)
    return PracticeListResponse(
        items=[Practice(id=p.id, text=p.text, category=p.category, difficulty=p.difficulty, hint=p.hint, audio_url=p.audio_url) for p in practices],
        total=total,
    )


@router.get("/{practice_id}")
async def get_practice(
    practice_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single practice by ID."""
    practice = await get_practice_by_id(db, practice_id)
    if not practice:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Practice not found")
    return Practice(id=practice.id, text=practice.text, category=practice.category, difficulty=practice.difficulty, hint=practice.hint, audio_url=practice.audio_url)
