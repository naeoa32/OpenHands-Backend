#!/usr/bin/env python3
"""
🎯 Personal OpenHands Backend for HF Spaces
💕 Made for you and your girlfriend - NO Google Cloud needed!

This is a simplified version that removes ALL unnecessary dependencies:
❌ NO Google Cloud Storage
❌ NO Docker 
❌ NO E2B
❌ NO Redis
✅ Pure OpenHands AI agents
✅ Novel writing in Indonesian
✅ File operations
✅ All LLM providers supported
"""

import os
import sys
import logging
import traceback
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_personal_environment():
    """Setup environment for personal use - no cloud services needed."""
    logger.info("🎯 Setting up Personal OpenHands Backend...")
    
    # Essential environment variables for personal use
    os.environ.setdefault('OPENHANDS_DISABLE_AUTH', 'true')
    os.environ.setdefault('DISABLE_SECURITY', 'true')
    os.environ.setdefault('WORKSPACE_BASE', '/tmp/workspace')
    os.environ.setdefault('RUNTIME', 'local')  # Use local runtime, no Docker
    os.environ.setdefault('SANDBOX_TYPE', 'local')
    os.environ.setdefault('FILE_STORE', 'local')  # Local file storage, no Google Cloud
    os.environ.setdefault('FILE_STORE_PATH', '/tmp/openhands_storage')
    
    # Create necessary directories
    Path('/tmp/workspace').mkdir(exist_ok=True)
    Path('/tmp/openhands_storage').mkdir(exist_ok=True)
    
    logger.info("✅ Personal environment configured - no cloud dependencies!")

def check_personal_dependencies():
    """Check only essential dependencies for personal use."""
    logger.info("🔍 Checking personal dependencies...")
    
    try:
        import fastapi
        logger.info("✅ FastAPI available")
    except ImportError:
        logger.error("❌ FastAPI not available")
        return False
    
    try:
        import uvicorn
        logger.info("✅ Uvicorn available")
    except ImportError:
        logger.error("❌ Uvicorn not available")
        return False
    
    try:
        import litellm
        logger.info("✅ LiteLLM available")
    except ImportError:
        logger.error("❌ LiteLLM not available")
        return False
    
    # Check optional dependencies
    try:
        import docker
        logger.info("⚠️  Docker available (not needed for personal use)")
    except ImportError:
        logger.info("✅ Docker not available (perfect for personal use)")
    
    try:
        import google.cloud
        logger.info("⚠️  Google Cloud available (not needed for personal use)")
    except ImportError:
        logger.info("✅ Google Cloud not available (perfect for personal use)")
    
    return True

def main():
    """Main entry point for personal OpenHands backend."""
    print("=" * 50)
    print("🎯 Personal OpenHands Backend Starting...")
    print("💕 Made for you and your girlfriend!")
    print("🚀 No Google Cloud, No Docker, No Complexity!")
    print("=" * 50)
    
    try:
        # Setup personal environment
        setup_personal_environment()
        
        # Check dependencies
        if not check_personal_dependencies():
            logger.error("❌ Missing essential dependencies")
            sys.exit(1)
        
        logger.info("📦 Importing OpenHands app...")
        
        # Import OpenHands app
        from openhands.server.app import app
        
        logger.info("✅ OpenHands app imported successfully!")
        logger.info("🎉 Personal backend ready!")
        
        # Add CORS for your frontend
        from fastapi.middleware.cors import CORSMiddleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allow all origins for personal use
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Add health check
        @app.get("/health")
        async def health_check():
            return {
                "status": "healthy",
                "message": "Personal OpenHands Backend is running!",
                "features": [
                    "AI Agents (CodeActAgent, BrowsingAgent, etc.)",
                    "Novel Writing (Indonesian)",
                    "File Operations",
                    "No Google Cloud needed",
                    "No Docker needed"
                ]
            }
        
        # Add personal info endpoint
        @app.get("/personal-info")
        async def personal_info():
            return {
                "title": "Personal OpenHands Backend",
                "description": "Made for you and your girlfriend 💕",
                "features": {
                    "ai_agents": [
                        "CodeActAgent - Complete coding assistant",
                        "BrowsingAgent - Web research",
                        "ReadOnlyAgent - Safe code review",
                        "LocAgent - Targeted code generation"
                    ],
                    "novel_writing": [
                        "Indonesian language support",
                        "7 creative templates",
                        "Character development",
                        "Plot structure",
                        "Dialogue writing"
                    ],
                    "file_operations": [
                        "view - Display files",
                        "create - Create new files", 
                        "str_replace - Edit content",
                        "insert - Add content"
                    ]
                },
                "no_dependencies": [
                    "No Google Cloud Storage",
                    "No Docker containers",
                    "No E2B sandboxes",
                    "No Redis cache",
                    "Pure local operation"
                ]
            }
        
        # Start server
        if __name__ == "__main__":
            import uvicorn
            
            logger.info("🚀 Starting Personal OpenHands Backend...")
            logger.info("💕 Perfect for your personal AI assistant!")
            
            uvicorn.run(
                app,
                host="0.0.0.0",
                port=7860,  # HF Spaces default port
                log_level="info"
            )
        
        return app
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.error("💡 This usually means a dependency is missing.")
        logger.error("💡 For personal use, you only need: fastapi, uvicorn, litellm")
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    app = main()