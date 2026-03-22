
### Requirement: Mini program silent login
The application SHALL attempt platform-appropriate login on app launch: WeChat silent login via `uni.login()` on MP-WEIXIN, or check for stored JWT token on H5.

#### Scenario: Token exists and valid
- **WHEN** the application launches with a valid stored token
- **THEN** the system SHALL use the stored token for API requests without re-login

#### Scenario: Token expired or missing (MP-WEIXIN)
- **WHEN** the application launches on MP-WEIXIN without a valid token
- **THEN** the system SHALL call `uni.login()` to get a code, send it to `/api/wx/login`, and store the returned token via `uni.setStorageSync`

#### Scenario: Token expired or missing (H5)
- **WHEN** the application launches on H5 without a valid token
- **THEN** the system SHALL redirect the user to the login page

#### Scenario: Auto re-login on 401 (MP-WEIXIN)
- **WHEN** an API request returns HTTP 401 on MP-WEIXIN
- **THEN** the system SHALL automatically attempt `uni.login()` and retry the original request

#### Scenario: Auto redirect on 401 (H5)
- **WHEN** an API request returns HTTP 401 on H5
- **THEN** the system SHALL clear the stored token and redirect the user to the login page


### Requirement: H5 email/password login
The H5 platform SHALL provide an email/password login page that authenticates via the existing `/api/auth/login` endpoint.

#### Scenario: H5 login page
- **WHEN** an unauthenticated user accesses the H5 app
- **THEN** the system SHALL display a login page with email and password input fields

#### Scenario: H5 successful login
- **WHEN** the user submits valid email and password on H5
- **THEN** the system SHALL POST to `/api/auth/login`, store the JWT token in `localStorage`, and navigate to the index page

#### Scenario: H5 login error
- **WHEN** the user submits invalid credentials on H5
- **THEN** the system SHALL display an error message without navigating away

#### Scenario: H5 logout
- **WHEN** the user taps logout on the H5 profile page
- **THEN** the system SHALL clear the stored token from `localStorage` and redirect to the login page
