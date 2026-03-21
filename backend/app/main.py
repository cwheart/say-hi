import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.services.whisper_service import whisper_service

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: load Whisper model on startup, cleanup on shutdown."""
    model_name = os.getenv("WHISPER_MODEL", "base")
    whisper_service.load_model(model_name)
    yield
    whisper_service.cleanup()
    await engine.dispose()


app = FastAPI(
    title="Say Hi - English Pronunciation Scoring API",
    description="An English pronunciation recognition and scoring system powered by OpenAI Whisper",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS configuration
# Include all frontend origins: Admin (5173), H5 uni-app dev (5174), H5 production domain
# Example: CORS_ORIGINS=http://localhost:5173,http://localhost:5174,https://sayhi.example.com
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:5174,http://localhost:3000")
origins = [origin.strip() for origin in cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
from app.routers import (  # noqa: E402
    auth, evaluate, history, practices,
    wx, wx_practices, wx_evaluate, wx_history,
    admin_auth, admin_users, admin_practices, admin_history,
)

# Existing routes
app.include_router(auth.router, prefix="/api")
app.include_router(evaluate.router, prefix="/api")
app.include_router(practices.router, prefix="/api")
app.include_router(history.router, prefix="/api")

# WeChat mini program routes
app.include_router(wx.router, prefix="/api")
app.include_router(wx_practices.router, prefix="/api")
app.include_router(wx_evaluate.router, prefix="/api")
app.include_router(wx_history.router, prefix="/api")

# Admin routes
app.include_router(admin_auth.router, prefix="/api")
app.include_router(admin_users.router, prefix="/api")
app.include_router(admin_practices.router, prefix="/api")
app.include_router(admin_history.router, prefix="/api")


@app.get("/api/health")
async def health_check():
    """Health check endpoint returning model loading status."""
    return {
        "status": "ok",
        "model": {
            "name": whisper_service.model_name,
            "status": whisper_service.status,
        },
    }