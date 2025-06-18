#!/usr/bin/env python3
"""
Main entry point for Render deployment
This file is required by Render's auto-detection
"""
import os
import uvicorn

if __name__ == "__main__":
    # Get port from environment (Render sets this automatically)
    port = int(os.environ.get('PORT', 3000))
    
    # Set default environment variables for backend-only deployment
    os.environ.setdefault('SERVE_FRONTEND', 'false')
    os.environ.setdefault('DEBUG', 'false')
    os.environ.setdefault('CORS_ALLOWED_ORIGINS', '*')
    os.environ.setdefault('LOG_LEVEL', 'info')
    
    print(f"🚀 Starting OpenHands Backend on port {port}")
    print(f"📁 SERVE_FRONTEND: {os.environ.get('SERVE_FRONTEND')}")
    print(f"🔧 DEBUG: {os.environ.get('DEBUG')}")
    print(f"🌐 CORS_ALLOWED_ORIGINS: {os.environ.get('CORS_ALLOWED_ORIGINS')}")
    
    # Start the server
    uvicorn.run(
        "openhands.server.listen:app",
        host="0.0.0.0",
        port=port,
        log_level=os.environ.get('LOG_LEVEL', 'info'),
        access_log=True
    )