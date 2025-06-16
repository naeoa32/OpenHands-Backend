"""
OpenHands Backend optimized for Hugging Face Spaces deployment
"""
import os
import uvicorn
from openhands.server.app import app

# Configure for Hugging Face Spaces
if __name__ == "__main__":
    # Hugging Face Spaces specific configuration
    port = int(os.getenv("PORT", 7860))  # HF Spaces default port
    host = "0.0.0.0"
    
    print(f"🤗 Starting OpenHands Backend for Hugging Face Spaces")
    print(f"🚀 Server will run on {host}:{port}")
    print(f"🔧 Runtime: {os.getenv('OPENHANDS_RUNTIME', 'local')}")
    print(f"🌐 CORS: {os.getenv('CORS_ALLOWED_ORIGINS', '*')}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )