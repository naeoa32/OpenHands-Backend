"""
HF Spaces specific routes for debugging and status checking.
"""
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/hf", tags=["hf-spaces"])

# Add a catch-all route for missing endpoints
@router.get("/logs-container")
async def logs_container():
    """Handle logs-container requests that might be coming from HF Spaces UI."""
    return JSONResponse({
        "message": "Logs endpoint not implemented",
        "status": "info",
        "logs": []
    })

@router.get("/logs")
async def logs():
    """Handle logs requests."""
    return JSONResponse({
        "message": "Logs endpoint",
        "status": "info", 
        "logs": []
    })


@router.get("/status")
async def hf_status():
    """Get HF Spaces deployment status and configuration."""
    return {
        "status": "running",
        "environment": "huggingface-spaces",
        "runtime": os.getenv("OPENHANDS_RUNTIME", "local"),
        "settings_store": os.getenv("SETTINGS_STORE_TYPE", "file"),
        "secrets_store": os.getenv("SECRETS_STORE_TYPE", "file"),
        "cors_enabled": os.getenv("CORS_ALLOWED_ORIGINS", "*"),
        "auth_disabled": os.getenv("OPENHANDS_DISABLE_AUTH", "false"),
        "security_disabled": os.getenv("DISABLE_SECURITY", "false"),
    }


@router.get("/ready")
async def hf_ready():
    """Health check endpoint for HF Spaces."""
    return {
        "ready": True,
        "message": "OpenHands Backend is ready for HF Spaces",
        "api_available": True,
    }


@router.get("/environment")
async def hf_environment():
    """Get environment configuration for debugging."""
    env_vars = {
        "OPENHANDS_RUNTIME": os.getenv("OPENHANDS_RUNTIME"),
        "SETTINGS_STORE_TYPE": os.getenv("SETTINGS_STORE_TYPE"),
        "SECRETS_STORE_TYPE": os.getenv("SECRETS_STORE_TYPE"),
        "CORS_ALLOWED_ORIGINS": os.getenv("CORS_ALLOWED_ORIGINS"),
        "DISABLE_SECURITY": os.getenv("DISABLE_SECURITY"),
        "OPENHANDS_DISABLE_AUTH": os.getenv("OPENHANDS_DISABLE_AUTH"),
        "DEFAULT_LLM_MODEL": os.getenv("DEFAULT_LLM_MODEL"),
        "DEFAULT_LLM_BASE_URL": os.getenv("DEFAULT_LLM_BASE_URL"),
        "SKIP_SETTINGS_MODAL": os.getenv("SKIP_SETTINGS_MODAL"),
        "FILE_STORE_PATH": os.getenv("FILE_STORE_PATH"),
        "WORKSPACE_BASE": os.getenv("WORKSPACE_BASE"),
        "CACHE_DIR": os.getenv("CACHE_DIR"),
        "MAX_ITERATIONS": os.getenv("MAX_ITERATIONS"),
        "CONFIRMATION_MODE": os.getenv("CONFIRMATION_MODE"),
        "DEFAULT_AGENT": os.getenv("DEFAULT_AGENT"),
        "DEFAULT_LANGUAGE": os.getenv("DEFAULT_LANGUAGE"),
        # Don't expose sensitive values, just indicate if they're set
        "JWT_SECRET": "✅ Set" if os.getenv("JWT_SECRET") else "❌ Missing",
        "LLM_API_KEY": "✅ Set" if os.getenv("LLM_API_KEY") else "❌ Missing",
        "OPENROUTER_API_KEY": "✅ Set" if os.getenv("OPENROUTER_API_KEY") else "❌ Missing",
    }
    
    return {
        "environment_variables": env_vars,
        "directories": {
            "file_store_exists": os.path.exists(os.getenv("FILE_STORE_PATH", "/tmp/openhands")),
            "workspace_exists": os.path.exists(os.getenv("WORKSPACE_BASE", "/tmp/workspace")),
            "cache_exists": os.path.exists(os.getenv("CACHE_DIR", "/tmp/cache")),
        }
    }

