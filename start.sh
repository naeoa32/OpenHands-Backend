#!/bin/bash

# Human-Like Writing Assistant Startup Script for HF Spaces

# Set environment variables for HF Spaces
export PORT=7860
export HOST="0.0.0.0"
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python 3.11 or higher."
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
    pip install --no-cache-dir -r requirements.txt
    touch .dependencies_installed
fi

# Start the server
echo "Starting Human-Like Writing Assistant..."
python app.py