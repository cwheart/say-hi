from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class WordComparison(BaseModel):
    """A single word-level comparison entry."""
    target: Optional[str] = Field(None, description="The target word (None if extra)")
    recognized: Optional[str] = Field(None, description="The recognized word (None if missing)")
    status: str = Field(..., description="One of: correct, incorrect, missing, extra")


class Scores(BaseModel):
    """Multi-dimension pronunciation scores."""
    accuracy: int = Field(..., ge=0, le=100, description="Accuracy score (0-100)")
    completeness: int = Field(..., ge=0, le=100, description="Completeness score (0-100)")
    fluency: int = Field(..., ge=0, le=100, description="Fluency score (0-100)")
    overall: int = Field(..., ge=0, le=100, description="Overall weighted score (0-100)")


class EvaluationResult(BaseModel):
    """Full pronunciation evaluation result."""
    target_text: str = Field(..., description="The reference text")
    recognized_text: str = Field(..., description="The transcribed text from Whisper")
    scores: Scores = Field(..., description="Multi-dimension scores")
    word_comparison: List[WordComparison] = Field(
        ..., description="Word-by-word alignment comparison"
    )


class EvaluationRequest(BaseModel):
    """Request body for text-only fields (audio sent as file)."""
    target_text: str = Field(..., description="The reference text to compare against")


class Practice(BaseModel):
    """A single practice item."""
    id: str = Field(..., description="Unique identifier")
    text: str = Field(..., description="The target text for pronunciation")
    category: str = Field(..., description="Category: word, phrase, or sentence")
    difficulty: str = Field(..., description="Difficulty: beginner, intermediate, or advanced")
    hint: Optional[str] = Field(None, description="Optional pronunciation hint")


class PracticeListResponse(BaseModel):
    """Response for practice list endpoint."""
    items: List[Practice]
    total: int


# ─── Auth Schemas ───


class RegisterRequest(BaseModel):
    """User registration request."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="Password (min 6 characters)")


class LoginRequest(BaseModel):
    """User login request."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="Password")


class UserResponse(BaseModel):
    """User info response."""
    id: str = Field(..., description="User UUID")
    email: Optional[str] = Field(None, description="User email")
    role: str = Field(default="user", description="User role: admin or user")
    nickname: Optional[str] = Field(None, description="User nickname")
    is_active: bool = Field(default=True, description="Account active status")
    created_at: datetime = Field(..., description="Account creation time")

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    """Authentication response with token."""
    user: UserResponse
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer")


# ─── Admin Schemas ───


class AdminUserResponse(BaseModel):
    """Admin view of a user."""
    id: str
    email: Optional[str] = None
    role: str
    openid: Optional[str] = None
    nickname: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PracticeCreate(BaseModel):
    """Request to create a new practice."""
    text: str = Field(..., description="The target text")
    category: str = Field(..., description="Category: word, phrase, or sentence")
    difficulty: str = Field(..., description="Difficulty: beginner, intermediate, or advanced")
    hint: Optional[str] = Field(None, description="Optional pronunciation hint")


class PracticeUpdate(BaseModel):
    """Request to update a practice."""
    text: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    hint: Optional[str] = None


# ─── WeChat Schemas ───


class WxLoginRequest(BaseModel):
    """WeChat mini program login request."""
    code: str = Field(..., description="wx.login() code")


class WxAuthResponse(BaseModel):
    """WeChat auth response."""
    user: UserResponse
    access_token: str
    token_type: str = "bearer"


# ─── History Schemas ───


class HistoryItem(BaseModel):
    """Summary of a single evaluation history entry."""
    id: str
    practice_id: Optional[str] = None
    target_text: str
    recognized_text: str
    accuracy: int
    completeness: int
    fluency: int
    overall_score: int
    created_at: datetime

    model_config = {"from_attributes": True}


class HistoryDetail(HistoryItem):
    """Full evaluation history entry with word comparison."""
    word_comparison: Optional[List[WordComparison]] = None


class AdminHistoryItem(HistoryItem):
    """History item with user email for admin view."""
    user_email: Optional[str] = None


class PaginatedResponse(BaseModel):
    """Generic paginated response."""
    items: list
    total: int
    page: int
    page_size: int
    total_pages: int
