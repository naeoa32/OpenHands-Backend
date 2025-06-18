"""
Novel Writing Mode API endpoints
Specialized endpoints for Indonesian creative writing assistance
"""
import os
import uuid
import json
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from openhands.core.novel_writing_prompts import (
    create_novel_writing_prompt, 
    get_novel_writing_questions,
    NOVEL_WRITING_QUESTIONS
)
from openhands.core.novel_writing_config import (
    create_novel_writing_llm_config,
    should_use_premium_model,
    get_novel_writing_model_info,
    NovelWritingConfig
)

router = APIRouter(prefix="/novel", tags=["novel-writing"])

# In-memory storage for novel writing sessions
NOVEL_SESSIONS: Dict[str, Dict] = {}

class NovelWritingRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    template: Optional[str] = None
    original_prompt: Optional[str] = None
    force_premium: Optional[bool] = False
    api_key: Optional[str] = None

class NovelWritingResponse(BaseModel):
    session_id: str
    response: str
    template_used: Optional[str]
    model_info: Dict
    questions: List[str]
    timestamp: str
    status: str

@router.get("/")
async def novel_info():
    """Get novel writing service information."""
    return JSONResponse({
        "service": "novel-writing",
        "status": "running",
        "description": "Indonesian creative writing assistance with AI",
        "active_sessions": len(NOVEL_SESSIONS),
        "supported_templates": list(NOVEL_WRITING_QUESTIONS.keys()),
        "features": [
            "Indonesian language prompts",
            "Template-based assistance",
            "Intelligent model selection",
            "Creative writing optimization",
            "Character development",
            "Plot structure guidance",
            "Dialogue writing help",
            "World building assistance"
        ],
        "endpoints": {
            "info": "GET /novel/",
            "write": "POST /novel/write",
            "templates": "GET /novel/templates",
            "questions": "GET /novel/questions/{template}",
            "sessions": "GET /novel/sessions",
            "health": "GET /novel/health"
        }
    })

