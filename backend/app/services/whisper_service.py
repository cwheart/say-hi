import logging
from typing import Optional

import whisper
import numpy as np

logger = logging.getLogger(__name__)


class WhisperService:
    """Service for loading and using the OpenAI Whisper model."""

    def __init__(self):
        self.model: Optional[whisper.Whisper] = None
        self.model_name: str = "base"
        self.status: str = "not_loaded"  # not_loaded, loading, ready, error

    def load_model(self, model_name: str = "base") -> None:
        """Load the Whisper model into memory."""
        self.model_name = model_name
        self.status = "loading"
        try:
            logger.info(f"Loading Whisper model: {model_name}")
            self.model = whisper.load_model(model_name)
            self.status = "ready"
            logger.info(f"Whisper model '{model_name}' loaded successfully")
        except Exception as e:
            self.status = "error"
            logger.error(f"Failed to load Whisper model: {e}")
            raise

    def transcribe(self, audio_path: str) -> dict:
        """
        Transcribe an audio file to English text.

        Args:
            audio_path: Path to the audio file (WAV format preferred).

        Returns:
            dict with keys:
                - text: The transcribed text
                - segments: List of segment dicts with timing and confidence info
                - language: Detected language
        """
        if self.model is None or self.status != "ready":
            raise RuntimeError("Whisper model is not loaded")

        try:
            result = self.model.transcribe(
                audio_path,
                language="en",
                fp16=False,  # Use fp32 for CPU compatibility
            )
            return {
                "text": result.get("text", "").strip(),
                "segments": result.get("segments", []),
                "language": result.get("language", "en"),
            }
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise

    def cleanup(self) -> None:
        """Release model resources."""
        self.model = None
        self.status = "not_loaded"
        logger.info("Whisper model unloaded")


# Singleton instance
whisper_service = WhisperService()
