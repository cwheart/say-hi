import logging
import os
import subprocess
import tempfile
import uuid

logger = logging.getLogger(__name__)

# Supported input audio formats
SUPPORTED_FORMATS = {".webm", ".ogg", ".mp3", ".wav", ".m4a", ".flac"}


def get_temp_dir() -> str:
    """Get or create the temporary directory for audio processing."""
    temp_dir = os.getenv("TEMP_DIR", os.path.join(tempfile.gettempdir(), "say-hi"))
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir


def save_upload_file(file_bytes: bytes, original_filename: str) -> str:
    """
    Save uploaded file to a temporary location.

    Args:
        file_bytes: Raw file bytes.
        original_filename: Original filename from the upload.

    Returns:
        Path to the saved temporary file.
    """
    temp_dir = get_temp_dir()
    ext = os.path.splitext(original_filename)[1].lower() or ".webm"
    filename = f"{uuid.uuid4()}{ext}"
    filepath = os.path.join(temp_dir, filename)

    with open(filepath, "wb") as f:
        f.write(file_bytes)

    logger.info(f"Saved upload file: {filepath} ({len(file_bytes)} bytes)")
    return filepath


def convert_to_wav(input_path: str) -> str:
    """
    Convert an audio file to WAV format using ffmpeg.

    If the input is already WAV, returns the same path.

    Args:
        input_path: Path to the input audio file.

    Returns:
        Path to the WAV file.

    Raises:
        RuntimeError: If ffmpeg conversion fails.
    """
    if input_path.lower().endswith(".wav"):
        return input_path

    temp_dir = get_temp_dir()
    output_path = os.path.join(temp_dir, f"{uuid.uuid4()}.wav")

    try:
        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-ar", "16000",       # 16kHz sample rate (Whisper preferred)
            "-ac", "1",           # Mono channel
            "-sample_fmt", "s16", # 16-bit PCM
            "-y",                 # Overwrite output
            output_path,
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            logger.error(f"ffmpeg error: {result.stderr}")
            raise RuntimeError(f"Audio conversion failed: {result.stderr}")

        logger.info(f"Converted {input_path} -> {output_path}")
        return output_path

    except subprocess.TimeoutExpired:
        raise RuntimeError("Audio conversion timed out")
    except FileNotFoundError:
        raise RuntimeError(
            "ffmpeg not found. Please install ffmpeg: https://ffmpeg.org/download.html"
        )


def cleanup_files(*paths: str) -> None:
    """Remove temporary files."""
    for path in paths:
        try:
            if path and os.path.exists(path):
                os.remove(path)
                logger.debug(f"Cleaned up: {path}")
        except OSError as e:
            logger.warning(f"Failed to cleanup {path}: {e}")
