import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    evaluations = relationship("EvaluationHistory", back_populates="user", lazy="selectin")


class Practice(Base):
    __tablename__ = "practices"

    id = Column(String(50), primary_key=True)
    text = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, index=True)
    difficulty = Column(String(50), nullable=False, index=True)
    hint = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    evaluations = relationship("EvaluationHistory", back_populates="practice", lazy="selectin")


class EvaluationHistory(Base):
    __tablename__ = "evaluation_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    practice_id = Column(String(50), ForeignKey("practices.id", ondelete="SET NULL"), nullable=True, index=True)
    target_text = Column(Text, nullable=False)
    recognized_text = Column(Text, nullable=False)
    accuracy = Column(Integer, nullable=False)
    completeness = Column(Integer, nullable=False)
    fluency = Column(Integer, nullable=False)
    overall_score = Column(Integer, nullable=False)
    word_comparison = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="evaluations")
    practice = relationship("Practice", back_populates="evaluations")
