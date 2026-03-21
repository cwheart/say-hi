## ADDED Requirements

### Requirement: Save evaluation results
The system SHALL persist every pronunciation evaluation result to the evaluation_history table, associated with the authenticated user.

#### Scenario: Evaluation saved after scoring
- **WHEN** a successful evaluation is completed via POST `/api/evaluate`
- **THEN** the system SHALL save the result (scores, recognized text, word comparison) to evaluation_history with the current user's ID

#### Scenario: Evaluation linked to practice
- **WHEN** the evaluation request includes a practice_id parameter
- **THEN** the saved record SHALL include a foreign key reference to the practice

#### Scenario: Evaluation without practice
- **WHEN** the evaluation request does not include a practice_id (custom text)
- **THEN** the saved record SHALL have practice_id set to NULL

### Requirement: View evaluation history
The system SHALL provide API endpoints to query the current user's evaluation history.

#### Scenario: List history
- **WHEN** an authenticated user sends GET to `/api/history`
- **THEN** the system SHALL return a paginated list of their evaluation records, ordered by created_at descending

#### Scenario: Pagination
- **WHEN** the request includes `page` and `page_size` query parameters
- **THEN** the system SHALL return the corresponding page of results with total count

#### Scenario: View single record
- **WHEN** an authenticated user sends GET to `/api/history/{id}`
- **THEN** the system SHALL return the full evaluation record including word_comparison

#### Scenario: Access control
- **WHEN** a user attempts to view another user's evaluation record
- **THEN** the system SHALL return HTTP 404

### Requirement: Frontend history page
The frontend SHALL provide a page to view past practice results.

#### Scenario: History list page
- **WHEN** an authenticated user navigates to `/history`
- **THEN** the system SHALL display a list of past evaluations with date, target text, overall score, and a link to details

#### Scenario: Best score display
- **WHEN** viewing a practice detail page for a practice the user has attempted before
- **THEN** the system SHALL display the user's best score for that practice
