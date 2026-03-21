## ADDED Requirements

### Requirement: Mini program app structure
The mini program SHALL follow the standard WeChat mini program project structure with pages, components, and utils directories.

#### Scenario: App initialization
- **WHEN** the mini program launches
- **THEN** the system SHALL check for stored token, attempt silent login if no token, and navigate to the index page

### Requirement: Index page - practice library
The mini program SHALL provide an index page displaying categorized practice items.

#### Scenario: Display practice categories
- **WHEN** user opens the mini program index page
- **THEN** the system SHALL display practice items grouped by category (word, phrase, sentence) with difficulty badges

#### Scenario: Filter by category
- **WHEN** user taps a category tab
- **THEN** the system SHALL filter and display only practices of that category

#### Scenario: Navigate to practice
- **WHEN** user taps a practice item
- **THEN** the system SHALL navigate to the practice page with the practice ID

### Requirement: Practice page - recording and submission
The mini program SHALL provide a practice page where users record their pronunciation and submit for evaluation.

#### Scenario: Display target text
- **WHEN** user navigates to the practice page
- **THEN** the system SHALL display the target text, difficulty, category, hint (if any), and best score (if any)

#### Scenario: Start recording
- **WHEN** user taps the record button
- **THEN** the system SHALL start recording via wx.getRecorderManager() with mp3 format, 16000Hz sample rate, mono channel

#### Scenario: Stop recording
- **WHEN** user taps the stop button or recording reaches max duration (30 seconds)
- **THEN** the system SHALL stop recording and enable the submit button

#### Scenario: Submit evaluation
- **WHEN** user taps the submit button
- **THEN** the system SHALL upload the audio file via wx.uploadFile() to `/api/wx/evaluate` and navigate to the result page

#### Scenario: Recording permission denied
- **WHEN** the user has not granted microphone permission
- **THEN** the system SHALL prompt the user to enable microphone access in settings

### Requirement: Result page - score display
The mini program SHALL provide a result page showing evaluation scores and word-by-word comparison.

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
The mini program SHALL provide a page showing the user's past evaluation attempts.

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
The mini program SHALL provide a profile page showing user info and app settings.

#### Scenario: Display profile
- **WHEN** user navigates to the profile page
- **THEN** the system SHALL display the user's nickname (or "WeChat User") and total practice count

### Requirement: Tab bar navigation
The mini program SHALL provide a bottom tab bar for navigation between main pages.

#### Scenario: Tab bar display
- **WHEN** the mini program is open
- **THEN** the system SHALL display a bottom tab bar with: Practice (index), History, Profile
