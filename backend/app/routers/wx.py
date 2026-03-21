from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.db_models import User
from app.models.schemas import WxLoginRequest, WxAuthResponse, UserResponse
from app.services.auth_service import create_access_token
from app.services.wx_service import code_to_openid

router = APIRouter(prefix="/wx", tags=["wechat"])


@router.post("/login", response_model=WxAuthResponse)
async def wx_login(request: WxLoginRequest, db: AsyncSession = Depends(get_db)):
    """WeChat mini program login: exchange code for JWT token."""
    try:
        openid = await code_to_openid(request.code)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="WeChat service unavailable",
        )

    if not openid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="WeChat login failed: invalid or expired code",
        )

    # Find or create user by openid
    result = await db.execute(select(User).where(User.openid == openid))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(openid=openid, role="user")
        db.add(user)
        await db.flush()
        await db.refresh(user)

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    token = create_access_token(str(user.id), role=user.role)

    return WxAuthResponse(
        user=UserResponse(
            id=str(user.id), email=user.email, role=user.role,
            nickname=user.nickname, is_active=user.is_active, created_at=user.created_at,
        ),
        access_token=token,
    )
