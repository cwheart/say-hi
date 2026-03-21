## ADDED Requirements

### Requirement: Browser audio recording
The system SHALL provide audio recording capability in the browser using the MediaRecorder API. Users SHALL be able to start, stop, and re-record their pronunciation.

#### Scenario: Start recording
- **WHEN** user clicks the "Record" button
- **THEN** system SHALL request microphone permission (if not already granted) and begin recording audio

#### Scenario: Stop recording
- **WHEN** user clicks the "Stop" button during an active recording
- **THEN** system SHALL stop recording and store the audio blob in memory for playback and upload

#### Scenario: Playback recorded audio
- **WHEN** user clicks the "Play" button after recording
- **THEN** system SHALL play back the recorded audio through the browser

#### Scenario: Re-record audio
- **WHEN** user clicks the "Re-record" button after a recording exists
- **THEN** system SHALL discard the previous recording and start a new recording session

#### Scenario: Microphone permission denied
- **WHEN** user denies microphone permission
- **THEN** system SHALL display a clear error message explaining that microphone access is required

### Requirement: Recording time limit
The system SHALL enforce a maximum recording duration of 30 seconds to control upload file size.

#### Scenario: Maximum duration reached
- **WHEN** recording reaches 30 seconds
- **THEN** system SHALL automatically stop recording and display a notification that the time limit was reached

### Requirement: Audio upload
The system SHALL upload the recorded audio file to the backend API as multipart/form-data along with the target reference text.

#### Scenario: Successful upload
- **WHEN** user submits a recording for evaluation
- **THEN** system SHALL send the audio blob and target text to the `/api/evaluate` endpoint and display a loading indicator

#### Scenario: Upload failure
- **WHEN** the upload request fails (network error or server error)
- **THEN** system SHALL display an error message and allow the user to retry

### Requirement: Browser compatibility check
The system SHALL detect whether the browser supports the MediaRecorder API on page load.

#### Scenario: Unsupported browser
- **WHEN** user opens the application in a browser that does not support MediaRecorder API
- **THEN** system SHALL display a message recommending a supported browser (Chrome, Firefox, Edge)
