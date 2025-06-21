#!/bin/bash

# OpenHands Backend Startup Script

# Set environment variables
export PLAYWRIGHT_BROWSERS_PATH="/tmp/playwright_browsers"
export PORT=12000
export HOST="0.0.0.0"
export OPENHANDS_RUNTIME="local"
export CORS_ALLOWED_ORIGINS="*"
export SETTINGS_STORE_TYPE="memory"
export SECRETS_STORE_TYPE="memory"
export CONVERSATION_STORE_TYPE="memory"
export FILE_STORE="memory"
export SESSION_STORE_TYPE="memory"
export DISABLE_SECURITY="true"
export OPENHANDS_DISABLE_AUTH="true"
export SECURITY_CONFIRMATION_MODE="false"
export DISABLE_FILE_LOGGING="true"
export DISABLE_PERSISTENT_SESSIONS="true"
export SERVE_FRONTEND="false"
export MAX_ITERATIONS="30"
export DEFAULT_AGENT="CodeActAgent"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python 3.12 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "pip is not installed. Please install pip."
    exit 1
fi

# Install dependencies if needed
if [ ! -f ".dependencies_installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    pip install playwright
    python install_playwright.py
    touch .dependencies_installed
fi

# Start the server
echo "Starting OpenHands Backend..."
python app.py