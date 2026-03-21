## CHANGED Requirements

### Requirement: History navigation
The frontend SHALL include a navigation link to the history page and display user info in the header.

#### Scenario: Navigation header update
- **WHEN** a user is logged in
- **THEN** the header SHALL show the user's email, a link to "History", and a "Logout" button

#### Scenario: History page in navigation
- **WHEN** a user clicks "History" in the header
- **THEN** the system SHALL navigate to `/history` showing past evaluation records
