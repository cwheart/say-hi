#!/usr/bin/env python3
"""
Uvicorn development server with debug configuration.

This script provides a convenient way to start the FastAPI backend
with debugging enabled, auto-reload, and detailed logging.

Usage:
    python debug_server.py
    
Environment Variables (from .env file):
    - DEBUG: Enable debug mode (true/false)
    - LOG_LEVEL: Logging level (debug, info, warning, error, critical)
    - HOST: Server host (default: 0.0.0.0)
    - PORT: Server port (default: 8000)
"""

import os
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(backend_dir))

try:
    import uvicorn
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("\nPlease install required packages:")
    print("  pip install uvicorn[standard] python-dotenv")
    sys.exit(1)

# Load environment variables from .env file
env_file = backend_dir / ".env"
if env_file.exists():
    print(f"📄 Loading environment from {env_file}")
    load_dotenv(env_file)
else:
    print(f"⚠️  Warning: .env file not found at {env_file}")
    print("   Using default environment variables")

# Configuration
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "debug").lower()
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
RELOAD = os.getenv("UVICORN_RELOAD", "true").lower() == "true"

# Print configuration
print("\n" + "="*60)
print("🚀 Say Hi Backend - Debug Server Configuration")
print("="*60)
print(f"📍 Host: {HOST}:{PORT}")
print(f"🔧 Debug Mode: {DEBUG}")
print(f"📊 Log Level: {LOG_LEVEL}")
print(f"🔄 Auto Reload: {RELOAD}")
print(f"📝 Access Log: Enabled")
print(f"🔍 Loop: uvloop (auto)")
print("="*60 + "\n")

if __name__ == "__main__":
    try:
        # Start uvicorn server with debug configuration
        uvicorn.run(
            "app.main:app",
            host=HOST,
            port=PORT,
            reload=RELOAD,
            log_level=LOG_LEVEL,
            access_log=True,
            loop="uvloop" if sys.platform != "win32" else "asyncio",
            debug=DEBUG,
            lifespan="on",
            http="auto",
            ws="auto",
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)
