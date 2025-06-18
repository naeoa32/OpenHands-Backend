# 🚀 OpenHands Backend - Complete API Documentation

## 📋 Overview

This is a complete OpenHands backend implementation focused on **OpenRouter API integration** for HuggingFace Spaces deployment. All endpoints are designed to work without file system dependencies.

## 🔑 Environment Variables

```bash
# Required for real AI chat
LLM_API_KEY=your-openrouter-api-key

# Optional configurations
LLM_MODEL=openai/gpt-4o-mini
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_TEMPERATURE=0.7
```

## 🎯 Main Chat Endpoints

### 1. Real OpenRouter Chat (Recommended)
**The main chat endpoint with real AI responses**

```bash
POST /chat/message
```

**Request:**
```json
{
  "message": "Hello! How can you help me?",
  "conversation_id": "optional-uuid",
  "model": "openai/gpt-4o-mini",
  "api_key": "optional-if-env-set",
  "max_tokens": 1000,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "conversation_id": "uuid",
  "response": "Hello! I'm an AI assistant...",
  "model": "openai/gpt-4o-mini",
  "timestamp": "2025-01-18T...",
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 25,
    "total_tokens": 40
  },
  "status": "success"
}
```

**Features:**
- ✅ Real OpenRouter API integration
- ✅ Conversation memory (in-memory)
- ✅ Multiple model support
- ✅ Token usage tracking
- ✅ Error handling

### 2. Memory Chat (Fallback)
**Simple echo chat without API calls**

```bash
POST /memory-chat/message
```

**Request:**
```json
{
  "message": "Test message",
  "conversation_id": "optional-uuid",
  "model": "openai/gpt-4o-mini"
}
```

**Response:**
```json
{
  "conversation_id": "uuid",
  "response": "Echo from memory chat: Test message",
  "timestamp": "2025-01-18T...",
  "status": "success"
}
```

## 🧪 Testing Endpoints

### 3. OpenRouter Test
**Test OpenRouter API connectivity**

```bash
POST /openrouter/test
```

**Request:**
```json
{
  "message": "Test OpenRouter",
  "model": "openai/gpt-4o-mini",
  "api_key": "optional"
}
```

### 4. Simple Test Chat
**Basic test endpoint**

```bash
POST /test-chat/message
```

## 📊 Information Endpoints

### Health Checks
```bash
GET /health                    # Main health check
GET /chat/health              # Real chat health
GET /memory-chat/health       # Memory chat health
GET /openrouter/health        # OpenRouter health
```

### Service Information
```bash
GET /                         # Root API info with all endpoints
GET /chat/                    # Chat service info
GET /memory-chat/             # Memory chat info
GET /openrouter/              # OpenRouter test info
```

### Models and Configuration
```bash
GET /chat/models              # Available OpenRouter models
GET /openrouter/models        # OpenRouter models list
GET /api/options/config       # System configuration
```

## 💾 Conversation Management

### List Conversations
```bash
GET /chat/conversations       # Real chat conversations
GET /memory-chat/conversations # Memory chat conversations
```

### Get Specific Conversation
```bash
GET /chat/conversations/{id}
GET /memory-chat/conversations/{id}
```

### Delete Conversations
```bash
DELETE /chat/conversations/{id}        # Delete specific
DELETE /memory-chat/conversations      # Clear all memory
```

## 🔧 HuggingFace Spaces Endpoints

### Status and Debugging
```bash
GET /api/hf/status            # HF Spaces status
GET /api/hf/ready             # Readiness check
GET /api/hf/environment       # Environment info
GET /api/hf/debug             # Debug information
GET /api/hf/logs              # Application logs
```

### Test Endpoints
```bash
POST /api/hf/test-conversation # HF-specific test
GET /api/simple/health         # Simple health check
POST /api/simple/conversation  # Simple conversation test
```

## 📚 Documentation

```bash
GET /docs                     # Interactive API documentation
GET /openapi.json            # OpenAPI specification
```

## 🚀 Quick Start Guide

### 1. Basic Setup
```bash
# Set your OpenRouter API key
export LLM_API_KEY="your-openrouter-api-key"

# Start the server
python app_hf.py
```

### 2. Test Connection
```bash
curl -X GET "http://localhost:8000/"
```

### 3. Send First Message
```bash
curl -X POST "http://localhost:8000/chat/message" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! Can you help me with coding?",
    "model": "openai/gpt-4o-mini"
  }'
```

### 4. Continue Conversation
```bash
curl -X POST "http://localhost:8000/chat/message" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Write a Python function to calculate fibonacci",
    "conversation_id": "your-conversation-id-from-step-3",
    "model": "openai/gpt-4o-mini"
  }'
```

## 🎯 Supported Models

### OpenAI Models
- `openai/gpt-4o-mini` (Recommended - Fast & Efficient)
- `openai/gpt-4o` (Most Capable)

### Anthropic Models
- `anthropic/claude-3.5-sonnet` (Excellent for coding)
- `anthropic/claude-3-haiku` (Fast & Efficient)

### Google Models
- `google/gemini-pro`

### Meta Models
- `meta-llama/llama-3.1-8b-instruct`

## ⚡ Performance Features

### Memory Management
- ✅ All storage in memory (no file system)
- ✅ Conversation history (last 10 messages)
- ✅ Automatic token management
- ✅ Memory cleanup on restart

### Error Handling
- ✅ API key validation
- ✅ Rate limit handling
- ✅ Timeout management
- ✅ Graceful error responses

### HuggingFace Spaces Optimized
- ✅ No file system dependencies
- ✅ Memory-only storage
- ✅ Fast startup
- ✅ Minimal resource usage

## 🔒 Security Features

- ✅ API key protection
- ✅ Request validation
- ✅ Error message sanitization
- ✅ CORS enabled for frontend integration

## 📈 Monitoring

### Health Monitoring
```bash
GET /health                   # Overall system health
GET /chat/health             # Chat service status
```

### Usage Tracking
- Token usage per conversation
- Active conversation count
- Model usage statistics
- Error rate monitoring

## 🐛 Troubleshooting

### Common Issues

1. **"API key required" error**
   - Set `LLM_API_KEY` environment variable
   - Or provide `api_key` in request body

2. **"Rate limit exceeded"**
   - Wait a few seconds and retry
   - Consider using a different model

3. **"Timeout" error**
   - Check internet connection
   - Try a simpler request

4. **"Permission denied" errors**
   - Use memory-based endpoints (`/chat/` or `/memory-chat/`)
   - Avoid file-based endpoints

### Debug Endpoints
```bash
GET /api/hf/debug            # System debug info
GET /api/hf/environment      # Environment variables
GET /api/hf/logs             # Application logs
```

## 🎉 Success Indicators

When everything is working correctly, you should see:

✅ All health checks return 200  
✅ `/chat/message` accepts messages  
✅ Real AI responses from OpenRouter  
✅ Conversation memory works  
✅ No file permission errors  

## 📞 Support

For issues or questions:
1. Check the debug endpoints
2. Verify API key configuration
3. Test with simple endpoints first
4. Use memory-based endpoints for reliability

---

**🎯 This backend is specifically designed for OpenRouter integration and HuggingFace Spaces deployment!**