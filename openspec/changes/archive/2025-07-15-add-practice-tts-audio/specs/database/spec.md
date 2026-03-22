## MODIFIED Requirements

### Requirement: SQLAlchemy table models
The system SHALL define database tables using SQLAlchemy ORM with the Practice model including an audio_url field.

#### Scenario: Practices table
- **WHEN** the database is initialized
- **THEN** a `practices` table SHALL exist with columns: id (varchar, PK), text (not null), category (not null), difficulty (not null), hint (nullable), audio_url (varchar(500), nullable), created_at (timestamp), updated_at (timestamp)

## ADDED Requirements

### Requirement: Database migration for audio_url
The system SHALL provide an Alembic migration to add the `audio_url` column to the practices table.

#### Scenario: Migration upgrade
- **WHEN** `alembic upgrade head` is executed
- **THEN** the practices table SHALL have a new `audio_url` column (varchar(500), nullable, default null)

#### Scenario: Migration downgrade
- **WHEN** `alembic downgrade -1` is executed
- **THEN** the `audio_url` column SHALL be removed from the practices table

#### Scenario: Existing practices default value
- **WHEN** the migration runs on a database with existing practices
- **THEN** all existing practices SHALL have `audio_url` set to null