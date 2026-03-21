
### Requirement: Admin login page
The Admin dashboard SHALL provide a login page for administrators to authenticate with email and password.

#### Scenario: Admin login form
- **WHEN** an unauthenticated user navigates to the Admin app
- **THEN** the system SHALL display a login form with email and password fields

#### Scenario: Successful admin login
- **WHEN** an admin enters valid credentials and submits
- **THEN** the system SHALL store the JWT token and redirect to the dashboard

#### Scenario: Non-admin login attempt
- **WHEN** a user with role `user` attempts to log in to the Admin dashboard
- **THEN** the system SHALL display an error "Access denied: admin role required"

### Requirement: User management page
The Admin dashboard SHALL provide a page to view and manage all registered users.

#### Scenario: User list display
- **WHEN** an admin navigates to the user management page
- **THEN** the system SHALL display a paginated table with columns: email, role, openid (if present), created_at, status

#### Scenario: Disable user
- **WHEN** an admin clicks the disable button on a user row
- **THEN** the system SHALL call the API to disable the user and update the UI

#### Scenario: Enable user
- **WHEN** an admin clicks the enable button on a disabled user row
- **THEN** the system SHALL call the API to enable the user and update the UI

### Requirement: Practice CRUD page
The Admin dashboard SHALL provide pages to create, read, update, and delete practice items.

#### Scenario: Practice list
- **WHEN** an admin navigates to the practice management page
- **THEN** the system SHALL display a paginated table of all practices with text, category, difficulty, and action buttons

#### Scenario: Create practice
- **WHEN** an admin fills out the create practice form with text, category, difficulty, and optional hint
- **THEN** the system SHALL submit the data to the API and add the new practice to the list

#### Scenario: Edit practice
- **WHEN** an admin clicks edit on a practice and modifies fields
- **THEN** the system SHALL submit the updated data to the API and refresh the list

#### Scenario: Delete practice
- **WHEN** an admin clicks delete on a practice and confirms
- **THEN** the system SHALL call the delete API and remove the practice from the list

### Requirement: Evaluation history overview
The Admin dashboard SHALL provide a page to view all users' evaluation history.

#### Scenario: History list
- **WHEN** an admin navigates to the history overview page
- **THEN** the system SHALL display a paginated table of all evaluations with user email, target text, overall score, and date

#### Scenario: History filter
- **WHEN** an admin filters by user email or date range
- **THEN** the system SHALL display only matching evaluation records

### Requirement: Admin navigation and layout
The Admin dashboard SHALL provide a sidebar navigation with links to all management pages.

#### Scenario: Sidebar navigation
- **WHEN** an admin is logged in
- **THEN** the system SHALL display a sidebar with links: Dashboard, Users, Practices, History, and a logout button

#### Scenario: Admin logout
- **WHEN** an admin clicks the logout button
- **THEN** the system SHALL clear the JWT token and redirect to the login page
