## ADDED Requirements

### Requirement: Practice library
The system SHALL provide a built-in practice library with English words and sentences organized by difficulty level (beginner, intermediate, advanced).

#### Scenario: List all practices
- **WHEN** a client sends GET request to `/api/practices`
- **THEN** the system SHALL return a list of practice items grouped by category and difficulty level

#### Scenario: Get practice by ID
- **WHEN** a client sends GET request to `/api/practices/{id}`
- **THEN** the system SHALL return the practice item details including the target text, difficulty level, category, and optional hint

#### Scenario: Practice not found
- **WHEN** a client requests a practice ID that does not exist
- **THEN** the system SHALL return HTTP 404 with an error message

### Requirement: Practice categories
The system SHALL organize practices into categories: `word` (single words), `phrase` (short phrases), and `sentence` (full sentences).

#### Scenario: Filter by category
- **WHEN** a client sends GET request to `/api/practices?category=word`
- **THEN** the system SHALL return only practice items in the `word` category

#### Scenario: Filter by difficulty
- **WHEN** a client sends GET request to `/api/practices?difficulty=beginner`
- **THEN** the system SHALL return only practice items with `beginner` difficulty level

### Requirement: Built-in seed data
The system SHALL include at least 30 pre-loaded practice items covering all categories and difficulty levels. The seed data SHALL be loaded from a JSON file at application startup.

#### Scenario: Seed data available on startup
- **WHEN** the FastAPI application starts
- **THEN** the practice library SHALL contain at least 30 items across all categories and difficulty levels
