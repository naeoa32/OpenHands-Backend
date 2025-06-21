"""
Simplified OpenHands Backend for Hugging Face Spaces
"""
import os
import sys
import logging
import tempfile
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Setup environment variables
os.environ.setdefault("PORT", "12000")  # Use port 12000 for the runtime environment
os.environ.setdefault("HOST", "0.0.0.0")
os.environ.setdefault("OPENHANDS_RUNTIME", "local")
os.environ.setdefault("CORS_ALLOWED_ORIGINS", "*")
os.environ["SETTINGS_STORE_TYPE"] = "memory"
os.environ["SECRETS_STORE_TYPE"] = "memory"
os.environ["CONVERSATION_STORE_TYPE"] = "memory"
os.environ["FILE_STORE"] = "memory"
os.environ["SESSION_STORE_TYPE"] = "memory"
os.environ["DISABLE_SECURITY"] = "true"
os.environ["OPENHANDS_DISABLE_AUTH"] = "true"
os.environ["SECURITY_CONFIRMATION_MODE"] = "false"
os.environ["DISABLE_FILE_LOGGING"] = "true"
os.environ["DISABLE_PERSISTENT_SESSIONS"] = "true"
os.environ["SERVE_FRONTEND"] = "false"
os.environ.setdefault("MAX_ITERATIONS", "30")
os.environ.setdefault("DEFAULT_AGENT", "CodeActAgent")
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/tmp/playwright_browsers")

# Import required packages
try:
    import fastapi
    import uvicorn
    from fastapi import FastAPI, Request, Response, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    logger.info("✅ FastAPI available")
except ImportError as e:
    logger.error(f"❌ Error importing FastAPI: {e}")
    sys.exit(1)

# Create FastAPI app
app = FastAPI(title="OpenHands API", version="0.43.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "OpenHands API is running",
        "version": "0.43.0",
        "endpoints": {
            "api_models": "/api/options/models",
            "api_agents": "/api/options/agents",
            "conversations": "/api/conversations",
            "simple_conversation": "/api/simple/conversation",
            "test-chat": "/api/test-chat",
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Simple conversation endpoint
@app.post("/api/simple/conversation")
async def simple_conversation(request: Request):
    data = await request.json()
    message = data.get("message", "")
    
    # Simple echo response
    return {
        "response": f"Echo: {message}",
        "conversation_id": "test-conversation",
        "message_id": "test-message"
    }

# Test chat endpoint
@app.post("/api/test-chat")
async def test_chat(request: Request):
    data = await request.json()
    message = data.get("message", "")
    
    # Simple echo response
    return {
        "response": f"Test chat: {message}",
        "conversation_id": "test-conversation",
        "message_id": "test-message"
    }

# Models options endpoint
@app.get("/api/options/models")
async def get_models():
    return {
        "models": [
            {"id": "openrouter/anthropic/claude-3-haiku-20240307", "name": "Claude 3 Haiku"},
            {"id": "openrouter/anthropic/claude-3-sonnet-20240229", "name": "Claude 3 Sonnet"},
            {"id": "openrouter/anthropic/claude-3-opus-20240229", "name": "Claude 3 Opus"}
        ]
    }

# Agents options endpoint
@app.get("/api/options/agents")
async def get_agents():
    return {
        "agents": [
            {"id": "CodeActAgent", "name": "Code Act Agent"},
            {"id": "BrowsingAgent", "name": "Browsing Agent"},
            {"id": "SimpleAgent", "name": "Simple Agent"}
        ]
    }

# Install Playwright browsers
def install_playwright_browsers():
    """Install Playwright browsers with robust error handling"""
    try:
        logger.info("🎭 Installing Playwright browsers...")
        
        # Create a custom browser path in /tmp to avoid permission issues
        browser_path = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/tmp/playwright_browsers")
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = browser_path
        
        # Create the directory if it doesn't exist
        Path(browser_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Using custom browser path: {browser_path}")
        
        # Set HOME to a temporary directory to avoid .cache permission issues
        temp_home = tempfile.mkdtemp()
        old_home = os.environ.get("HOME")
        os.environ["HOME"] = temp_home
        logger.info(f"🏠 Using temporary HOME directory: {temp_home}")
        
        # Check if browser already exists
        chromium_path = os.path.join(browser_path, "chromium-1169")
        if os.path.exists(chromium_path):
            logger.info("✅ Playwright browser already installed")
            # Restore original HOME
            if old_home:
                os.environ["HOME"] = old_home
            return True
        
        # Try to install with --with-deps first (recommended)
        try:
            import subprocess
            logger.info("🔄 Attempting installation with --with-deps...")
            env = os.environ.copy()
            result = subprocess.run(
                [sys.executable, "-m", "playwright", "install", "chromium", "--with-deps"],
                capture_output=True,
                text=True,
                timeout=300,
                env=env
            )

            if result.returncode == 0:
                logger.info("✅ Playwright browsers installed successfully with dependencies")
                # Restore original HOME
                if old_home:
                    os.environ["HOME"] = old_home
                return True
            else:
                logger.warning(f"⚠️ Installation with --with-deps failed: {result.stderr}")
        except Exception as e:
            logger.warning(f"⚠️ Error during installation with --with-deps: {e}")

        # Fallback: Try without --with-deps
        try:
            logger.info("🔄 Attempting installation without --with-deps...")
            env = os.environ.copy()
            result = subprocess.run(
                [sys.executable, "-m", "playwright", "install", "chromium"],
                capture_output=True,
                text=True,
                timeout=300,
                env=env
            )

            if result.returncode == 0:
                logger.info("✅ Playwright browsers installed successfully (without deps)")
                # Restore original HOME
                if old_home:
                    os.environ["HOME"] = old_home
                return True
            else:
                logger.error(f"❌ Installation failed: {result.stderr}")
                # Restore original HOME
                if old_home:
                    os.environ["HOME"] = old_home
                return False
        except Exception as e:
            logger.error(f"❌ Error during installation: {e}")
            # Restore original HOME
            if old_home:
                os.environ["HOME"] = old_home
            return False

    except Exception as e:
        logger.error(f"❌ Playwright install error: {e}")
        return False

# Main entry point
if __name__ == "__main__":
    try:
        logger.info("🔄 Setting up environment...")
        
        # Check for LiteLLM
        try:
            import litellm
            logger.info("✅ LiteLLM available")
        except ImportError:
            logger.warning("⚠️ LiteLLM not available")
        
        # Check for Playwright
        try:
            import playwright
            logger.info("✅ Playwright available")
            
            # Install Playwright browsers
            if install_playwright_browsers():
                logger.info("✅ Playwright browsers installed successfully")
            else:
                logger.warning("⚠️ Playwright browser installation failed")
        except ImportError:
            logger.warning("⚠️ Playwright not available")
        
        # Start uvicorn server
        logger.info("🚀 Starting uvicorn server...")
        uvicorn.run(
            app, 
            host=os.environ.get("HOST", "0.0.0.0"),
            port=int(os.environ.get("PORT", 12000)),
            log_level="info"
        )
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        sys.exit(1)