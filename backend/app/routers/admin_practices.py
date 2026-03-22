from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.db_models import User
from app.models.schemas import Practice, PracticeCreate, PracticeListResponse, PracticeUpdate
from app.services.deps import require_admin
from app.services import tts_service
from app.services.practice_service import (
    create_practice,
    delete_practice,
    get_practice_by_id,
    get_practices,
    update_practice,
)

router = APIRouter(prefix="/admin/practices", tags=["admin-practices"])


@router.get("", response_model=PracticeListResponse)
async def list_practices(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """List all practices (admin view)."""
    practices, total = await get_practices(db)
    return PracticeListResponse(
        items=[Practice(id=p.id, text=p.text, category=p.category, difficulty=p.difficulty, hint=p.hint, audio_url=p.audio_url) for p in practices],
        total=total,
    )


@router.post("", response_model=Practice, status_code=status.HTTP_201_CREATED)
async def create_new_practice(
    data: PracticeCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Create a new practice item."""
    practice = await create_practice(db, data)
    return Practice(id=practice.id, text=practice.text, category=practice.category, difficulty=practice.difficulty, hint=practice.hint, audio_url=practice.audio_url)


@router.put("/{practice_id}", response_model=Practice)
async def update_existing_practice(
    practice_id: str,
    data: PracticeUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Update a practice item."""
    practice = await update_practice(db, practice_id, data)
    if not practice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Practice not found")
    return Practice(id=practice.id, text=practice.text, category=practice.category, difficulty=practice.difficulty, hint=practice.hint, audio_url=practice.audio_url)


@router.delete("/{practice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_practice(
    practice_id: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Delete a practice item."""
    success = await delete_practice(db, practice_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Practice not found")


@router.post("/{practice_id}/regenerate-audio", response_model=Practice)
async def regenerate_audio(
    practice_id: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Regenerate TTS audio for a specific practice."""
    practice = await get_practice_by_id(db, practice_id)
    if not practice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Practice not found")

    audio_url = await tts_service.generate_audio(practice.text, practice_id)
    if not audio_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="TTS 音频生成失败，请检查后端日志",
        )

    practice.audio_url = audio_url
    await db.flush()
    await db.refresh(practice)

    return Practice(
        id=practice.id, text=practice.text, category=practice.category,
        difficulty=practice.difficulty, hint=practice.hint, audio_url=practice.audio_url,
    )
