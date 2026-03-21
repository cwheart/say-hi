## ADDED Requirements

### Requirement: User registration
The system SHALL allow users to register with email and password.

#### Scenario: Successful registration
- **WHEN** a POST request is sent to `/api/auth/register` with valid email and password
- **THEN** the system SHALL create a new user, hash the password with bcrypt, and return user info with a JWT access token

#### Scenario: Duplicate email
- **WHEN** a user attempts to register with an email that already exists
- **THEN** the system SHALL return HTTP 409 with an error message

#### Scenario: Invalid email format
- **WHEN** a user attempts to register with an invalid email format
- **THEN** the system SHALL return HTTP 422 with a validation error

#### Scenario: Weak password
- **WHEN** a user attempts to register with a password shorter than 6 characters
- **THEN** the system SHALL return HTTP 422 with a validation error

### Requirement: User login
The system SHALL allow users to log in with email and password and receive a JWT token.

#### Scenario: Successful login
- **WHEN** a POST request is sent to `/api/auth/login` with valid credentials
- **THEN** the system SHALL verify the password and return a JWT access token

#### Scenario: Invalid credentials
- **WHEN** a user attempts to log in with wrong email or password
- **THEN** the system SHALL return HTTP 401 with "Invalid email or password"

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

### Requirement: Frontend auth pages
The frontend SHALL provide login and registration pages with form validation.

#### Scenario: Login page
- **WHEN** user navigates to `/login`
- **THEN** the system SHALL display a login form with email and password fields

#### Scenario: Registration page
- **WHEN** user navigates to `/register`
- **THEN** the system SHALL display a registration form with email, password, and confirm password fields

#### Scenario: Auth redirect
- **WHEN** an unauthenticated user attempts to access a protected page
- **THEN** the system SHALL redirect to `/login`

#### Scenario: Token storage
- **WHEN** user successfully logs in or registers
- **THEN** the system SHALL store the JWT token in localStorage and redirect to the home page

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