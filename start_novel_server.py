#!/usr/bin/env python3
"""
Start script for OpenHands Backend with Novel Writing Mode support
Optimized for Render deployment
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_environment():
    """Setup environment variables for novel writing mode"""
    
    # Default environment variables for novel writing mode
    defaults = {
        'PORT': '8000',
        'HOST': '0.0.0.0',
        'LLM_BASE_URL': 'https://openrouter.ai/api/v1',
        'LLM_MODEL': 'openrouter/anthropic/claude-3-haiku-20240307',
        'OR_SITE_URL': 'https://docs.all-hands.dev/',
        'OR_APP_NAME': 'OpenHands-NovelWriting',
        'RUNTIME': 'eventstream',
        'DEFAULT_AGENT': 'CodeActAgent',
        'MAX_CONCURRENT_CONVERSATIONS': '5',
        'SECURITY_CONFIRMATION_MODE': 'false',
        'FILE_STORE_PATH': '/tmp/openhands_storage',
        'LOG_LEVEL': 'INFO',
        'CORS_ALLOWED_ORIGINS': '*',
        'SERVE_FRONTEND': 'false',
        'DEBUG': 'false',
        'ENABLE_AUTO_LINT': 'false',
        'ENABLE_AUTO_TEST': 'false',
    }
    
    # Set defaults only if not already set
    for key, value in defaults.items():
        if key not in os.environ:
            os.environ[key] = value
    
    # Ensure required directories exist
    file_store_path = os.environ.get('FILE_STORE_PATH', '/tmp/openhands_storage')
    os.makedirs(file_store_path, exist_ok=True)
    
    print("🔧 Environment configured for Novel Writing Mode")
    print(f"   - Port: {os.environ.get('PORT')}")
    print(f"   - Host: {os.environ.get('HOST')}")
    print(f"   - LLM Base URL: {os.environ.get('LLM_BASE_URL')}")
    print(f"   - Default Model: {os.environ.get('LLM_MODEL')}")
    print(f"   - File Store: {file_store_path}")

def check_requirements():
    """Check if required environment variables are set"""
    required_vars = [
        'OPENROUTER_API_KEY',
        'LLM_API_KEY',
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables before starting the server.")
        print("For development, you can create a .env file with these values.")
        return False
    
    print("✅ All required environment variables are set")
    return True

def main():
    """Main entry point"""
    print("🚀 Starting OpenHands Backend with Novel Writing Mode")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    print("\n📚 Novel Writing Mode Features:")
    print("   - Indonesian creative writing prompts")
    print("   - Intelligent model selection (Budget/Premium)")
    print("   - Template-based assistance")
    print("   - Optimized AI parameters for creativity")
    print("   - No generic responses - always asks specific questions")
    
    print(f"\n🌐 Server will start on http://{os.environ.get('HOST')}:{os.environ.get('PORT')}")
    print("   - WebSocket endpoint: /socket.io/")
    print("   - Health check: /api/health")
    print("   - CORS enabled for all origins")
    
    print("\n📝 Frontend Integration:")
    print("   Send novel_mode: true in MessageAction to activate")
    print("   Include template_used and original_prompt for best results")
    
    try:
        # Import and start the server
        from openhands.server.listen import main as server_main
        
        print("\n🎯 Starting server...")
        server_main()
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()