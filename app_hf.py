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
    
    # Set default environment variables for HF Spaces
    os.environ.setdefault("OPENHANDS_RUNTIME", "local")
    os.environ.setdefault("CORS_ALLOWED_ORIGINS", "*")
    os.environ.setdefault("SERVE_FRONTEND", "false")
    
    # Set file store path to a writable directory in HF Spaces
    os.environ.setdefault("FILE_STORE_PATH", "/tmp/openhands")
    
    # Set cache directory to a writable location
    os.environ.setdefault("CACHE_DIR", "/tmp/cache")
    
    print("🤗 Starting OpenHands Backend for Hugging Face Spaces")
    print(f"🚀 Server will run on {host}:{port}")
    print(f"🔧 Runtime: {os.getenv('OPENHANDS_RUNTIME')}")
    print(f"🌐 CORS: {os.getenv('CORS_ALLOWED_ORIGINS')}")
    print(f"📁 File Store: {os.getenv('FILE_STORE_PATH')}")
    print(f"💾 Cache Dir: {os.getenv('CACHE_DIR')}")
    print(f"🔑 LLM API Key: {'✅ Set' if os.getenv('LLM_API_KEY') else '❌ Missing'}")
    print("📡 API Endpoints:")
    print("   GET  /api/options/config")
    print("   POST /api/conversations") 
    print("   GET  /health")
    print("🌍 Ready for frontend integration!")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )