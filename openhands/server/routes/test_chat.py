"""
Ultra-simple test chat endpoint for HF Spaces
No dependencies, no file operations, just pure API responses
"""
import uuid
import json
from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

router = APIRouter(prefix="/test-chat", tags=["test-chat"])

# In-memory storage for demo purposes
conversations: Dict[str, Dict[str, Any]] = {}

class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    status: str
    timestamp: str

@router.get("/")
async def test_chat_info():
    """Get test chat service info."""
    return JSONResponse({
        "service": "test-chat",
        "status": "running",
        "description": "Ultra-simple chat endpoint for testing",
        "endpoints": {
            "info": "GET /test-chat/",
            "chat": "POST /test-chat/message",
            "history": "GET /test-chat/conversation/{id}",
            "list": "GET /test-chat/conversations"
        },
        "features": [
            "No file operations",
            "No complex dependencies", 
            "In-memory storage only",
            "Instant responses"
        ]
    })

@router.post("/message")
async def send_message(message: ChatMessage):
    """Send a message and get a simple response."""
    try:
        # Generate or use existing conversation ID
        conversation_id = message.conversation_id or str(uuid.uuid4())
        
        # Create conversation if it doesn't exist
        if conversation_id not in conversations:
            conversations[conversation_id] = {
                "id": conversation_id,
                "created_at": datetime.now().isoformat(),
                "messages": []
            }
        
        # Add user message
        user_msg = {
            "role": "user",
            "content": message.message,
            "timestamp": datetime.now().isoformat()
        }
        conversations[conversation_id]["messages"].append(user_msg)
        
        # Generate simple response
        response_text = f"Echo: {message.message} (Test response from HF Spaces)"
        
        # Add assistant response
        assistant_msg = {
            "role": "assistant", 
            "content": response_text,
            "timestamp": datetime.now().isoformat()
        }
        conversations[conversation_id]["messages"].append(assistant_msg)
        
        return JSONResponse({
            "conversation_id": conversation_id,
            "response": response_text,
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "message_count": len(conversations[conversation_id]["messages"])
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Chat failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@router.get("/conversation/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history."""
    try:
        if conversation_id not in conversations:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "Conversation not found",
                    "conversation_id": conversation_id
                }
            )
        
        return JSONResponse({
            "status": "success",
            "conversation": conversations[conversation_id],
            "message_count": len(conversations[conversation_id]["messages"])
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Failed to get conversation: {str(e)}"
            }
        )

@router.get("/conversations")
async def list_conversations():
    """List all conversations."""
    try:
        conversation_list = []
        for conv_id, conv_data in conversations.items():
            conversation_list.append({
                "id": conv_id,
                "created_at": conv_data["created_at"],
                "message_count": len(conv_data["messages"]),
                "last_message": conv_data["messages"][-1]["content"] if conv_data["messages"] else None
            })
        
        return JSONResponse({
            "status": "success",
            "conversations": conversation_list,
            "total_count": len(conversation_list)
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Failed to list conversations: {str(e)}"
            }
        )

@router.delete("/conversation/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation."""
    try:
        if conversation_id not in conversations:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "Conversation not found"
                }
            )
        
        del conversations[conversation_id]
        
        return JSONResponse({
            "status": "success",
            "message": "Conversation deleted",
            "conversation_id": conversation_id
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Failed to delete conversation: {str(e)}"
            }
        )

@router.get("/health")
async def test_chat_health():
    """Health check for test chat service."""
    return JSONResponse({
        "status": "healthy",
        "service": "test-chat",
        "active_conversations": len(conversations),
        "timestamp": datetime.now().isoformat(),
        "memory_usage": "minimal"
    })