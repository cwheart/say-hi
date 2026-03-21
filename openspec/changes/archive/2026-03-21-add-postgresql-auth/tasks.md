## 1. Backend Dependencies & Config

- [x] 1.1 Update `requirements.txt` — add sqlalchemy[asyncio], asyncpg, alembic, passlib[bcrypt], python-jose[cryptography]
- [x] 1.2 Update `.env.example` — add DATABASE_URL, JWT_SECRET, JWT_EXPIRE_MINUTES
- [x] 1.3 Rename `backend/app/models/evaluation.py` → `backend/app/models/schemas.py`, update all imports

## 2. Database Layer

- [x] 2.1 Create `backend/app/database.py` — async engine, async_sessionmaker, get_db dependency
- [x] 2.2 Create `backend/app/models/db_models.py` — SQLAlchemy models for User, Practice, EvaluationHistory (with Base)
- [x] 2.3 Initialize Alembic in `backend/` — `alembic init alembic`, configure `alembic.ini` and `env.py` for async
- [x] 2.4 Create initial Alembic migration — auto-generate from db_models, creates users, practices, evaluation_history tables

## 3. Auth Service

- [x] 3.1 Create `backend/app/services/auth_service.py` — password hashing (bcrypt), JWT creation & verification
- [x] 3.2 Create `backend/app/services/deps.py` — get_db, get_current_user dependencies (OAuth2PasswordBearer)
- [x] 3.3 Add auth Pydantic schemas to `schemas.py` — RegisterRequest, LoginRequest, AuthResponse, UserResponse

## 4. Auth API Routes

- [x] 4.1 Create `backend/app/routers/auth.py` — POST /register, POST /login, GET /me
- [x] 4.2 Register auth router in `main.py`

## 5. Migrate Practices to DB

- [x] 5.1 Rewrite `backend/app/services/practice_service.py` — async DB queries instead of in-memory dict
- [x] 5.2 Update `backend/app/routers/practices.py` — inject db session, use new practice_service
- [x] 5.3 Remove practice_service.load() from main.py lifespan, add DB engine dispose on shutdown

## 6. Seed Data Script

- [x] 6.1 Create `backend/scripts/__init__.py` and `backend/scripts/seed_db.py` — read practices.json, insert into DB, support --force flag
- [x] 6.2 Test seed script: create database, run alembic upgrade head, run seed script

## 7. Evaluation History

- [x] 7.1 Update `backend/app/routers/evaluate.py` — require auth (get_current_user), accept optional practice_id, save result to evaluation_history table
- [x] 7.2 Create `backend/app/routers/history.py` — GET /history (paginated, current user), GET /history/{id}
- [x] 7.3 Add history Pydantic schemas to `schemas.py` — HistoryListResponse, HistoryDetailResponse, PaginatedResponse
- [x] 7.4 Register history router in `main.py`

## 8. Update main.py

- [x] 8.1 Update `backend/app/main.py` — import DB engine, update lifespan (dispose engine on shutdown), register all new routers

## 9. Frontend Auth

- [x] 9.1 Create `frontend/src/composables/useAuth.ts` — login, register, logout, token management (localStorage), current user state
- [x] 9.2 Update `frontend/src/composables/useApi.ts` — add axios interceptor for JWT token, 401 redirect
- [x] 9.3 Add auth types to `frontend/src/types/index.ts` — LoginRequest, RegisterRequest, AuthResponse, UserInfo
- [x] 9.4 Create `frontend/src/views/LoginView.vue` — email + password form, error display, link to register
- [x] 9.5 Create `frontend/src/views/RegisterView.vue` — email + password + confirm password form, error display, link to login
- [x] 9.6 Update `frontend/src/router/index.ts` — add /login, /register, /history routes, add navigation guard (redirect to /login if not authenticated)

## 10. Frontend History & UI Updates

- [x] 10.1 Create `frontend/src/views/HistoryList.vue` — paginated list of past evaluations with date, target text, score
- [x] 10.2 Update `frontend/src/views/PracticeDetail.vue` — pass practice_id to evaluate API, show best score if available
- [x] 10.3 Update `frontend/src/App.vue` — show user email in header, add History link, add Logout button (when logged in), show Login link (when not logged in)
- [x] 10.4 Update `frontend/src/composables/useApi.ts` — add getHistory, getHistoryById, getBestScore API methods

## 11. Documentation

- [x] 11.1 Update `README.md` — add PostgreSQL setup instructions, database creation, alembic migration, seed data script steps
