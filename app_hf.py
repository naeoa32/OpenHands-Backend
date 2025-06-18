"""
OpenHands Backend optimized for Hugging Face Spaces deployment
Simplified version to avoid common deployment issues
"""
import os
import sys
import logging
import uvicorn
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_hf_environment():
    """Setup environment variables for Hugging Face Spaces"""
    
    # Core HF Spaces configuration
    os.environ.setdefault("PORT", "7860")
    os.environ.setdefault("HOST", "0.0.0.0")
    os.environ.setdefault("OPENHANDS_RUNTIME", "e2b")  # Use E2B for cloud execution
    os.environ.setdefault("CORS_ALLOWED_ORIGINS", "*")
    
    # Use memory-based storage to avoid file permission issues
    os.environ["SETTINGS_STORE_TYPE"] = "memory"
    os.environ["SECRETS_STORE_TYPE"] = "memory"
    os.environ["CONVERSATION_STORE_TYPE"] = "memory"
    os.environ["FILE_STORE"] = "memory"
    os.environ["SESSION_STORE_TYPE"] = "memory"
    
    # Disable security and auth for public API
    os.environ["DISABLE_SECURITY"] = "true"
    os.environ["OPENHANDS_DISABLE_AUTH"] = "true"
    os.environ["SECURITY_CONFIRMATION_MODE"] = "false"
    
    # Disable file-based features
    os.environ["DISABLE_FILE_LOGGING"] = "true"
    os.environ["DISABLE_PERSISTENT_SESSIONS"] = "true"
    os.environ["SERVE_FRONTEND"] = "false"
    
    # Set reasonable defaults for public usage
    os.environ.setdefault("MAX_ITERATIONS", "30")
    os.environ.setdefault("DEFAULT_AGENT", "CodeActAgent")
    
    # File storage configuration - use local storage for HF Spaces
    os.environ.setdefault("FILE_STORE", "local")
    os.environ.setdefault("FILE_STORE_PATH", "/tmp/openhands_storage")
    
    # LLM configuration - use OpenRouter by default
    if not os.getenv("LLM_API_KEY"):
        logger.warning("⚠️  LLM_API_KEY not set. Please set it in HF Spaces environment variables.")
    os.environ.setdefault("LLM_MODEL", "openrouter/anthropic/claude-3-haiku-20240307")
    os.environ.setdefault("LLM_BASE_URL", "https://openrouter.ai/api/v1")
    
    # E2B Runtime configuration for cloud code execution
    if not os.getenv("E2B_API_KEY"):
        logger.warning("⚠️  E2B_API_KEY not set. Code execution will be limited.")
        logger.info("💡 Get your E2B API key from: https://e2b.dev/docs")
        # Fallback to local runtime if E2B not available
        os.environ["OPENHANDS_RUNTIME"] = "local"
    
    # Create directories if they don't exist
    directories = ["/tmp/openhands", "/tmp/cache", "/tmp/workspace", "/tmp/file_store"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    logger.info("✅ Environment configured for Hugging Face Spaces")
    return "/tmp/file_store", "/tmp/cache"


if __name__ == "__main__":
    try:
        logger.info("🔧 Setting up Hugging Face environment...")
        file_store_path, cache_dir = setup_hf_environment()
        
        logger.info("📦 Importing OpenHands app...")
        from openhands.server.app import app
        
        # Get configuration
        port = int(os.getenv("PORT", 7860))
        host = os.getenv("HOST", "0.0.0.0")
        
        # Startup information
        print("🤗 OpenHands Backend for Hugging Face Spaces")
        print(f"🚀 Server: {host}:{port}")
        print(f"🔑 LLM API Key: {'✅ Set' if os.getenv('LLM_API_KEY') else '❌ Missing'}")
        print(f"🤖 LLM Model: {os.getenv('LLM_MODEL', 'Not configured')}")
        print("📡 API Endpoints available at /docs")
        
        logger.info("🚀 Starting uvicorn server...")
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info"
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
