## CHANGED Requirements

### Requirement: Practice data source
The practice data source SHALL change from in-memory JSON dictionary to PostgreSQL database queries.

#### Scenario: List practices from database
- **WHEN** a client sends GET to `/api/practices`
- **THEN** the system SHALL query the practices table in PostgreSQL instead of the in-memory dictionary

#### Scenario: Get practice by ID from database
- **WHEN** a client sends GET to `/api/practices/{id}`
- **THEN** the system SHALL query the practices table by primary key
