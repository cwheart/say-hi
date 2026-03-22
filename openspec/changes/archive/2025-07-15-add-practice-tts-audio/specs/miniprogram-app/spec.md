## MODIFIED Requirements

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

## ADDED Requirements

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