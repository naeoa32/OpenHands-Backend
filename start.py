#!/usr/bin/env python3
"""
Simple start script for Render deployment
"""
import os
import uvicorn

if __name__ == "__main__":
    # Get port from environment (Render sets this automatically)
    port = int(os.environ.get('PORT', 3000))
    
    # Start the server
    uvicorn.run(
        "openhands.server.listen:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )