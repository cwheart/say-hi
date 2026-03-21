#!/bin/bash

# Say Hi Backend - Debug Server Launcher
# This script starts the uvicorn server with optimal debug settings

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Say Hi Backend - Debug Server           ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Warning: .env file not found${NC}"
    echo -e "${YELLOW}   Creating from .env.example...${NC}"
    cp .env.example .env 2>/dev/null || true
fi

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${YELLOW}⚠️  Virtual environment not activated${NC}"
    echo -e "${YELLOW}   Attempting to activate...${NC}"
    if [ -d "venv" ]; then
        source venv/bin/activate
        echo -e "${GREEN}✓ Virtual environment activated${NC}"
    else
        echo -e "${RED}✗ No virtual environment found${NC}"
        echo -e "${YELLOW}   Please create one with:${NC}"
        echo -e "   python3 -m venv venv"
        exit 1
    fi
fi

# Check dependencies
echo -e "${BLUE}📦 Checking dependencies...${NC}"
python -c "import uvicorn" 2>/dev/null || {
    echo -e "${RED}✗ uvicorn not installed${NC}"
    echo -e "${YELLOW}   Installing...${NC}"
    pip install -q uvicorn[standard] python-dotenv
}
echo -e "${GREEN}✓ Dependencies OK${NC}"
echo ""

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Default values
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
LOG_LEVEL=${LOG_LEVEL:-debug}
RELOAD=${UVICORN_RELOAD:-true}

# Print configuration
echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC} Configuration                          ${GREEN}║${NC}"
echo -e "${GREEN}╠════════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║${NC} Host: ${BLUE}${HOST}:${PORT}${NC}                        ${GREEN}║${NC}"
echo -e "${GREEN}║${NC} Log Level: ${YELLOW}${LOG_LEVEL}${NC}                       ${GREEN}║${NC}"
echo -e "${GREEN}║${NC} Auto Reload: ${YELLOW}${RELOAD}${NC}                     ${GREEN}║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
echo ""

# Start server
echo -e "${BLUE}🚀 Starting Uvicorn server...${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

cd "$(dirname "$0")"
python -m uvicorn app.main:app \
    --host "$HOST" \
    --port "$PORT" \
    --reload="$RELOAD" \
    --log-level "$LOG_LEVEL" \
    --access-log \
    --lifespan on
