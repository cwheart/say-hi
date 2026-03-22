
### Requirement: Mini program app structure
The application SHALL use a uni-app (Vue 3 + Vite + TypeScript) project structure in the `uniapp/src/` directory with pages as `.vue` Single File Components, replacing the original WeChat native mini program structure.

#### Scenario: App initialization
- **WHEN** the application launches
- **THEN** the system SHALL check for stored token, attempt platform-appropriate login if no token (wx.login on MP-WEIXIN, redirect to login page on H5), and navigate to the index page

### Requirement: Index page - practice library
The application SHALL provide an index page displaying categorized practice items.

#### Scenario: Display practice categories
- **WHEN** user opens the index page
- **THEN** the system SHALL display practice items grouped by category (word, phrase, sentence) with difficulty badges

#### Scenario: Filter by category
- **WHEN** user taps a category tab
- **THEN** the system SHALL filter and display only practices of that category

#### Scenario: Navigate to practice
- **WHEN** user taps a practice item
- **THEN** the system SHALL navigate to the practice page with the practice ID via `uni.navigateTo`

### Requirement: Practice page - recording and submission
The application SHALL provide a practice page where users can listen to standard pronunciation, record their own pronunciation, and submit for evaluation.

#### Scenario: Display target text with audio button
- **WHEN** user navigates to the practice page and the practice has an `audio_url`
- **THEN** the system SHALL display the target text with a 🔊 speaker icon button next to it

#### Scenario: Hide audio button when no audio
- **WHEN** user navigates to the practice page and the practice has no `audio_url` (null)
- **THEN** the system SHALL display the target text without the speaker icon button

#### Scenario: Play standard pronunciation
- **WHEN** user taps the 🔊 speaker icon button
- **THEN** the system SHALL play the audio from the practice's `audio_url` using the platform-appropriate audio player (uni.createInnerAudioContext on MP-WEIXIN, new Audio on H5)

#### Scenario: Stop audio playback
- **WHEN** user taps the speaker icon while audio is playing
- **THEN** the system SHALL stop the audio playback

#### Scenario: Audio playback visual feedback
- **WHEN** the standard pronunciation audio is playing
- **THEN** the speaker icon SHALL display an animated/active state to indicate playback

#### Scenario: Audio playback error
- **WHEN** the audio file fails to load or play
- **THEN** the system SHALL display a toast message "播放失败" and reset the button state

#### Scenario: Display target text
- **WHEN** user navigates to the practice page
- **THEN** the system SHALL display the target text, difficulty, category, hint (if any), and best score (if any)

#### Scenario: Start recording
- **WHEN** user taps the record button
- **THEN** the system SHALL start recording via the platform-appropriate recorder (uni.getRecorderManager on MP-WEIXIN, MediaRecorder on H5)

#### Scenario: Stop recording
- **WHEN** user taps the stop button or recording reaches max duration (30 seconds)
- **THEN** the system SHALL stop recording and enable the submit button

#### Scenario: Submit evaluation
- **WHEN** user taps the submit button
- **THEN** the system SHALL upload the audio file via the platform-appropriate upload method to `/api/wx/evaluate` and navigate to the result page

#### Scenario: Recording permission denied
- **WHEN** the user has not granted microphone permission
- **THEN** the system SHALL prompt the user to enable microphone access in settings

### Requirement: Result page - score display
The application SHALL provide a result page showing evaluation scores and word-by-word comparison.

#### Scenario: Display scores
- **WHEN** the result page receives evaluation data
- **THEN** the system SHALL display overall score, accuracy, completeness, fluency as progress bars with color coding

#### Scenario: Word comparison
- **WHEN** evaluation data includes word_comparison
- **THEN** the system SHALL display each word with color coding: green (correct), red (incorrect), orange (missing), gray (extra)

#### Scenario: Try again
- **WHEN** user taps "Try Again" button
- **THEN** the system SHALL navigate back to the practice page

### Requirement: History page
The application SHALL provide a page showing the user's past evaluation attempts.

#### Scenario: Display history list
- **WHEN** user navigates to the history page
- **THEN** the system SHALL display a scrollable list of past evaluations with target text, overall score, and date

#### Scenario: Load more
- **WHEN** user scrolls to the bottom of the history list
- **THEN** the system SHALL load the next page of history items

#### Scenario: Empty history
- **WHEN** user has no evaluation history
- **THEN** the system SHALL display a message "No practice history yet"

### Requirement: Profile page
The application SHALL provide a profile page showing user info and app settings.

#### Scenario: Display profile
- **WHEN** user navigates to the profile page
- **THEN** the system SHALL display the user's nickname (or "WeChat User" on MP-WEIXIN, email on H5) and total practice count

### Requirement: Cross-platform audio player utility
The application SHALL provide a `src/utils/audio-player.ts` utility for cross-platform audio playback.

#### Scenario: Play audio on MP-WEIXIN
- **WHEN** the audio player is invoked on MP-WEIXIN with a URL
- **THEN** the system SHALL use `uni.createInnerAudioContext()` to play the audio

#### Scenario: Play audio on H5
- **WHEN** the audio player is invoked on H5 with a URL
- **THEN** the system SHALL use `new Audio(url)` to play the audio

#### Scenario: Stop current playback
- **WHEN** the stop method is called
- **THEN** the system SHALL stop the currently playing audio and release resources

#### Scenario: Playback state callbacks
- **WHEN** the audio player is initialized
- **THEN** the system SHALL support `onPlay`, `onStop`, and `onError` callbacks

### Requirement: Tab bar navigation
The application SHALL provide a bottom tab bar for navigation between main pages.

#### Scenario: Tab bar display
- **WHEN** the application is open
- **THEN** the system SHALL display a bottom tab bar with: Practice (index), History, Profile


### Requirement: WeChat native project files
**Reason**: Replaced by uni-app project structure. Original `miniprogram/` directory with `app.json`, `app.js`, `app.wxss`, `project.config.json`, `sitemap.json`, and all `.wxml`/`.wxss`/`.js` page/component files are no longer needed.
**Migration**: All functionality is reimplemented as Vue 3 SFC files in `uniapp/src/`. Delete the `miniprogram/` directory after migration.
