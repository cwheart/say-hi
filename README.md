# Say Hi - English Pronunciation Scoring System

An English pronunciation recognition and scoring system powered by OpenAI Whisper. Users practice pronunciation via a WeChat Mini Program, while administrators manage content through a dedicated admin dashboard.

## Features

- 🎤 WeChat Mini Program + H5 web app (uni-app cross-platform)
- 🧠 Local speech recognition powered by OpenAI Whisper
- 📊 Multi-dimension scoring: Accuracy, Completeness, Fluency
- 🔤 Word-by-word comparison with color-coded feedback
- 📚 Built-in practice library with words, phrases, and sentences
- � WeChat login (Mini Program) + Email/Password login (Admin)
- 🗄️ PostgreSQL database for persistent data storage
- 📈 Practice history tracking
- 🛠️ Admin dashboard: user management, practice CRUD, history overview

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

### Admin Dashboard

```bash
cd admin

# Install dependencies
npm install

# Start dev server
npm run dev
```

Admin dashboard at `http://localhost:5173`, proxying API to `http://localhost:8000`.

### User App (uni-app: WeChat Mini Program + H5)

```bash
cd uniapp

# Install dependencies
npm install

# H5 development server
npm run dev:h5

# WeChat Mini Program development build
npm run dev:mp-weixin
# Then open 微信开发者工具, import dist/dev/mp-weixin/
```

H5 at `http://localhost:5174`, WeChat Mini Program via 微信开发者工具.
See `uniapp/README.md` for full details.

## Project Structure

```
say-hi/
├── admin/                 # Vue.js 3 Admin Dashboard
│   ├── src/
│   │   ├── components/    # AdminLayout
│   │   ├── composables/   # useAuth, useApi
│   │   ├── views/         # Dashboard, Users, Practices, History, Login
│   │   ├── router/        # Vue Router with admin auth guards
│   │   └── types/         # TypeScript type definitions
│   └── package.json
├── uniapp/                # uni-app (Vue 3 + Vite + TS) → MP-WEIXIN + H5
│   ├── src/
│   │   ├── pages/         # index, practice, result, history, profile, login
│   │   ├── components/    # score-card, word-compare
│   │   ├── utils/         # request, upload, auth, recorder, storage
│   │   ├── types/         # TypeScript type definitions
│   │   ├── pages.json     # Page routes & tab bar config
│   │   └── manifest.json  # Platform-specific settings
│   └── package.json
├── backend/               # Python FastAPI
│   ├── app/
│   │   ├── main.py        # FastAPI entry point
│   │   ├── routers/       # auth, evaluate, practices, history, wx_*, admin_*
│   │   ├── services/      # Whisper, scoring, auth, wx_service
│   │   ├── models/        # SQLAlchemy ORM models & Pydantic schemas
│   │   ├── data/          # Practice seed data (JSON)
│   │   └── database.py    # Async SQLAlchemy engine & session
│   ├── alembic/           # Database migrations
│   ├── scripts/           # seed_db.py (practices + admin user)
│   └── requirements.txt
└── README.md
```

## API Endpoints

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/health` | GET | No | Health check |
| **Auth** | | | |
| `/api/auth/register` | POST | No | Register user (email + password) |
| `/api/auth/login` | POST | No | Login (email + password) |
| `/api/auth/me` | GET | JWT | Get current user info |
| **WeChat** | | | |
| `/api/wx/login` | POST | No | WeChat mini program login (code → JWT) |
| `/api/wx/practices` | GET | JWT | List practices |
| `/api/wx/evaluate` | POST | JWT | Upload audio + evaluate |
| `/api/wx/history` | GET | JWT | User's evaluation history |
| **Admin** | | | |
| `/api/admin/auth/login` | POST | No | Admin login (role check) |
| `/api/admin/users` | GET | Admin | List all users |
| `/api/admin/users/{id}/disable` | PATCH | Admin | Disable user |
| `/api/admin/users/{id}/enable` | PATCH | Admin | Enable user |
| `/api/admin/practices` | GET/POST | Admin | List / Create practices |
| `/api/admin/practices/{id}` | PUT/DELETE | Admin | Update / Delete practice |
| `/api/admin/history` | GET | Admin | All users' evaluation history |

## Configuration

See `backend/.env.example` for available configuration options:

- `DATABASE_URL` - PostgreSQL connection string (e.g., `postgresql+asyncpg://user@localhost:5432/sayhi`)
- `SECRET_KEY` - JWT signing secret (change this in production!)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - JWT token expiry time (default: 1440 = 24h)
- `WHISPER_MODEL` - Model size: `tiny`, `base` (default), `small`, `medium`, `large`
- `CORS_ORIGINS` - Allowed CORS origins
- `MAX_UPLOAD_SIZE` - Maximum audio file upload size

## Tech Stack

- **Admin Dashboard**: Vue.js 3, Vite, TypeScript, Vue Router, Axios
- **User App**: uni-app (Vue 3 + Vite + TypeScript) → WeChat Mini Program + H5
- **Backend**: FastAPI, OpenAI Whisper, python-Levenshtein, httpx
- **Database**: PostgreSQL, SQLAlchemy 2.0 (async), Alembic
- **Auth**: JWT (python-jose), passlib + bcrypt, WeChat jscode2session
- **Audio**: uni.getRecorderManager (mini program), Web MediaRecorder (H5), ffmpeg (server-side)

## License

MIT
