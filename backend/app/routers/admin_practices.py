from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.db_models import User
from app.models.schemas import Practice, PracticeCreate, PracticeListResponse, PracticeUpdate
from app.services.deps import require_admin
from app.services.practice_service import (
    create_practice,
    delete_practice,
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
        items=[Practice(id=p.id, text=p.text, category=p.category, difficulty=p.difficulty, hint=p.hint) for p in practices],
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
    return Practice(id=practice.id, text=practice.text, category=practice.category, difficulty=practice.difficulty, hint=practice.hint)


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
    return Practice(id=practice.id, text=practice.text, category=practice.category, difficulty=practice.difficulty, hint=practice.hint)


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
