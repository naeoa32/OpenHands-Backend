"""
Simple conversation routes for HF Spaces without complex dependencies
"""
import os
import uuid
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(prefix="/api/simple", tags=["simple-conversation"])

class SimpleConversationRequest(BaseModel):
    """Simple conversation request model"""
    message: str
    conversation_id: Optional[str] = None

class SimpleConversationResponse(BaseModel):
    """Simple conversation response model"""
    conversation_id: str
    status: str
    message: str
    response: Optional[str] = None

@router.post("/conversation")
async def create_simple_conversation(request: SimpleConversationRequest):
    """Create a simple conversation without complex dependencies."""
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or uuid.uuid4().hex
        
        # Simple response for testing
        response_message = f"Echo: {request.message}"
        
        return JSONResponse({
            "conversation_id": conversation_id,
            "status": "success",
            "message": "Conversation created successfully",
            "response": response_message,
            "user_message": request.message
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Failed to create conversation: {str(e)}",
                "conversation_id": None
            }
        )

@router.get("/conversation/{conversation_id}")
async def get_simple_conversation(conversation_id: str):
    """Get conversation info."""
    try:
        return JSONResponse({
            "conversation_id": conversation_id,
            "status": "active",
            "message": "Conversation found",
            "messages": [
                {"role": "system", "content": "This is a simple conversation endpoint"},
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there! This is a test response."}
            ]
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Failed to get conversation: {str(e)}"
            }
        )

@router.get("/health")
async def simple_health():
    """Simple health check for conversation service."""
    return JSONResponse({
        "status": "healthy",
        "service": "simple-conversation",
        "message": "Simple conversation service is running"
    })

@router.get("/test")
async def simple_test():
    """Test endpoint to verify the service is working."""
    return JSONResponse({
        "status": "success",
        "message": "Simple conversation service test passed",
        "endpoints": {
            "create": "POST /api/simple/conversation",
            "get": "GET /api/simple/conversation/{id}",
            "health": "GET /api/simple/health",
            "test": "GET /api/simple/test"
        }
    })