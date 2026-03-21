# Say Hi Backend

English Pronunciation Scoring System API powered by OpenAI Whisper.

## Quick Start

### Option 1: Using the debug script (Recommended)

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
python scripts/debug_server.py
```

Or use the bash script:

```bash
cd backend
./scripts/start_debug.sh
```

### Option 2: Direct uvicorn command

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --log-level debug --host 0.0.0.0 --port 8000
```

### Option 3: VS Code Debug

1. Open the `backend` folder in VS Code
2. Press `F5` or go to Run and Debug
3. Select "Python: FastAPI Backend" configuration
4. Server will start with debugging enabled

## Configuration

Edit `.env` file to customize settings:

```bash
# Server
HOST=0.0.0.0
PORT=8000

# Debug options
DEBUG=true
LOG_LEVEL=debug
UVICORN_RELOAD=true

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/sayhi

# Whisper model
WHISPER_MODEL=base
```

## Debug Features

- ✅ Auto-reload on code changes
- ✅ Detailed logging (debug level)
- ✅ Access log enabled
- ✅ Interactive debugger
- ✅ Source maps for better debugging

## API Documentation

Once running, access the interactive API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Health Check

http://localhost:8000/api/health
