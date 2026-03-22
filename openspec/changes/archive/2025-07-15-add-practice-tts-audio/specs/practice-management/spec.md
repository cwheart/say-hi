## MODIFIED Requirements

### Requirement: Admin practice CRUD operations
The practice management service SHALL support create, update, and delete operations for admin users, with automatic TTS audio generation on create and text update.

#### Scenario: Create practice with TTS
- **WHEN** the practice service receives a create request with text, category, difficulty, and optional hint
- **THEN** it SHALL generate a slug-based ID, insert the record into the database, trigger TTS audio generation asynchronously, and return the created practice

#### Scenario: Update practice with TTS regeneration
- **WHEN** the practice service receives an update request and the `text` field has changed
- **THEN** it SHALL update the record, trigger TTS audio regeneration asynchronously, and return the updated practice

#### Scenario: Update practice without text change
- **WHEN** the practice service receives an update request where the `text` field has NOT changed
- **THEN** it SHALL update the record without triggering TTS audio regeneration

#### Scenario: Delete practice with audio cleanup
- **WHEN** the practice service receives a delete request with a practice ID
- **THEN** it SHALL delete the record from the database and delete the associated audio file if it exists

### Requirement: Practice data model includes audio_url
The Practice response SHALL include the `audio_url` field indicating the URL of the generated pronunciation audio.

#### Scenario: Practice response with audio
- **WHEN** a client requests practice data and the practice has a generated audio file
- **THEN** the response SHALL include `audio_url` with the value `/api/audio/{practice_id}.mp3`

#### Scenario: Practice response without audio
- **WHEN** a client requests practice data and the practice has no generated audio
- **THEN** the response SHALL include `audio_url` with a null value