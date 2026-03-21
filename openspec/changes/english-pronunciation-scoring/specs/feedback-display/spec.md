## ADDED Requirements

### Requirement: Score dashboard
The frontend SHALL display evaluation results in a visual dashboard showing: overall score (large, prominent), individual dimension scores (accuracy, completeness, fluency), and a score level label (Excellent/Good/Fair/Poor).

#### Scenario: Display overall score
- **WHEN** evaluation results are received from the backend
- **THEN** the system SHALL display the overall score (0-100) with a color-coded indicator (green >= 80, yellow >= 60, orange >= 40, red < 40)

#### Scenario: Score level label
- **WHEN** overall score >= 90
- **THEN** the system SHALL display "Excellent"
- **WHEN** overall score >= 70
- **THEN** the system SHALL display "Good"
- **WHEN** overall score >= 50
- **THEN** the system SHALL display "Fair"
- **WHEN** overall score < 50
- **THEN** the system SHALL display "Poor"

### Requirement: Word-level comparison view
The frontend SHALL display a word-by-word comparison between the target text and the user's pronunciation, with color-coded highlighting.

#### Scenario: Correct word display
- **WHEN** a word is marked as `correct` in the alignment result
- **THEN** the word SHALL be displayed in green

#### Scenario: Incorrect word display
- **WHEN** a word is marked as `incorrect` in the alignment result
- **THEN** the target word SHALL be displayed in red with the recognized word shown below it

#### Scenario: Missing word display
- **WHEN** a word is marked as `missing` in the alignment result
- **THEN** the target word SHALL be displayed in orange with a strikethrough or "skipped" indicator

#### Scenario: Extra word display
- **WHEN** a word is marked as `extra` in the alignment result
- **THEN** the extra word SHALL be displayed in gray with an indicator that it was not in the target

### Requirement: Loading state
The frontend SHALL display a loading spinner or progress indicator while the backend processes the audio evaluation.

#### Scenario: Loading indicator during evaluation
- **WHEN** audio is uploaded and evaluation is in progress
- **THEN** the system SHALL display a loading indicator with a message like "Analyzing your pronunciation..."

#### Scenario: Loading complete
- **WHEN** evaluation results are received
- **THEN** the loading indicator SHALL be replaced by the score dashboard and word comparison view

### Requirement: Try again flow
The frontend SHALL allow users to immediately try the same practice again after viewing results.

#### Scenario: Try again button
- **WHEN** evaluation results are displayed
- **THEN** a "Try Again" button SHALL be visible, and clicking it SHALL reset the recording state while keeping the same target text
