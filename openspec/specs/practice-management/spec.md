## CHANGED Requirements

### Requirement: Practice data source
The practice data source SHALL be PostgreSQL database, accessible via both user-facing and admin APIs.

#### Scenario: List practices from database (user)
- **WHEN** a client sends GET to `/api/practices` or `/api/wx/practices`
- **THEN** the system SHALL query the practices table in PostgreSQL

#### Scenario: Get practice by ID from database
- **WHEN** a client sends GET to `/api/practices/{id}` or `/api/wx/practices/{id}`
- **THEN** the system SHALL query the practices table by primary key

### Requirement: Admin practice CRUD operations
The practice management service SHALL support create, update, and delete operations for admin users.

#### Scenario: Create practice
- **WHEN** the practice service receives a create request with text, category, difficulty, and optional hint
- **THEN** it SHALL generate a slug-based ID, insert the record into the database, and return the created practice

#### Scenario: Update practice
- **WHEN** the practice service receives an update request with a practice ID and updated fields
- **THEN** it SHALL update the record in the database and return the updated practice

#### Scenario: Delete practice
- **WHEN** the practice service receives a delete request with a practice ID
- **THEN** it SHALL delete the record from the database

#### Scenario: Practice not found on update/delete
- **WHEN** the practice service receives an update or delete request for a non-existent ID
- **THEN** it SHALL raise an HTTP 404 error

### Requirement: Practice updated_at tracking
The practices table SHALL track when a practice was last updated.

#### Scenario: Updated timestamp
- **WHEN** a practice is created or updated
- **THEN** the updated_at column SHALL be set to the current timestamp