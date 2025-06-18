"""
Real OpenRouter chat endpoint with actual API integration
This is the main chat endpoint that uses OpenRouter API
"""
import os
import uuid
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["chat"])

# In-memory storage for conversations
CHAT_CONVERSATIONS: Dict[str, Dict] = {}

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    model: Optional[str] = "openai/gpt-4o-mini"
    api_key: Optional[str] = None
    stream: Optional[bool] = False
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    model: str
    timestamp: str
    usage: Optional[Dict] = None
    status: str

@router.get("/")
async def chat_info():
    """Get chat service info."""
    return JSONResponse({
        "service": "openrouter-chat",
        "status": "running",
        "description": "Real OpenRouter API chat integration",
        "active_conversations": len(CHAT_CONVERSATIONS),
        "supported_models": [
            "openai/gpt-4o-mini",
            "openai/gpt-4o",
            "anthropic/claude-3.5-sonnet",
            "anthropic/claude-3-haiku",
            "google/gemini-pro",
            "meta-llama/llama-3.1-8b-instruct"
        ],
        "endpoints": {
            "info": "GET /chat/",
            "message": "POST /chat/message",
            "conversations": "GET /chat/conversations",
            "health": "GET /chat/health"
        }
    })

@router.post("/message")
async def send_chat_message(request: ChatRequest):
    """Send a message to OpenRouter and get real AI response."""
    try:
        # Get API key
        api_key = request.api_key or os.getenv("LLM_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        
        if not api_key:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "OpenRouter API key required. Set LLM_API_KEY environment variable or provide in request.",
                    "timestamp": datetime.now().isoformat()
                }
            )
        
        # Get or create conversation
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        if conversation_id not in CHAT_CONVERSATIONS:
            CHAT_CONVERSATIONS[conversation_id] = {
                "id": conversation_id,
                "created_at": datetime.now().isoformat(),
                "messages": [],
                "model": request.model,
                "total_tokens": 0
            }
        
        # Add user message to conversation
        user_message = {
            "role": "user",
            "content": request.message,
            "timestamp": datetime.now().isoformat()
        }
        CHAT_CONVERSATIONS[conversation_id]["messages"].append(user_message)
        
        # Prepare messages for OpenRouter (last 10 messages to avoid token limit)
        conversation_messages = CHAT_CONVERSATIONS[conversation_id]["messages"][-10:]
        openrouter_messages = [
            {"role": msg["role"], "content": msg["content"]} 
            for msg in conversation_messages
        ]
        
        # Add system message for better responses
        system_message = {
            "role": "system",
            "content": "You are a helpful AI assistant. Provide clear, concise, and helpful responses."
        }
        openrouter_messages.insert(0, system_message)
        
        # Prepare OpenRouter API request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://huggingface.co/spaces/Minatoz997/Backend66",
            "X-Title": "OpenHands Backend Chat"
        }
        
        payload = {
            "model": request.model,
            "messages": openrouter_messages,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "stream": False  # For now, disable streaming
        }
        
        # Make request to OpenRouter
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            assistant_message_content = data["choices"][0]["message"]["content"]
            
            # Add assistant response to conversation
            assistant_message = {
                "role": "assistant",
                "content": assistant_message_content,
                "timestamp": datetime.now().isoformat(),
                "model": request.model
            }
            CHAT_CONVERSATIONS[conversation_id]["messages"].append(assistant_message)
            
            # Update token usage
            usage = data.get("usage", {})
            CHAT_CONVERSATIONS[conversation_id]["total_tokens"] += usage.get("total_tokens", 0)
            
            return JSONResponse({
                "conversation_id": conversation_id,
                "response": assistant_message_content,
                "model": request.model,
                "timestamp": datetime.now().isoformat(),
                "usage": usage,
                "status": "success",
                "message_count": len(CHAT_CONVERSATIONS[conversation_id]["messages"]),
                "total_tokens": CHAT_CONVERSATIONS[conversation_id]["total_tokens"]
            })
        
        elif response.status_code == 401:
            return JSONResponse(
                status_code=401,
                content={
                    "status": "error",
                    "message": "Invalid OpenRouter API key",
                    "timestamp": datetime.now().isoformat()
                }
            )
        
        elif response.status_code == 429:
            return JSONResponse(
                status_code=429,
                content={
                    "status": "error",
                    "message": "Rate limit exceeded. Please try again later.",
                    "timestamp": datetime.now().isoformat()
                }
            )
        
        else:
            error_data = response.text
            try:
                error_json = response.json()
                error_message = error_json.get("error", {}).get("message", error_data)
            except:
                error_message = error_data
            
            return JSONResponse(
                status_code=response.status_code,
                content={
                    "status": "error",
                    "message": f"OpenRouter API error: {error_message}",
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
                "message": f"Chat error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@router.get("/conversations")
async def list_chat_conversations():
    """List all chat conversations."""
    conversations = []
    for conv_id, conv_data in CHAT_CONVERSATIONS.items():
        conversations.append({
            "id": conv_id,
            "created_at": conv_data["created_at"],
            "message_count": len(conv_data["messages"]),
            "model": conv_data.get("model", "unknown"),
            "total_tokens": conv_data.get("total_tokens", 0),
            "last_message": conv_data["messages"][-1]["timestamp"] if conv_data["messages"] else None
        })
    
    return JSONResponse({
        "status": "success",
        "total_conversations": len(conversations),
        "conversations": conversations
    })

@router.get("/conversations/{conversation_id}")
async def get_chat_conversation(conversation_id: str):
    """Get a specific chat conversation."""
    if conversation_id not in CHAT_CONVERSATIONS:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return JSONResponse({
        "status": "success",
        "conversation": CHAT_CONVERSATIONS[conversation_id]
    })

@router.delete("/conversations/{conversation_id}")
async def delete_chat_conversation(conversation_id: str):
    """Delete a specific chat conversation."""
    if conversation_id not in CHAT_CONVERSATIONS:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    del CHAT_CONVERSATIONS[conversation_id]
    
    return JSONResponse({
        "status": "success",
        "message": f"Deleted conversation {conversation_id}",
        "remaining_conversations": len(CHAT_CONVERSATIONS)
    })

@router.get("/health")
async def chat_health():
    """Health check for chat service."""
    api_key_available = bool(os.getenv("LLM_API_KEY") or os.getenv("OPENROUTER_API_KEY"))
    
    return JSONResponse({
        "status": "healthy",
        "service": "openrouter-chat",
        "api_key_configured": api_key_available,
        "active_conversations": len(CHAT_CONVERSATIONS),
        "openrouter_endpoint": "https://openrouter.ai/api/v1/chat/completions",
        "timestamp": datetime.now().isoformat()
    })

@router.get("/models")
async def get_chat_models():
    """Get available models for chat."""
    return JSONResponse({
        "status": "success",
        "models": [
            {
                "id": "openai/gpt-4o-mini",
                "name": "GPT-4o Mini",
                "description": "Fast and efficient model",
                "recommended": True
            },
            {
                "id": "openai/gpt-4o",
                "name": "GPT-4o",
                "description": "Most capable OpenAI model"
            },
            {
                "id": "anthropic/claude-3.5-sonnet",
                "name": "Claude 3.5 Sonnet",
                "description": "Anthropic's most capable model"
            },
            {
                "id": "anthropic/claude-3-haiku",
                "name": "Claude 3 Haiku",
                "description": "Fast and efficient Claude model"
            },
            {
                "id": "google/gemini-pro",
                "name": "Gemini Pro",
                "description": "Google's advanced model"
            },
            {
                "id": "meta-llama/llama-3.1-8b-instruct",
                "name": "Llama 3.1 8B",
                "description": "Meta's open source model"
            }
        ]
    })