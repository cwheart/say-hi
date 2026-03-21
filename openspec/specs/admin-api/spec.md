
### Requirement: Admin authentication endpoint
The system SHALL provide an admin login endpoint that verifies email/password and checks role=admin.

#### Scenario: Successful admin login
- **WHEN** a POST request is sent to `/api/admin/auth/login` with valid admin credentials
- **THEN** the system SHALL return a JWT token with role=admin in the payload

#### Scenario: Non-admin login attempt
- **WHEN** a POST request is sent to `/api/admin/auth/login` with credentials of a user with role=user
- **THEN** the system SHALL return HTTP 403 with "Admin access required"

### Requirement: Admin role authorization
The system SHALL provide a `require_admin` dependency that validates the current user has role=admin.

#### Scenario: Admin access granted
- **WHEN** a request with a JWT token for a user with role=admin hits an admin endpoint
- **THEN** the system SHALL allow the request to proceed

#### Scenario: Non-admin access denied
- **WHEN** a request with a JWT token for a user with role=user hits an admin endpoint
- **THEN** the system SHALL return HTTP 403

### Requirement: User management API
The system SHALL provide admin endpoints to list and manage users.

#### Scenario: List users
- **WHEN** an admin sends GET to `/api/admin/users` with optional page and page_size params
- **THEN** the system SHALL return a paginated list of all users with id, email, role, openid, is_active, created_at

#### Scenario: Disable user
- **WHEN** an admin sends PATCH to `/api/admin/users/{id}/disable`
- **THEN** the system SHALL set the user's is_active to false and return the updated user

#### Scenario: Enable user
- **WHEN** an admin sends PATCH to `/api/admin/users/{id}/enable`
- **THEN** the system SHALL set the user's is_active to true and return the updated user

### Requirement: Practice CRUD API
The system SHALL provide admin endpoints to create, update, and delete practice items.

#### Scenario: Create practice
- **WHEN** an admin sends POST to `/api/admin/practices` with text, category, difficulty, and optional hint
- **THEN** the system SHALL create a new practice in the database and return it

#### Scenario: Update practice
- **WHEN** an admin sends PUT to `/api/admin/practices/{id}` with updated fields
- **THEN** the system SHALL update the practice and return the updated record

#### Scenario: Delete practice
- **WHEN** an admin sends DELETE to `/api/admin/practices/{id}`
- **THEN** the system SHALL soft-delete or hard-delete the practice and return HTTP 204

#### Scenario: Create practice with duplicate text
- **WHEN** an admin sends POST with text that already exists
- **THEN** the system SHALL still create the practice (duplicates allowed)

### Requirement: Admin history API
The system SHALL provide admin endpoints to view all users' evaluation history.

#### Scenario: List all evaluations
- **WHEN** an admin sends GET to `/api/admin/history` with optional page, page_size, user_id params
- **THEN** the system SHALL return a paginated list of all evaluations across all users, including user email

#### Scenario: Filter by user
- **WHEN** an admin sends GET to `/api/admin/history?user_id={id}`
- **THEN** the system SHALL return only evaluations for the specified user
