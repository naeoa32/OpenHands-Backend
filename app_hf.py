"""
OpenHands Backend optimized for Hugging Face Spaces deployment
"""
import os
import secrets
import tempfile
import uvicorn
import sys
import logging

# Configure logging for better debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure for Hugging Face Spaces BEFORE importing app
def setup_hf_environment():
    """Setup environment variables for Hugging Face Spaces"""
    
    # Set default environment variables for HF Spaces
    os.environ.setdefault("OPENHANDS_RUNTIME", "local")
    os.environ.setdefault("CORS_ALLOWED_ORIGINS", "*")
    os.environ.setdefault("SERVE_FRONTEND", "false")
    
    # Create writable directories
    file_store_path = "/tmp/openhands"
    cache_dir = "/tmp/cache"
    workspace_dir = "/tmp/workspace"
    
    # All directories that might be needed
    directories_to_create = [
        file_store_path,
        cache_dir, 
        workspace_dir,
        "/tmp/openhands/sessions",
        "/tmp/openhands/logs",
        "/tmp/openhands/data",
        "/tmp/openhands/storage",
        "/tmp/openhands/conversations",
        "/tmp/openhands/models",
        "/tmp/openhands/settings"
    ]
    
    # Ensure directories exist with proper permissions
    for directory in directories_to_create:
        try:
            os.makedirs(directory, mode=0o777, exist_ok=True)
            os.chmod(directory, 0o777)
            logger.info(f"✅ Created directory: {directory}")
        except Exception as e:
            logger.warning(f"⚠️ Could not create directory {directory}: {e}")
            # Continue with other directories
    
    # Set file store path to a writable directory in HF Spaces
    os.environ.setdefault("FILE_STORE_PATH", file_store_path)
    
    # Set cache directory to a writable location
    os.environ.setdefault("CACHE_DIR", cache_dir)
    
    # Generate JWT secret if not provided (for HF Spaces)
    if not os.getenv("JWT_SECRET"):
        jwt_secret = secrets.token_urlsafe(32)
        os.environ["JWT_SECRET"] = jwt_secret
        print(f"🔐 Generated JWT secret for session")

    # Set other HF-specific configs
    os.environ.setdefault("DISABLE_SECURITY", "true")  # For public API
    os.environ.setdefault("SANDBOX_RUNTIME_CONTAINER_IMAGE", "")  # Disable Docker
    os.environ.setdefault("SANDBOX_USER_ID", "1000")
    os.environ.setdefault("WORKSPACE_BASE", "/tmp/workspace")

    # Additional security bypass for HF Spaces
    os.environ.setdefault("OPENHANDS_DISABLE_AUTH", "true")
    os.environ.setdefault("ENABLE_AUTO_LINT", "false")
    os.environ.setdefault("ENABLE_SECURITY_ANALYSIS", "false")

    # Use memory-based storage for read-only environments
    os.environ.setdefault("SETTINGS_STORE_TYPE", "memory")
    os.environ.setdefault("SECRETS_STORE_TYPE", "memory")

    # Pre-configure default LLM settings for easy access
    os.environ.setdefault("DEFAULT_LLM_MODEL", "openrouter/anthropic/claude-3-haiku-20240307")
    os.environ.setdefault("DEFAULT_LLM_BASE_URL", "https://openrouter.ai/api/v1") 
    os.environ.setdefault("SKIP_SETTINGS_MODAL", "true")  # Skip setup wizard if API key available

    # Enhanced user experience settings
    os.environ.setdefault("DEFAULT_AGENT", "CodeActAgent")
    os.environ.setdefault("DEFAULT_LANGUAGE", "en")
    os.environ.setdefault("CONFIRMATION_MODE", "false")
    os.environ.setdefault("ENABLE_AUTO_LINT", "false")

    # Performance optimizations for HF Spaces
    os.environ.setdefault("MAX_ITERATIONS", "30")  # Reasonable limit for public usage
    os.environ.setdefault("MAX_BUDGET_PER_TASK", "10.0")  # Cost control

    # Create workspace directory
    workspace_dir = "/tmp/workspace"
    os.makedirs(workspace_dir, mode=0o777, exist_ok=True)
    
    # Set workspace permissions
    try:
        os.chmod(workspace_dir, 0o777)
        logger.info(f"✅ Set workspace permissions")
    except Exception as e:
        logger.warning(f"⚠️ Could not set workspace permissions: {e}")

    return file_store_path, cache_dir


if __name__ == "__main__":
    try:
        # Setup environment before importing anything
        logger.info("🔧 Setting up Hugging Face environment...")
        file_store_path, cache_dir = setup_hf_environment()

        # Now import the app after environment is configured
        logger.info("📦 Importing OpenHands app...")
        from openhands.server.app import app

        # Hugging Face Spaces specific configuration
        port = int(os.getenv("PORT", 7860))  # HF Spaces default port
        host = "0.0.0.0"

        print("🤗 Starting OpenHands Backend for Hugging Face Spaces")
        print(f"🚀 Server will run on {host}:{port}")
        print(f"🔧 Runtime: {os.getenv('OPENHANDS_RUNTIME')}")
        print(f"🌐 CORS: {os.getenv('CORS_ALLOWED_ORIGINS')}")
        print(f"📁 File Store: {file_store_path}")
        print(f"💾 Cache Dir: {cache_dir}")
        print(f"🔑 LLM API Key: {'✅ Set' if os.getenv('LLM_API_KEY') else '❌ Missing'}")
        print(f"🔐 JWT Secret: {'✅ Set' if os.getenv('JWT_SECRET') else '❌ Missing'}")
        print(f"🛡️ Security Disabled: {os.getenv('DISABLE_SECURITY')}")
        print(f"🔓 Auth Disabled: {os.getenv('OPENHANDS_DISABLE_AUTH')}")
        print("📡 API Endpoints:")
        print("   GET  / (root)")
        print("   GET  /health")
        print("   GET  /docs (API documentation)")
        print("   GET  /api/options/config")
        print("   GET  /api/hf/status")
        print("   GET  /api/hf/ready")
        print("   GET  /api/hf/environment")
        print("   POST /api/conversations")
        print("🌍 Ready for frontend integration!")
        
        # Debug environment
        print("\n🔍 Debug Info:")
        print(f"   Python Path: {sys.path[:3]}...")
        print(f"   LLM_MODEL: {os.getenv('LLM_MODEL', 'Not set')}")
        print(f"   LLM_BASE_URL: {os.getenv('LLM_BASE_URL', 'Not set')}")
        print(f"   DEFAULT_LLM_MODEL: {os.getenv('DEFAULT_LLM_MODEL', 'Not set')}")
        print(f"   DEFAULT_LLM_BASE_URL: {os.getenv('DEFAULT_LLM_BASE_URL', 'Not set')}")
        print(f"   OPENROUTER_API_KEY: {'✅ Set' if os.getenv('OPENROUTER_API_KEY') else '❌ Missing'}")
        print(f"   WORKSPACE_BASE: {os.getenv('WORKSPACE_BASE', 'Not set')}")
        print(f"   SETTINGS_STORE_TYPE: {os.getenv('SETTINGS_STORE_TYPE', 'file')}")
        print(f"   SECRETS_STORE_TYPE: {os.getenv('SECRETS_STORE_TYPE', 'file')}")
        print(f"   SKIP_SETTINGS_MODAL: {os.getenv('SKIP_SETTINGS_MODAL', 'false')}")

        logger.info("🚀 Starting uvicorn server...")
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
