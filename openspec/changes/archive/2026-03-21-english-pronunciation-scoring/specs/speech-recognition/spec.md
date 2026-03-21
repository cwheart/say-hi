## ADDED Requirements

### Requirement: Whisper model loading
The backend SHALL load the OpenAI Whisper model at application startup. The model size SHALL be configurable via the `WHISPER_MODEL` environment variable (default: `base`).

#### Scenario: Successful model loading
- **WHEN** the FastAPI application starts
- **THEN** the Whisper model SHALL be loaded into memory and ready to process requests

#### Scenario: Model loading status
- **WHEN** a client sends GET request to `/api/health`
- **THEN** the system SHALL respond with model loading status (`loading`, `ready`, or `error`)

### Requirement: Audio-to-text transcription
The backend SHALL accept audio file uploads and transcribe them to English text using the Whisper model. The system SHALL support WebM, WAV, MP3, and OGG audio formats.

#### Scenario: Successful transcription
- **WHEN** a valid audio file is uploaded to `/api/evaluate`
- **THEN** the system SHALL transcribe the audio to English text and include the transcribed text in the response

#### Scenario: Audio format conversion
- **WHEN** the uploaded audio is not in WAV format
- **THEN** the system SHALL convert it to WAV using ffmpeg before passing it to Whisper

#### Scenario: Invalid audio file
- **WHEN** an invalid or corrupted audio file is uploaded
- **THEN** the system SHALL return HTTP 400 with a descriptive error message

#### Scenario: Empty audio
- **WHEN** an audio file contains no detectable speech
- **THEN** the system SHALL return the transcription result as empty string and scoring SHALL reflect zero accuracy

### Requirement: Whisper language enforcement
The system SHALL configure Whisper to only recognize English language input to improve accuracy for English pronunciation evaluation.

#### Scenario: English language setting
- **WHEN** Whisper processes an audio file
- **THEN** the language parameter SHALL be set to "en" (English)
