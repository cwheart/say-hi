## CHANGED Requirements

### Requirement: Authenticated evaluation
The `/api/evaluate` endpoint SHALL require JWT authentication and include optional practice_id.

#### Scenario: Authenticated submission
- **WHEN** a POST request to `/api/evaluate` includes a valid JWT token
- **THEN** the system SHALL process the evaluation and associate the result with the authenticated user

#### Scenario: Unauthenticated submission
- **WHEN** a POST request to `/api/evaluate` lacks a valid JWT token
- **THEN** the system SHALL return HTTP 401

#### Scenario: Practice ID parameter
- **WHEN** the evaluation form data includes an optional `practice_id` field
- **THEN** the system SHALL link the evaluation record to the specified practice
