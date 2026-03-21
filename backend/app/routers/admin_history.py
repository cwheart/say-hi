import math
import uuid as uuid_mod
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.db_models import EvaluationHistory, User
from app.models.schemas import AdminHistoryItem, PaginatedResponse
from app.services.deps import require_admin

router = APIRouter(prefix="/admin/history", tags=["admin-history"])


@router.get("", response_model=PaginatedResponse)
async def list_all_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """List all evaluation history (admin only). Optionally filter by user_id."""
    base_filter = []
    if user_id:
        try:
            uid = uuid_mod.UUID(user_id)
            base_filter.append(EvaluationHistory.user_id == uid)
        except ValueError:
            pass

    count_query = select(func.count()).select_from(EvaluationHistory)
    for f in base_filter:
        count_query = count_query.where(f)
    total = (await db.execute(count_query)).scalar() or 0
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    query = (
        select(EvaluationHistory, User.email.label("user_email"))
        .join(User, EvaluationHistory.user_id == User.id, isouter=True)
        .order_by(EvaluationHistory.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    for f in base_filter:
        query = query.where(f)

    result = await db.execute(query)
    rows = result.all()

    items = []
    for row in rows:
        h = row[0]  # EvaluationHistory
        user_email = row[1]  # User.email
        items.append(AdminHistoryItem(
            id=str(h.id), practice_id=h.practice_id, target_text=h.target_text,
            recognized_text=h.recognized_text, accuracy=h.accuracy, completeness=h.completeness,
            fluency=h.fluency, overall_score=h.overall_score, created_at=h.created_at,
            user_email=user_email,
        ))

    return PaginatedResponse(
        items=items, total=total, page=page, page_size=page_size, total_pages=total_pages,
    )
