## MODIFIED Requirements

### Requirement: SQLAlchemy table models
The system SHALL define database tables using SQLAlchemy ORM with extended User model fields.

#### Scenario: Users table
- **WHEN** the database is initialized
- **THEN** a `users` table SHALL exist with columns: id (UUID, PK), email (unique, nullable), password_hash (nullable), role (VARCHAR(20), default 'user'), openid (VARCHAR(100), unique, nullable), nickname (VARCHAR(100), nullable), is_active (boolean, default true), created_at (timestamp), updated_at (timestamp)

#### Scenario: Practices table
- **WHEN** the database is initialized
- **THEN** a `practices` table SHALL exist with columns: id (varchar, PK), text (not null), category (not null), difficulty (not null), hint (nullable), created_at (timestamp), updated_at (timestamp)

#### Scenario: Evaluation history table
- **WHEN** the database is initialized
- **THEN** an `evaluation_history` table SHALL exist with columns: id (UUID, PK), user_id (FK→users), practice_id (FK→practices, nullable), target_text (not null), recognized_text (not null), accuracy (int), completeness (int), fluency (int), overall_score (int), word_comparison (JSONB), created_at (timestamp)

## ADDED Requirements

### Requirement: Database migration for user model extension
The system SHALL provide an Alembic migration to add role, openid, nickname, and is_active columns to the users table.

#### Scenario: Migration upgrade
- **WHEN** `alembic upgrade head` is executed
- **THEN** the users table SHALL have new columns: role (default 'user'), openid (nullable, unique), nickname (nullable), is_active (default true)

#### Scenario: Migration downgrade
- **WHEN** `alembic downgrade -1` is executed
- **THEN** the new columns SHALL be removed from the users table

#### Scenario: Existing users default values
- **WHEN** the migration runs on a database with existing users
- **THEN** all existing users SHALL have role='user' and is_active=true
