import math
import uuid as uuid_mod

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.db_models import User
from app.models.schemas import AdminUserResponse, PaginatedResponse
from app.services.deps import require_admin

router = APIRouter(prefix="/admin/users", tags=["admin-users"])


@router.get("", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """List all users (admin only)."""
    total = (await db.execute(select(func.count()).select_from(User))).scalar() or 0
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    query = (
        select(User)
        .order_by(User.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    users = result.scalars().all()

    return PaginatedResponse(
        items=[AdminUserResponse(
            id=str(u.id), email=u.email, role=u.role, openid=u.openid,
            nickname=u.nickname, is_active=u.is_active,
            created_at=u.created_at, updated_at=u.updated_at,
        ) for u in users],
        total=total, page=page, page_size=page_size, total_pages=total_pages,
    )


@router.patch("/{user_id}/disable")
async def disable_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Disable a user account."""
    try:
        uid = uuid_mod.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    result = await db.execute(select(User).where(User.id == uid))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = False
    await db.flush()
    await db.refresh(user)

    return AdminUserResponse(
        id=str(user.id), email=user.email, role=user.role, openid=user.openid,
        nickname=user.nickname, is_active=user.is_active,
        created_at=user.created_at, updated_at=user.updated_at,
    )


@router.patch("/{user_id}/enable")
async def enable_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Enable a user account."""
    try:
        uid = uuid_mod.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    result = await db.execute(select(User).where(User.id == uid))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = True
    await db.flush()
    await db.refresh(user)

    return AdminUserResponse(
        id=str(user.id), email=user.email, role=user.role, openid=user.openid,
        nickname=user.nickname, is_active=user.is_active,
        created_at=user.created_at, updated_at=user.updated_at,
    )
