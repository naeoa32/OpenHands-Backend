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
    
    print(f"🚀 Starting OpenHands Backend on port {port}")
    
    # Start the server
    uvicorn.run(
        "openhands.server.listen:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        access_log=True
    )