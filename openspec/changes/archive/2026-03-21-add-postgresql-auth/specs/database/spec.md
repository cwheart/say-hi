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
The system SHALL define three database tables using SQLAlchemy ORM:

#### Scenario: Users table
- **WHEN** the database is initialized
- **THEN** a `users` table SHALL exist with columns: id (UUID, PK), email (unique, not null), password_hash (not null), created_at (timestamp), updated_at (timestamp)

#### Scenario: Practices table
- **WHEN** the database is initialized
- **THEN** a `practices` table SHALL exist with columns: id (varchar, PK), text (not null), category (not null), difficulty (not null), hint (nullable), created_at (timestamp)

#### Scenario: Evaluation history table
- **WHEN** the database is initialized
- **THEN** an `evaluation_history` table SHALL exist with columns: id (UUID, PK), user_id (FK→users), practice_id (FK→practices, nullable), target_text (not null), recognized_text (not null), accuracy (int), completeness (int), fluency (int), overall_score (int), word_comparison (JSONB), created_at (timestamp)

### Requirement: Alembic migration management
The system SHALL use Alembic to manage database schema migrations.

#### Scenario: Initial migration
- **WHEN** `alembic upgrade head` is executed
- **THEN** all three tables (users, practices, evaluation_history) SHALL be created

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
