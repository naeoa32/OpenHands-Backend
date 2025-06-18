"""
Pure memory-based conversation endpoint for HF Spaces
No file system dependencies at all
"""
import uuid
import json
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter(prefix="/memory-chat", tags=["memory-chat"])

# In-memory storage for conversations
CONVERSATIONS: Dict[str, Dict] = {}

class MemoryChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    model: Optional[str] = "openai/gpt-4o-mini"

class MemoryChatResponse(BaseModel):
    conversation_id: str
    response: str
    timestamp: str
    model: str
    status: str

@router.get("/")
async def memory_chat_info():
    """Get memory chat service info."""
    return JSONResponse({
        "service": "memory-chat",
        "status": "running",
        "description": "Pure memory-based chat with no file dependencies",
        "active_conversations": len(CONVERSATIONS),
        "endpoints": {
            "info": "GET /memory-chat/",
            "chat": "POST /memory-chat/message",
            "list": "GET /memory-chat/conversations",
            "get": "GET /memory-chat/conversations/{conversation_id}",
            "clear": "DELETE /memory-chat/conversations"
        }
    })

@router.post("/message")
async def send_message(request: MemoryChatRequest):
    """Send a message and get a response (pure memory, no OpenRouter call for now)."""
    try:
        # Get or create conversation
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        if conversation_id not in CONVERSATIONS:
            CONVERSATIONS[conversation_id] = {
                "id": conversation_id,
                "created_at": datetime.now().isoformat(),
                "messages": [],
                "model": request.model
            }
        
        # Add user message
        user_message = {
            "role": "user",
            "content": request.message,
            "timestamp": datetime.now().isoformat()
        }
        CONVERSATIONS[conversation_id]["messages"].append(user_message)
        
        # Generate simple response (echo for now, can be replaced with OpenRouter call)
        response_text = f"Echo from memory chat: {request.message}"
        
        # Add assistant response
        assistant_message = {
            "role": "assistant", 
            "content": response_text,
            "timestamp": datetime.now().isoformat(),
            "model": request.model
        }
        CONVERSATIONS[conversation_id]["messages"].append(assistant_message)
        
        return JSONResponse({
            "conversation_id": conversation_id,
            "response": response_text,
            "timestamp": datetime.now().isoformat(),
            "model": request.model,
            "status": "success",
            "message_count": len(CONVERSATIONS[conversation_id]["messages"])
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Memory chat error: {str(e)}"
        )

@router.get("/conversations")
async def list_conversations():
    """List all active conversations."""
    conversations = []
    for conv_id, conv_data in CONVERSATIONS.items():
        conversations.append({
            "id": conv_id,
            "created_at": conv_data["created_at"],
            "message_count": len(conv_data["messages"]),
            "model": conv_data.get("model", "unknown"),
            "last_message": conv_data["messages"][-1]["timestamp"] if conv_data["messages"] else None
        })
    
    return JSONResponse({
        "status": "success",
        "total_conversations": len(conversations),
        "conversations": conversations
    })

@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get a specific conversation."""
    if conversation_id not in CONVERSATIONS:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return JSONResponse({
        "status": "success",
        "conversation": CONVERSATIONS[conversation_id]
    })

@router.delete("/conversations")
async def clear_all_conversations():
    """Clear all conversations from memory."""
    count = len(CONVERSATIONS)
    CONVERSATIONS.clear()
    
    return JSONResponse({
        "status": "success",
        "message": f"Cleared {count} conversations from memory",
        "remaining_conversations": len(CONVERSATIONS)
    })

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a specific conversation."""
    if conversation_id not in CONVERSATIONS:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    del CONVERSATIONS[conversation_id]
    
    return JSONResponse({
        "status": "success",
        "message": f"Deleted conversation {conversation_id}",
        "remaining_conversations": len(CONVERSATIONS)
    })

@router.get("/health")
async def memory_chat_health():
    """Health check for memory chat service."""
    return JSONResponse({
        "status": "healthy",
        "service": "memory-chat",
        "active_conversations": len(CONVERSATIONS),
        "memory_usage": "in-memory only",
        "file_dependencies": "none",
        "timestamp": datetime.now().isoformat()
    })