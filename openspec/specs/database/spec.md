## ADDED Requirements

### Requirement: PostgreSQL connection management
The system SHALL connect to PostgreSQL using SQLAlchemy 2.0 async engine with asyncpg driver. Connection URL SHALL be configurable via DATABASE_URL environment variable.

#### Scenario: Successful connection
- **WHEN** the FastAPI application starts
- **THEN** the system SHALL create an async engine and session factory connected to PostgreSQL

#### Scenario: Connection failure
- **WHEN** PostgreSQL is not reachable at startup
- **THEN** the system SHALL log an error and fail to start

### Requirement: SQLAlchemy table models
The system SHALL define database tables using SQLAlchemy ORM with extended User model fields.

#### Scenario: Users table
- **WHEN** the database is initialized
- **THEN** a `users` table SHALL exist with columns: id (UUID, PK), email (unique, nullable), password_hash (nullable), role (VARCHAR(20), default 'user'), openid (VARCHAR(100), unique, nullable), nickname (VARCHAR(100), nullable), is_active (boolean, default true), created_at (timestamp), updated_at (timestamp)

#### Scenario: Practices table
- **WHEN** the database is initialized
- **THEN** a `practices` table SHALL exist with columns: id (varchar, PK), text (not null), category (not null), difficulty (not null), hint (nullable), audio_url (varchar(500), nullable), created_at (timestamp), updated_at (timestamp)

#### Scenario: Evaluation history table
- **WHEN** the database is initialized
- **THEN** an `evaluation_history` table SHALL exist with columns: id (UUID, PK), user_id (FK→users), practice_id (FK→practices, nullable), target_text (not null), recognized_text (not null), accuracy (int), completeness (int), fluency (int), overall_score (int), word_comparison (JSONB), created_at (timestamp)

### Requirement: Alembic migration management
The system SHALL use Alembic to manage database schema migrations.

#### Scenario: Initial migration
- **WHEN** `alembic upgrade head` is executed
- **THEN** all three tables (users, practices, evaluation_history) SHALL be created

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

### Requirement: Seed data script
The system SHALL provide a standalone script to initialize seed data from practices.json into the PostgreSQL practices table.

#### Scenario: First-time seed
- **WHEN** `python -m scripts.seed_db` is executed and the practices table is empty
- **THEN** the script SHALL insert all items from practices.json into the practices table

#### Scenario: Idempotent seed
- **WHEN** `python -m scripts.seed_db` is executed and the practices table already has data
- **THEN** the script SHALL skip insertion and print a message that data already exists

#### Scenario: Force reseed
- **WHEN** `python -m scripts.seed_db --force` is executed
- **THEN** the script SHALL delete all existing practices and re-insert from practices.json