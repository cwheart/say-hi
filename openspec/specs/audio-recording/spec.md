## CHANGED Requirements

### Requirement: Authenticated evaluation
The `/api/evaluate` and `/api/wx/evaluate` endpoints SHALL require JWT authentication and support audio from both web and mini program clients.

#### Scenario: Web client submission
- **WHEN** a POST request to `/api/evaluate` includes a valid JWT token and webm audio
- **THEN** the system SHALL process the evaluation using ffmpeg conversion and Whisper

#### Scenario: Mini program submission
- **WHEN** a POST request to `/api/wx/evaluate` includes a valid JWT token and mp3 audio
- **THEN** the system SHALL process the evaluation using ffmpeg conversion and Whisper

#### Scenario: Unauthenticated submission
- **WHEN** a POST request to any evaluate endpoint lacks a valid JWT token
- **THEN** the system SHALL return HTTP 401

#### Scenario: Practice ID parameter
- **WHEN** the evaluation form data includes an optional `practice_id` field
- **THEN** the system SHALL link the evaluation record to the specified practice

### Requirement: Mini program audio recording
The mini program SHALL record audio using wx.getRecorderManager() with settings optimized for Whisper recognition.

#### Scenario: Recording configuration
- **WHEN** the recorder is initialized
- **THEN** the system SHALL configure: format=mp3, sampleRate=16000, numberOfChannels=1, encodeBitRate=48000

#### Scenario: Recording start
- **WHEN** user triggers recording
- **THEN** the system SHALL call recorderManager.start() and show a recording indicator

#### Scenario: Recording stop
- **WHEN** user triggers stop or max duration (30s) is reached
- **THEN** the system SHALL stop recording and provide the temp file path

#### Scenario: Recording error
- **WHEN** a recording error occurs
- **THEN** the system SHALL display an error toast and reset the recording state

### Requirement: Mini program audio upload
The mini program SHALL upload recorded audio to the backend using wx.uploadFile().

#### Scenario: Upload audio for evaluation
- **WHEN** user submits a recording
- **THEN** the system SHALL use wx.uploadFile() to POST the audio file to `/api/wx/evaluate` with the JWT token in the header

#### Scenario: Upload with practice ID
- **WHEN** the recording is for a specific practice
- **THEN** the upload form data SHALL include `practice_id` and `target_text` fields