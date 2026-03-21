# Say Hi - English Pronunciation Scoring System

An English pronunciation recognition and scoring system powered by OpenAI Whisper. Record your pronunciation, get instant feedback with multi-dimension scoring and word-level comparison.

## Features

- 🎤 Browser-based audio recording
- 🧠 Local speech recognition powered by OpenAI Whisper
- 📊 Multi-dimension scoring: Accuracy, Completeness, Fluency
- 🔤 Word-by-word comparison with color-coded feedback
- 📚 Built-in practice library with words, phrases, and sentences
- 📱 Responsive design for desktop and mobile
- 🔐 User authentication (email + password, JWT)
- 🗄️ PostgreSQL database for persistent data storage
- 📈 Practice history tracking with best score display

## Prerequisites

- **Python** 3.9+ (3.11 recommended for Whisper compatibility)
- **Node.js** 18+
- **PostgreSQL** 14+
- **ffmpeg** (required for audio format conversion)

### Install ffmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows (using Chocolatey)
choco install ffmpeg
```

## Quick Start

### Database Setup

```bash
# Create the PostgreSQL database
createdb sayhi

# Or via psql
psql -c "CREATE DATABASE sayhi;"
```

### Backend

```bash
cd backend

# Create virtual environment (Python 3.11 recommended)
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install setuptools<81 wheel
pip install --no-build-isolation -r requirements.txt

# Copy environment config and update DATABASE_URL
cp .env.example .env
# Edit .env and set: DATABASE_URL=postgresql+asyncpg://<user>@localhost:5432/sayhi

# Run database migrations
alembic upgrade head

# Seed the practice library into the database
python scripts/seed_db.py

# Start server (Whisper model will download on first run)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

The frontend will be available at `http://localhost:5173` and will proxy API requests to the backend at `http://localhost:8000`.

## Project Structure

```
say-hi/
├── frontend/              # Vue.js 3 + Vite + TypeScript
│   ├── src/
│   │   ├── components/    # Vue components
│   │   ├── composables/   # Composition API utilities (auth, API, recorder)
│   │   ├── views/         # Page views (Login, Register, History, etc.)
│   │   ├── router/        # Vue Router with auth guards
│   │   └── types/         # TypeScript type definitions
│   └── package.json
├── backend/               # Python FastAPI
│   ├── app/
│   │   ├── main.py        # FastAPI entry point
│   │   ├── routers/       # API route handlers (auth, evaluate, history, practices)
│   │   ├── services/      # Business logic (Whisper, scoring, auth)
│   │   ├── models/        # SQLAlchemy ORM models & Pydantic schemas
│   │   ├── data/          # Practice seed data (JSON)
│   │   └── database.py    # Async SQLAlchemy engine & session
│   ├── alembic/           # Database migrations
│   ├── scripts/           # Utility scripts (seed_db.py)
│   └── requirements.txt
└── README.md
```

## API Endpoints

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/health` | GET | No | Health check with model loading status |
| `/api/auth/register` | POST | No | Register a new user |
| `/api/auth/login` | POST | No | Login and receive JWT token |
| `/api/auth/me` | GET | Yes | Get current user info |
| `/api/evaluate` | POST | Yes | Upload audio + target text, get scoring result |
| `/api/practices` | GET | Yes | List practice items (filterable by category/difficulty) |
| `/api/practices/{id}` | GET | Yes | Get single practice item details |
| `/api/history` | GET | Yes | Paginated list of evaluation history |
| `/api/history/{id}` | GET | Yes | Get details of a specific evaluation |

## Configuration

See `backend/.env.example` for available configuration options:

- `DATABASE_URL` - PostgreSQL connection string (e.g., `postgresql+asyncpg://user@localhost:5432/sayhi`)
- `SECRET_KEY` - JWT signing secret (change this in production!)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - JWT token expiry time (default: 1440 = 24h)
- `WHISPER_MODEL` - Model size: `tiny`, `base` (default), `small`, `medium`, `large`
- `CORS_ORIGINS` - Allowed CORS origins
- `MAX_UPLOAD_SIZE` - Maximum audio file upload size

## Tech Stack

- **Frontend**: Vue.js 3, Vite, TypeScript, Vue Router, Axios
- **Backend**: FastAPI, OpenAI Whisper, python-Levenshtein
- **Database**: PostgreSQL, SQLAlchemy 2.0 (async), Alembic
- **Auth**: JWT (python-jose), passlib + bcrypt
- **Audio**: MediaRecorder API (browser), ffmpeg (server-side conversion)

## License

MIT
