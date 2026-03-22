## ADDED Requirements

### Requirement: TTS audio generation service
The system SHALL provide a TTS service that generates English pronunciation audio files using Edge TTS (`edge-tts` Python package) with the `en-US-AriaNeural` voice.

#### Scenario: Generate audio for text
- **WHEN** the TTS service receives a text string and a practice ID
- **THEN** the system SHALL generate an MP3 audio file using Edge TTS and save it to `backend/audio/{practice_id}.mp3`

#### Scenario: Generate audio successfully
- **WHEN** Edge TTS successfully generates audio
- **THEN** the system SHALL return the relative URL `/api/audio/{practice_id}.mp3`

#### Scenario: Generate audio failure
- **WHEN** Edge TTS fails (network error, service unavailable)
- **THEN** the system SHALL log the error and return null without raising an exception

#### Scenario: Regenerate existing audio
- **WHEN** the TTS service is called for a practice ID that already has an audio file
- **THEN** the system SHALL overwrite the existing file with the newly generated audio

### Requirement: Audio file storage
The system SHALL store generated TTS audio files in a local `backend/audio/` directory.

#### Scenario: Audio directory initialization
- **WHEN** the TTS service is first invoked
- **THEN** the system SHALL create the `backend/audio/` directory if it does not exist

#### Scenario: Audio file naming
- **WHEN** an audio file is generated for a practice
- **THEN** the file SHALL be named `{practice_id}.mp3`

### Requirement: Audio static file serving
The system SHALL serve audio files via FastAPI StaticFiles mounted at `/api/audio/`.

#### Scenario: Access audio file
- **WHEN** a GET request is sent to `/api/audio/{practice_id}.mp3`
- **THEN** the system SHALL return the MP3 file with appropriate content-type header

#### Scenario: Audio file not found
- **WHEN** a GET request is sent to `/api/audio/{filename}` for a non-existent file
- **THEN** the system SHALL return HTTP 404

### Requirement: Admin regenerate audio endpoint
The system SHALL provide an admin endpoint to manually regenerate audio for a specific practice.

#### Scenario: Regenerate audio
- **WHEN** a POST request is sent to `/api/admin/practices/{id}/regenerate-audio` with admin JWT
- **THEN** the system SHALL regenerate the TTS audio for the specified practice and update the `audio_url` in the database

#### Scenario: Regenerate audio for non-existent practice
- **WHEN** a POST request is sent to `/api/admin/practices/{id}/regenerate-audio` for a non-existent practice
- **THEN** the system SHALL return HTTP 404

### Requirement: Batch audio generation
The system SHALL support batch generation of audio files for all practices that lack audio.

#### Scenario: Seed script generates audio
- **WHEN** the seed script runs and practices are inserted
- **THEN** the system SHALL generate TTS audio for each inserted practice with a delay between generations to avoid rate limiting

#### Scenario: Batch generation with delay
- **WHEN** multiple audio files are generated in sequence
- **THEN** the system SHALL wait at least 200ms between each generation
