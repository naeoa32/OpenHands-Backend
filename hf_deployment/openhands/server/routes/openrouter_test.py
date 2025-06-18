"""
OpenRouter API test endpoint for HF Spaces
Simple test to verify OpenRouter integration works
"""
import os
import json
import requests
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/openrouter", tags=["openrouter"])

class OpenRouterTestRequest(BaseModel):
    message: str
    model: Optional[str] = "openai/gpt-4o-mini"
    api_key: Optional[str] = None

@router.get("/")
async def openrouter_info():
    """Get OpenRouter service info."""
    return JSONResponse({
        "service": "openrouter-test",
        "status": "running",
        "description": "OpenRouter API test endpoint",
        "endpoints": {
            "info": "GET /openrouter/",
            "test": "POST /openrouter/test",
            "models": "GET /openrouter/models",
            "health": "GET /openrouter/health"
        },
        "default_model": "openai/gpt-4o-mini",
        "base_url": "https://openrouter.ai/api/v1"
    })

@router.post("/test")
async def test_openrouter(request: OpenRouterTestRequest):
    """Test OpenRouter API with a simple message."""
    try:
        # Get API key from request or environment
        api_key = request.api_key or os.getenv("LLM_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        
        if not api_key:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "No OpenRouter API key provided. Set LLM_API_KEY or OPENROUTER_API_KEY environment variable, or provide in request.",
                    "timestamp": datetime.now().isoformat()
                }
            )
        
        # Prepare OpenRouter API request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://huggingface.co/spaces/Minatoz997/Backend66",
            "X-Title": "OpenHands Backend Test"
        }
        
        payload = {
            "model": request.model,
            "messages": [
                {
                    "role": "user",
                    "content": request.message
                }
            ],
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        # Make request to OpenRouter
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            assistant_message = data["choices"][0]["message"]["content"]
            
            return JSONResponse({
                "status": "success",
                "request_message": request.message,
                "response_message": assistant_message,
                "model_used": request.model,
                "timestamp": datetime.now().isoformat(),
                "usage": data.get("usage", {}),
                "openrouter_response": "✅ Working"
            })
        else:
            return JSONResponse(
                status_code=response.status_code,
                content={
                    "status": "error",
                    "message": f"OpenRouter API error: {response.text}",
                    "status_code": response.status_code,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
    except requests.exceptions.Timeout:
        return JSONResponse(
            status_code=408,
            content={
                "status": "error",
                "message": "OpenRouter API request timed out",
                "timestamp": datetime.now().isoformat()
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Failed to test OpenRouter: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@router.get("/models")
async def get_openrouter_models():
    """Get available OpenRouter models."""
    try:
        api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        
        if not api_key:
            return JSONResponse({
                "status": "info",
                "message": "No API key provided, showing popular models",
                "popular_models": [
                    "openai/gpt-4o-mini",
                    "openai/gpt-4o",
                    "anthropic/claude-3.5-sonnet",
                    "google/gemini-pro",
                    "meta-llama/llama-3.1-8b-instruct"
                ]
            })
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            models = [model["id"] for model in data.get("data", [])]
            
            return JSONResponse({
                "status": "success",
                "total_models": len(models),
                "models": models[:20],  # Show first 20 models
                "timestamp": datetime.now().isoformat()
            })
        else:
            return JSONResponse(
                status_code=response.status_code,
                content={
                    "status": "error",
                    "message": f"Failed to fetch models: {response.text}",
                    "timestamp": datetime.now().isoformat()
                }
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Failed to get models: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@router.get("/health")
async def openrouter_health():
    """Health check for OpenRouter service."""
    api_key_available = bool(os.getenv("LLM_API_KEY") or os.getenv("OPENROUTER_API_KEY"))
    
    return JSONResponse({
        "status": "healthy",
        "service": "openrouter-test",
        "api_key_configured": api_key_available,
        "base_url": "https://openrouter.ai/api/v1",
        "timestamp": datetime.now().isoformat(),
        "environment_vars": {
            "LLM_API_KEY": "✅ Set" if os.getenv("LLM_API_KEY") else "❌ Not set",
            "OPENROUTER_API_KEY": "✅ Set" if os.getenv("OPENROUTER_API_KEY") else "❌ Not set",
            "LLM_MODEL": os.getenv("LLM_MODEL", "Not set"),
            "LLM_BASE_URL": os.getenv("LLM_BASE_URL", "Not set")
        }
    })