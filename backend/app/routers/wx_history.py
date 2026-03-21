import math

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.db_models import EvaluationHistory, User
from app.models.schemas import HistoryDetail, HistoryItem, PaginatedResponse
from app.services.deps import get_current_user

router = APIRouter(prefix="/wx/history", tags=["wechat-history"])


@router.get("", response_model=PaginatedResponse)
async def get_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get paginated evaluation history for the current mini program user."""
    count_query = select(func.count()).select_from(EvaluationHistory).where(
        EvaluationHistory.user_id == current_user.id
    )
    total = (await db.execute(count_query)).scalar() or 0
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    query = (
        select(EvaluationHistory)
        .where(EvaluationHistory.user_id == current_user.id)
        .order_by(EvaluationHistory.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    items = result.scalars().all()

    return PaginatedResponse(
        items=[HistoryItem(
            id=str(h.id), practice_id=h.practice_id, target_text=h.target_text,
            recognized_text=h.recognized_text, accuracy=h.accuracy, completeness=h.completeness,
            fluency=h.fluency, overall_score=h.overall_score, created_at=h.created_at,
        ) for h in items],
        total=total, page=page, page_size=page_size, total_pages=total_pages,
    )


@router.get("/{history_id}", response_model=HistoryDetail)
async def get_history_detail(
    history_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific evaluation history entry."""
    import uuid as uuid_mod
    try:
        uid = uuid_mod.UUID(history_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    result = await db.execute(
        select(EvaluationHistory).where(
            EvaluationHistory.id == uid,
            EvaluationHistory.user_id == current_user.id,
        )
    )
    h = result.scalar_one_or_none()
    if not h:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return HistoryDetail(
        id=str(h.id), practice_id=h.practice_id, target_text=h.target_text,
        recognized_text=h.recognized_text, accuracy=h.accuracy, completeness=h.completeness,
        fluency=h.fluency, overall_score=h.overall_score, created_at=h.created_at,
        word_comparison=h.word_comparison,
    )
