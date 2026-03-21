## MODIFIED Requirements

### Requirement: JWT authentication
The system SHALL use JWT Bearer tokens for authenticating protected API endpoints. JWT payload SHALL include user role for authorization decisions.

#### Scenario: Valid token
- **WHEN** a request includes a valid JWT token in the Authorization header
- **THEN** the system SHALL extract the user identity and role, and proceed with the request

#### Scenario: Expired token
- **WHEN** a request includes an expired JWT token
- **THEN** the system SHALL return HTTP 401

#### Scenario: Missing token on protected endpoint
- **WHEN** a request to a protected endpoint lacks an Authorization header
- **THEN** the system SHALL return HTTP 401

#### Scenario: JWT payload includes role
- **WHEN** a JWT token is created for any user
- **THEN** the token payload SHALL include the user's role (admin or user)

### Requirement: Get current user
The system SHALL provide an endpoint to retrieve the currently authenticated user's info, including role.

#### Scenario: Get current user
- **WHEN** an authenticated user sends GET to `/api/auth/me`
- **THEN** the system SHALL return the user's id, email, role, nickname, and created_at

## ADDED Requirements

### Requirement: User role field
The User model SHALL include a `role` field with values `admin` or `user`, defaulting to `user`.

#### Scenario: Default role
- **WHEN** a new user is created via registration or WeChat login
- **THEN** the user's role SHALL be `user` by default

#### Scenario: Admin role check
- **WHEN** the system needs to verify admin access
- **THEN** it SHALL check that `user.role == 'admin'`

### Requirement: WeChat openid field
The User model SHALL include a nullable `openid` field for WeChat login association.

#### Scenario: User with openid
- **WHEN** a user logs in via WeChat
- **THEN** the user record SHALL have the WeChat openid stored

#### Scenario: User without openid
- **WHEN** a user registered via email/password
- **THEN** the user's openid field SHALL be null

### Requirement: User active status
The User model SHALL include an `is_active` field for account enable/disable.

#### Scenario: Disabled user login
- **WHEN** a disabled user attempts to authenticate (via any method)
- **THEN** the system SHALL return HTTP 403 with "Account is disabled"

#### Scenario: Active by default
- **WHEN** a new user is created
- **THEN** the user's is_active SHALL be true by default