@router.post("/write")
async def novel_write(request: NovelWritingRequest):
    """Process novel writing request with specialized AI assistance."""
    try:
        # Get or create session
        session_id = request.session_id or str(uuid.uuid4())
        
        if session_id not in NOVEL_SESSIONS:
            NOVEL_SESSIONS[session_id] = {
                "id": session_id,
                "created_at": datetime.now().isoformat(),
                "messages": [],
                "template_history": [],
                "total_interactions": 0
            }
        
        session = NOVEL_SESSIONS[session_id]
        
        # Determine model selection
        use_premium = request.force_premium or should_use_premium_model(
            request.template,
            len(request.message)
        )
        
        # Get model information
        model_info = get_novel_writing_model_info(use_premium)
        
        # Create specialized prompt
        system_prompt = create_novel_writing_prompt(
            request.template,
            request.original_prompt or request.message
        )
        
        # Get template-specific questions
        questions = get_novel_writing_questions(request.template) if request.template else []
        
        # Add to session history
        user_message = {
            "role": "user",
            "content": request.message,
            "template": request.template,
            "timestamp": datetime.now().isoformat(),
            "original_prompt": request.original_prompt
        }
        session["messages"].append(user_message)
        
        if request.template:
            session["template_history"].append(request.template)
        
        session["total_interactions"] += 1
        
        # Get API key
        api_key = request.api_key or os.getenv("LLM_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        
        if not api_key:
            # Return helpful response without API call
            response_content = _create_helpful_response(request, questions, model_info)
        else:
            # Make actual API call to OpenRouter
            response_content = await _call_openrouter_api(
                request, system_prompt, session, api_key, model_info
            )
        
        # Add AI response to session
        ai_message = {
            "role": "assistant",
            "content": response_content,
            "model": model_info["model"],
            "template": request.template,
            "timestamp": datetime.now().isoformat()
        }
        session["messages"].append(ai_message)
        
        return JSONResponse({
            "session_id": session_id,
            "response": response_content,
            "template_used": request.template,
            "model_info": model_info,
            "questions": questions,
            "timestamp": datetime.now().isoformat(),
            "status": "success",
            "session_stats": {
                "total_interactions": session["total_interactions"],
                "templates_used": list(set(session["template_history"])),
                "message_count": len(session["messages"])
            }
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Novel writing error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

def _create_helpful_response(request: NovelWritingRequest, questions: List[str], model_info: Dict) -> str:
    """Create helpful response when API key is not available."""
    template_name = request.template or "umum"
    
    response = f"""🎭 **Mode Penulisan Novel Aktif** - Template: {template_name.title()}

Saya siap membantu Anda mengembangkan cerita dengan pendekatan yang mendalam dan personal. 

**Untuk permintaan Anda:** "{request.message}"

**Pertanyaan yang akan membantu mengembangkan ide:**"""
    
    for i, question in enumerate(questions[:3], 1):
        response += f"\n{i}. {question}"
    
    response += f"""

**Model yang direkomendasikan:** {model_info['name']} ({model_info['tier']})
- {model_info['strengths'][0] if model_info['strengths'] else 'Optimal untuk penulisan kreatif'}

**Langkah selanjutnya:**
1. Jawab salah satu pertanyaan di atas untuk detail yang lebih spesifik
2. Berikan konteks tambahan tentang cerita Anda
3. Sebutkan genre atau gaya penulisan yang diinginkan

*Catatan: Untuk respons AI yang lengkap, silakan atur API key OpenRouter.*"""
    
    return response

async def _call_openrouter_api(request: NovelWritingRequest, system_prompt: str, 
                              session: Dict, api_key: str, model_info: Dict) -> str:
    """Make actual API call to OpenRouter for novel writing."""
    import requests
    
    # Prepare conversation history (last 6 messages for context)
    conversation_messages = session["messages"][-6:]
    openrouter_messages = [
        {"role": msg["role"], "content": msg["content"]} 
        for msg in conversation_messages
    ]
    
    # Add system prompt
    openrouter_messages.insert(0, {
        "role": "system", 
        "content": system_prompt
    })
    
    # Add current user message
    openrouter_messages.append({
        "role": "user",
        "content": request.message
    })
    
    # Prepare API request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://huggingface.co/spaces/Minatoz997/Backend66",
        "X-Title": "OpenHands Novel Writing"
    }
    
    # Use novel writing optimized parameters
    config = NovelWritingConfig()
    payload = {
        "model": model_info["model"],
        "messages": openrouter_messages,
        "max_tokens": config.max_output_tokens,
        "temperature": config.temperature,
        "top_p": config.top_p,
        "stream": False
    }
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60
    )
    
    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        raise Exception(f"OpenRouter API error: {response.status_code} - {response.text}")

@router.get("/templates")
async def get_novel_templates():
    """Get available novel writing templates."""
    templates = []
    for template_id, questions in NOVEL_WRITING_QUESTIONS.items():
        template_info = {
            "id": template_id,
            "name": template_id.replace("-", " ").title(),
            "description": _get_template_description(template_id),
            "question_count": len(questions),
            "sample_questions": questions[:2]
        }
        templates.append(template_info)
    
    return JSONResponse({
        "status": "success",
        "total_templates": len(templates),
        "templates": templates
    })

def _get_template_description(template_id: str) -> str:
    """Get description for template."""
    descriptions = {
        "character-development": "Mengembangkan karakter yang kompleks dan relatable",
        "plot-structure": "Membangun struktur cerita yang menarik dan koheren",
        "dialogue-writing": "Menulis dialog yang natural dan berkarakter",
        "world-building": "Menciptakan dunia cerita yang immersive",
        "style-voice": "Mengembangkan gaya dan suara penulisan yang unik",
        "theme-symbolism": "Mengeksplorasi tema dan simbolisme yang mendalam",
        "editing-revision": "Merevisi dan memperbaiki draft dengan efektif"
    }
    return descriptions.get(template_id, "Template penulisan kreatif")

@router.get("/questions/{template}")
async def get_template_questions(template: str):
    """Get questions for specific template."""
    if template not in NOVEL_WRITING_QUESTIONS:
        raise HTTPException(status_code=404, detail="Template not found")
    
    questions = get_novel_writing_questions(template)
    
    return JSONResponse({
        "status": "success",
        "template": template,
        "template_name": template.replace("-", " ").title(),
        "description": _get_template_description(template),
        "questions": questions,
        "question_count": len(questions)
    })

@router.get("/sessions")
async def list_novel_sessions():
    """List all novel writing sessions."""
    sessions = []
    for session_id, session_data in NOVEL_SESSIONS.items():
        sessions.append({
            "id": session_id,
            "created_at": session_data["created_at"],
            "total_interactions": session_data["total_interactions"],
            "templates_used": list(set(session_data.get("template_history", []))),
            "message_count": len(session_data["messages"]),
            "last_activity": session_data["messages"][-1]["timestamp"] if session_data["messages"] else None
        })
    
    return JSONResponse({
        "status": "success",
        "total_sessions": len(sessions),
        "sessions": sessions
    })

@router.get("/sessions/{session_id}")
async def get_novel_session(session_id: str):
    """Get specific novel writing session."""
    if session_id not in NOVEL_SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return JSONResponse({
        "status": "success",
        "session": NOVEL_SESSIONS[session_id]
    })

@router.delete("/sessions/{session_id}")
async def delete_novel_session(session_id: str):
    """Delete specific novel writing session."""
    if session_id not in NOVEL_SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")
    
    del NOVEL_SESSIONS[session_id]
    
    return JSONResponse({
        "status": "success",
        "message": f"Deleted novel session {session_id}",
        "remaining_sessions": len(NOVEL_SESSIONS)
    })

@router.get("/health")
async def novel_health():
    """Health check for novel writing service."""
    api_key_available = bool(os.getenv("LLM_API_KEY") or os.getenv("OPENROUTER_API_KEY"))
    
    return JSONResponse({
        "status": "healthy",
        "service": "novel-writing",
        "api_key_configured": api_key_available,
        "active_sessions": len(NOVEL_SESSIONS),
        "supported_templates": len(NOVEL_WRITING_QUESTIONS),
        "features_available": [
            "Indonesian prompts",
            "Template assistance", 
            "Model selection",
            "Creative optimization"
        ],
        "timestamp": datetime.now().isoformat()
    })

@router.get("/models")
async def get_novel_models():
    """Get available models for novel writing."""
    budget_info = get_novel_writing_model_info(False)
    premium_info = get_novel_writing_model_info(True)
    
    return JSONResponse({
        "status": "success",
        "models": {
            "budget": budget_info,
            "premium": premium_info
        },
        "selection_criteria": {
            "content_length_threshold": "1500 characters",
            "complex_templates": ["style-voice", "theme-symbolism", "editing-revision"],
            "premium_recommended_for": ["Professional writing", "Complex narratives", "Literary fiction"]
        }
    })