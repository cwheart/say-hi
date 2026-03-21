import logging
import os
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.db_models import EvaluationHistory, User
from app.models.schemas import EvaluationResult
from app.services.audio_service import (
    SUPPORTED_FORMATS,
    cleanup_files,
    convert_to_wav,
    save_upload_file,
)
from app.services.deps import get_current_user
from app.services.scoring_service import evaluate_pronunciation
from app.services.whisper_service import whisper_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/wx", tags=["wechat-evaluate"])

MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 10 * 1024 * 1024))


@router.post("/evaluate", response_model=EvaluationResult)
async def wx_evaluate(
    audio: UploadFile = File(..., description="Audio file (MP3, WAV, etc.)"),
    target_text: str = Form(..., description="The reference text to compare against"),
    practice_id: Optional[str] = Form(None, description="Optional practice ID to link"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Evaluate pronunciation from mini program audio upload."""
    if whisper_service.status != "ready":
        raise HTTPException(status_code=503, detail=f"Whisper model is not ready (status: {whisper_service.status})")

    if not target_text.strip():
        raise HTTPException(status_code=400, detail="target_text cannot be empty")

    filename = audio.filename or "recording.mp3"
    ext = os.path.splitext(filename)[1].lower()
    if ext not in SUPPORTED_FORMATS:
        raise HTTPException(status_code=400, detail=f"Unsupported audio format '{ext}'. Supported: {', '.join(SUPPORTED_FORMATS)}")

    content = await audio.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Uploaded audio file is empty")
    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail=f"File too large. Maximum size: {MAX_UPLOAD_SIZE // (1024 * 1024)}MB")

    input_path = None
    wav_path = None

    try:
        input_path = save_upload_file(content, filename)
        wav_path = convert_to_wav(input_path)
        transcription = whisper_service.transcribe(wav_path)
        recognized_text = transcription["text"]
        segments = transcription.get("segments", [])
        result = evaluate_pronunciation(target_text, recognized_text, segments)

        history = EvaluationHistory(
            user_id=current_user.id,
            practice_id=practice_id,
            target_text=target_text,
            recognized_text=recognized_text,
            accuracy=result["scores"]["accuracy"],
            completeness=result["scores"]["completeness"],
            fluency=result["scores"]["fluency"],
            overall_score=result["scores"]["overall"],
            word_comparison=[wc for wc in result["word_comparison"]],
        )
        db.add(history)
        await db.flush()

        return EvaluationResult(**result)

    except RuntimeError as e:
        logger.error(f"WX Evaluation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"WX Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        files_to_clean = [input_path]
        if wav_path and wav_path != input_path:
            files_to_clean.append(wav_path)
        cleanup_files(*files_to_clean)
