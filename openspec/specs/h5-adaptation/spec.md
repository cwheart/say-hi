
### Requirement: H5 audio recording via Web MediaRecorder
The H5 platform SHALL record audio using the Web `MediaRecorder` API as a replacement for the WeChat-only `uni.getRecorderManager`.

#### Scenario: H5 recording initialization
- **WHEN** the recorder module is loaded on the H5 platform
- **THEN** the system SHALL use `navigator.mediaDevices.getUserMedia({ audio: true })` to acquire a media stream

#### Scenario: H5 recording start
- **WHEN** the user triggers recording on H5
- **THEN** the system SHALL create a `MediaRecorder` instance with `audio/webm;codecs=opus` mime type and call `start()`

#### Scenario: H5 recording stop
- **WHEN** the user triggers stop or max duration (30s) is reached on H5
- **THEN** the system SHALL call `MediaRecorder.stop()`, collect the recorded `Blob`, and provide it for upload

#### Scenario: H5 recording error
- **WHEN** a recording error occurs on H5 (e.g., microphone denied, API unsupported)
- **THEN** the system SHALL display a toast message and reset the recording state

#### Scenario: H5 MediaRecorder not supported
- **WHEN** the browser does not support `navigator.mediaDevices` or `MediaRecorder`
- **THEN** the system SHALL display a message "请使用现代浏览器或微信小程序进行录音"

### Requirement: H5 audio upload via fetch
The H5 platform SHALL upload recorded audio using `FormData` + `fetch` (or `XMLHttpRequest`) as a replacement for `uni.uploadFile`.

#### Scenario: H5 audio upload
- **WHEN** the user submits a recording on H5
- **THEN** the system SHALL create a `FormData` with the audio `Blob` (named `audio`), `practice_id`, and `target_text`, then POST to `/api/wx/evaluate` with the JWT token in the Authorization header

#### Scenario: H5 upload progress
- **WHEN** the audio file is being uploaded on H5
- **THEN** the system SHALL display a loading indicator until the server responds

### Requirement: H5 login flow
The H5 platform SHALL provide an email/password login form as a replacement for the WeChat `wx.login` silent login.

#### Scenario: H5 login page display
- **WHEN** the user opens the H5 app without a valid stored token
- **THEN** the system SHALL display a login form with email and password fields

#### Scenario: H5 login submission
- **WHEN** the user submits valid email and password on H5
- **THEN** the system SHALL POST to `/api/auth/login`, store the returned JWT token in `localStorage`, and redirect to the index page

#### Scenario: H5 login failure
- **WHEN** the user submits invalid credentials on H5
- **THEN** the system SHALL display an error message "邮箱或密码错误"

#### Scenario: H5 token persistence
- **WHEN** the user successfully logs in on H5
- **THEN** the system SHALL store the JWT token in `localStorage` and use it for subsequent API requests

#### Scenario: H5 auto-redirect on 401
- **WHEN** an H5 API request returns HTTP 401
- **THEN** the system SHALL clear the stored token and redirect the user to the login page

### Requirement: Platform adapter layer
The system SHALL provide a unified `platform.ts` utility that abstracts platform-specific operations behind a common interface.

#### Scenario: Recorder adapter
- **WHEN** any page calls the recorder module
- **THEN** the module SHALL use `uni.getRecorderManager()` on MP-WEIXIN and `MediaRecorder` on H5 via conditional compilation

#### Scenario: Upload adapter
- **WHEN** any page calls the upload module
- **THEN** the module SHALL use `uni.uploadFile()` on MP-WEIXIN and `FormData` + `fetch` on H5 via conditional compilation

#### Scenario: Auth adapter
- **WHEN** any page calls the auth module
- **THEN** the module SHALL use `uni.login()` flow on MP-WEIXIN and email/password login on H5 via conditional compilation
