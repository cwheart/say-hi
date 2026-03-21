## ADDED Requirements

### Requirement: Multi-dimension scoring
The system SHALL evaluate pronunciation across three dimensions and return a score (0-100) for each:
- **Accuracy**: Percentage of correctly pronounced words
- **Completeness**: Percentage of target words that were spoken
- **Fluency**: Estimated based on Whisper confidence and speech characteristics

#### Scenario: Perfect pronunciation
- **WHEN** the transcribed text exactly matches the target text (case-insensitive, punctuation-ignored)
- **THEN** accuracy SHALL be 100, completeness SHALL be 100, and fluency SHALL be >= 80

#### Scenario: Partial match
- **WHEN** the transcribed text partially matches the target text
- **THEN** accuracy and completeness scores SHALL reflect the proportion of matching words

#### Scenario: No match
- **WHEN** the transcribed text has no words matching the target text
- **THEN** accuracy SHALL be 0, completeness SHALL be 0

### Requirement: Overall score calculation
The system SHALL compute an overall score as a weighted average: Accuracy (50%) + Completeness (30%) + Fluency (20%).

#### Scenario: Overall score calculation
- **WHEN** individual dimension scores are computed
- **THEN** the overall score SHALL be calculated as `accuracy * 0.5 + completeness * 0.3 + fluency * 0.2`, rounded to the nearest integer

### Requirement: Word-level alignment
The system SHALL perform word-level alignment between the target text and the transcribed text using Levenshtein distance to identify correct, incorrect, missing, and extra words.

#### Scenario: Word alignment output
- **WHEN** evaluation is complete
- **THEN** the response SHALL include a word-level comparison array where each entry contains: the target word, the recognized word (or null if missing), and a status (`correct`, `incorrect`, `missing`, `extra`)

### Requirement: Text normalization
The system SHALL normalize both target and transcribed text before comparison by: converting to lowercase, removing punctuation, and trimming whitespace.

#### Scenario: Case-insensitive comparison
- **WHEN** target text is "Hello World" and transcribed text is "hello world"
- **THEN** the comparison SHALL treat them as a perfect match

#### Scenario: Punctuation-insensitive comparison
- **WHEN** target text contains punctuation like "Hello, world!"
- **THEN** the comparison SHALL ignore punctuation marks
