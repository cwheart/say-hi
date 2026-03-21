from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.schemas import Practice as PracticeSchema, PracticeListResponse
from app.services.practice_service import get_all_practices, get_practice_by_id

router = APIRouter()


@router.get("/practices", response_model=PracticeListResponse)
async def list_practices(
    category: Optional[str] = Query(None, description="Filter by category: word, phrase, sentence"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty: beginner, intermediate, advanced"),
    db: AsyncSession = Depends(get_db),
):
    """List practice items with optional category and difficulty filtering."""
    valid_categories = {"word", "phrase", "sentence"}
    if category and category not in valid_categories:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category '{category}'. Valid: {', '.join(valid_categories)}",
        )

    valid_difficulties = {"beginner", "intermediate", "advanced"}
    if difficulty and difficulty not in valid_difficulties:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid difficulty '{difficulty}'. Valid: {', '.join(valid_difficulties)}",
        )

    practices = await get_all_practices(db, category=category, difficulty=difficulty)
    items = [
        PracticeSchema(
            id=p.id, text=p.text, category=p.category,
            difficulty=p.difficulty, hint=p.hint,
        )
        for p in practices
    ]
    return PracticeListResponse(items=items, total=len(items))


@router.get("/practices/{practice_id}", response_model=PracticeSchema)
async def get_practice(practice_id: str, db: AsyncSession = Depends(get_db)):
    """Get a single practice item by ID."""
    practice = await get_practice_by_id(db, practice_id)
    if not practice:
        raise HTTPException(status_code=404, detail=f"Practice '{practice_id}' not found")
    return PracticeSchema(
        id=practice.id, text=practice.text, category=practice.category,
        difficulty=practice.difficulty, hint=practice.hint,
    )