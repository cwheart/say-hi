import logging
import os
from pathlib import Path
from typing import Optional

import edge_tts

logger = logging.getLogger(__name__)

# Audio storage directory
AUDIO_DIR = Path(__file__).parent.parent.parent / "audio"

# TTS voice
VOICE = "en-US-AriaNeural"


def _get_audio_path(practice_id: str) -> Path:
    """Get the file path for a practice's audio."""
    return AUDIO_DIR / f"{practice_id}.mp3"


def _get_audio_url(practice_id: str) -> str:
    """Get the relative URL for a practice's audio."""
    return f"/api/audio/{practice_id}.mp3"


async def generate_audio(text: str, practice_id: str) -> Optional[str]:
    """
    Generate TTS audio for the given text and save as MP3.

    Returns the audio URL on success, None on failure.
    Does NOT raise exceptions — logs errors and returns None.
    """
    try:
        # Ensure audio directory exists
        AUDIO_DIR.mkdir(parents=True, exist_ok=True)

        output_path = _get_audio_path(practice_id)

        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(str(output_path))

        audio_url = _get_audio_url(practice_id)
        logger.info(f"TTS audio generated: {audio_url} for text: '{text[:50]}...'")
        return audio_url

    except Exception as e:
        logger.error(f"TTS generation failed for practice '{practice_id}': {type(e).__name__}: {e}", exc_info=True)
        return None


def delete_audio(practice_id: str) -> bool:
    """
    Delete the audio file for a practice if it exists.

    Returns True if file was deleted, False otherwise.
    """
    try:
        audio_path = _get_audio_path(practice_id)
        if audio_path.exists():
            audio_path.unlink()
            logger.info(f"Deleted audio file: {audio_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to delete audio for practice '{practice_id}': {e}")
        return False