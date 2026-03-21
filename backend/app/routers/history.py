import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.db_models import EvaluationHistory, User
from app.models.schemas import HistoryDetail, HistoryItem, PaginatedResponse, WordComparison
from app.services.deps import get_current_user

router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=PaginatedResponse)
async def list_history(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=50, description="Items per page"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get paginated evaluation history for the current user."""
    # Count total
    count_query = select(func.count()).select_from(EvaluationHistory).where(
        EvaluationHistory.user_id == current_user.id
    )
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Fetch page
    offset = (page - 1) * page_size
    query = (
        select(EvaluationHistory)
        .where(EvaluationHistory.user_id == current_user.id)
        .order_by(EvaluationHistory.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(query)
    records = result.scalars().all()

    items = [
        HistoryItem(
            id=str(r.id),
            practice_id=r.practice_id,
            target_text=r.target_text,
            recognized_text=r.recognized_text,
            accuracy=r.accuracy,
            completeness=r.completeness,
            fluency=r.fluency,
            overall_score=r.overall_score,
            created_at=r.created_at,
        )
        for r in records
    ]

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total > 0 else 0,
    )


@router.get("/{history_id}", response_model=HistoryDetail)
async def get_history_detail(
    history_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a single evaluation history record with full details."""
    result = await db.execute(
        select(EvaluationHistory).where(EvaluationHistory.id == history_id)
    )
    record = result.scalar_one_or_none()

    if not record or record.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Record not found")

    word_comp = None
    if record.word_comparison:
        word_comp = [WordComparison(**wc) for wc in record.word_comparison]

    return HistoryDetail(
        id=str(record.id),
        practice_id=record.practice_id,
        target_text=record.target_text,
        recognized_text=record.recognized_text,
        accuracy=record.accuracy,
        completeness=record.completeness,
        fluency=record.fluency,
        overall_score=record.overall_score,
        created_at=record.created_at,
        word_comparison=word_comp,
    )