@router.post("/test-conversation")
async def test_conversation():
    """Simple test endpoint for conversation creation without dependencies."""
    try:
        import uuid
        conversation_id = uuid.uuid4().hex
        return JSONResponse({
            "status": "success",
            "conversation_id": conversation_id,
            "message": "Test conversation created successfully",
            "test": True
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error", 
                "message": f"Test conversation failed: {str(e)}",
                "test": True
            }
        )

@router.post("/simple-conversation")
async def simple_conversation():
    """Create a simple conversation with minimal dependencies."""
    try:
        import uuid
        from datetime import datetime
        
        conversation_id = uuid.uuid4().hex
        
        # Create a minimal conversation record
        conversation_data = {
            "conversation_id": conversation_id,
            "user_id": "anonymous",
            "created_at": datetime.now().isoformat(),
            "status": "created",
            "title": "New Conversation",
            "messages": [],
            "settings": {
                "agent": "CodeActAgent",
                "language": "en",
                "max_iterations": 30
            }
        }
        
        # Try to save to file system if possible
        try:
            import json
            conversations_dir = "/tmp/openhands/conversations"
            os.makedirs(conversations_dir, exist_ok=True)
            
            conversation_file = os.path.join(conversations_dir, f"{conversation_id}.json")
            with open(conversation_file, 'w') as f:
                json.dump(conversation_data, f, indent=2)
                
            return JSONResponse({
                "status": "success",
                "conversation_id": conversation_id,
                "message": "Simple conversation created and saved",
                "data": conversation_data
            })
        except Exception as save_error:
            # Return success even if we can't save to disk
            return JSONResponse({
                "status": "success",
                "conversation_id": conversation_id,
                "message": f"Simple conversation created (memory only): {save_error}",
                "data": conversation_data
            })
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error", 
                "message": f"Simple conversation failed: {str(e)}",
                "error_type": type(e).__name__
            }
        )

@router.get("/debug")
async def debug_info():
    """Debug endpoint to check system status."""
    try:
        import sys
        import platform
        
        return JSONResponse({
            "system": {
                "platform": platform.platform(),
                "python_version": sys.version,
                "python_path": sys.path[:3]
            },
            "environment": {
                "runtime": os.getenv("OPENHANDS_RUNTIME", "not_set"),
                "settings_store": os.getenv("SETTINGS_STORE_TYPE", "not_set"),
                "secrets_store": os.getenv("SECRETS_STORE_TYPE", "not_set"),
                "auth_disabled": os.getenv("OPENHANDS_DISABLE_AUTH", "not_set"),
                "security_disabled": os.getenv("DISABLE_SECURITY", "not_set")
            },
            "directories": {
                "file_store": {
                    "path": os.getenv("FILE_STORE_PATH", "/tmp/openhands"),
                    "exists": os.path.exists(os.getenv("FILE_STORE_PATH", "/tmp/openhands")),
                    "writable": os.access(os.getenv("FILE_STORE_PATH", "/tmp/openhands"), os.W_OK) if os.path.exists(os.getenv("FILE_STORE_PATH", "/tmp/openhands")) else False
                },
                "workspace": {
                    "path": os.getenv("WORKSPACE_BASE", "/tmp/workspace"),
                    "exists": os.path.exists(os.getenv("WORKSPACE_BASE", "/tmp/workspace")),
                    "writable": os.access(os.getenv("WORKSPACE_BASE", "/tmp/workspace"), os.W_OK) if os.path.exists(os.getenv("WORKSPACE_BASE", "/tmp/workspace")) else False
                },
                "cache": {
                    "path": os.getenv("CACHE_DIR", "/tmp/cache"),
                    "exists": os.path.exists(os.getenv("CACHE_DIR", "/tmp/cache")),
                    "writable": os.access(os.getenv("CACHE_DIR", "/tmp/cache"), os.W_OK) if os.path.exists(os.getenv("CACHE_DIR", "/tmp/cache")) else False
                }
            }
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"Debug failed: {str(e)}",
                "type": type(e).__name__
            }
        )