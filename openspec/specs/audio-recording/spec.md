
### Requirement: Mini program audio recording
The application SHALL record audio using a platform-adaptive recorder: `uni.getRecorderManager()` on MP-WEIXIN and Web `MediaRecorder` API on H5, both optimized for Whisper recognition.

#### Scenario: Recording configuration (MP-WEIXIN)
- **WHEN** the recorder is initialized on MP-WEIXIN
- **THEN** the system SHALL configure `uni.getRecorderManager()` with: format=mp3, sampleRate=16000, numberOfChannels=1, encodeBitRate=48000

#### Scenario: Recording configuration (H5)
- **WHEN** the recorder is initialized on H5
- **THEN** the system SHALL use `navigator.mediaDevices.getUserMedia({ audio: true })` and create a `MediaRecorder` with `audio/webm;codecs=opus` mime type

#### Scenario: Recording start
- **WHEN** user triggers recording
- **THEN** the system SHALL call the platform-appropriate start method and show a recording indicator

#### Scenario: Recording stop
- **WHEN** user triggers stop or max duration (30s) is reached
- **THEN** the system SHALL stop recording and provide the recorded audio (temp file path on MP-WEIXIN, Blob on H5)

#### Scenario: Recording error
- **WHEN** a recording error occurs
- **THEN** the system SHALL display an error toast and reset the recording state

### Requirement: Mini program audio upload
The application SHALL upload recorded audio to the backend using a platform-adaptive method: `uni.uploadFile()` on MP-WEIXIN and `FormData` + `fetch` on H5.

#### Scenario: Upload audio for evaluation (MP-WEIXIN)
- **WHEN** user submits a recording on MP-WEIXIN
- **THEN** the system SHALL use `uni.uploadFile()` to POST the audio file to `/api/wx/evaluate` with the JWT token in the header

#### Scenario: Upload audio for evaluation (H5)
- **WHEN** user submits a recording on H5
- **THEN** the system SHALL create a `FormData` with the audio Blob and POST to `/api/wx/evaluate` using `fetch` with the JWT token in the Authorization header

#### Scenario: Upload with practice ID
- **WHEN** the recording is for a specific practice
- **THEN** the upload form data SHALL include `practice_id` and `target_text` fields
