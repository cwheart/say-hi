## ADDED Requirements

### Requirement: WeChat login endpoint
The system SHALL provide a `/api/wx/login` endpoint that accepts a WeChat login code and returns a JWT token.

#### Scenario: Successful WeChat login (existing user)
- **WHEN** a POST request is sent to `/api/wx/login` with a valid WeChat code and the openid is already in the database
- **THEN** the system SHALL return a JWT token and user info for the existing user

#### Scenario: Successful WeChat login (new user)
- **WHEN** a POST request is sent to `/api/wx/login` with a valid WeChat code and the openid is not in the database
- **THEN** the system SHALL create a new user with the openid and role=user, and return a JWT token

#### Scenario: Invalid WeChat code
- **WHEN** a POST request is sent to `/api/wx/login` with an invalid or expired code
- **THEN** the system SHALL return HTTP 401 with "WeChat login failed"

#### Scenario: WeChat API failure
- **WHEN** the backend cannot reach the WeChat API (https://api.weixin.qq.com/sns/jscode2session)
- **THEN** the system SHALL return HTTP 502 with "WeChat service unavailable"

### Requirement: WeChat API configuration
The system SHALL read WX_APP_ID and WX_APP_SECRET from environment variables to call the WeChat jscode2session API.

#### Scenario: Configuration present
- **WHEN** the backend starts with WX_APP_ID and WX_APP_SECRET set
- **THEN** the system SHALL be ready to process WeChat login requests

#### Scenario: Configuration missing
- **WHEN** a WeChat login request is received but WX_APP_ID or WX_APP_SECRET is not set
- **THEN** the system SHALL return HTTP 500 with "WeChat login not configured"

### Requirement: Mini program silent login
The mini program SHALL attempt silent login on app launch using stored token or wx.login().

#### Scenario: Token exists and valid
- **WHEN** the mini program launches with a valid stored token
- **THEN** the system SHALL use the stored token for API requests without re-login

#### Scenario: Token expired or missing
- **WHEN** the mini program launches without a valid token
- **THEN** the system SHALL call wx.login() to get a code, send it to `/api/wx/login`, and store the returned token

#### Scenario: Auto re-login on 401
- **WHEN** an API request returns HTTP 401
- **THEN** the mini program SHALL automatically attempt wx.login() and retry the original request
