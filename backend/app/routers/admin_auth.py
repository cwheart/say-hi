from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.db_models import User
from app.models.schemas import AuthResponse, LoginRequest, UserResponse
from app.services.auth_service import create_access_token, verify_password

router = APIRouter(prefix="/admin/auth", tags=["admin-auth"])


@router.post("/login", response_model=AuthResponse)
async def admin_login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Admin login: verify email/password and check role=admin."""
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()

    if not user or not user.password_hash or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is disabled")

    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    token = create_access_token(str(user.id), role=user.role)

    return AuthResponse(
        user=UserResponse(
            id=str(user.id), email=user.email, role=user.role,
            nickname=user.nickname, is_active=user.is_active, created_at=user.created_at,
        ),
        access_token=token,
    )
