# Environment Variables Guide

## 🔑 Complete Environment Variables for OpenHands Backend with Novel Writing Mode

This guide provides all environment variables needed for deployment, especially for **Render deployment** with **OpenRouter API integration**.

## ✅ Required Variables

### 🚀 **OpenRouter API (Required)**
```bash
# Primary API configuration - 100% OpenRouter
OPENROUTER_API_KEY=your_openrouter_api_key_here
LLM_API_KEY=your_openrouter_api_key_here  # Same as above
LLM_BASE_URL=https://openrouter.ai/api/v1
```

### 🔐 **Session Security**
```bash
SESSION_API_KEY=your_session_api_key_here  # Generate random string
```

## 🎯 Novel Writing Mode Configuration

### 🤖 **Model Selection**
```bash
# Default model (overridden in novel mode)
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307

# Novel Writing Mode specific models
NOVEL_WRITING_BUDGET_MODEL=openrouter/anthropic/claude-3-haiku-20240307
NOVEL_WRITING_PREMIUM_MODEL=openrouter/anthropic/claude-3-opus-20240229
```

### ⚙️ **Smart Model Selection Thresholds**
```bash
# Content length threshold for premium model (characters)
NOVEL_PREMIUM_CONTENT_THRESHOLD=1500

# Template complexity threshold (1-3, 3=premium)
NOVEL_PREMIUM_COMPLEXITY_THRESHOLD=3

# Force premium mode for testing (true/false)
NOVEL_FORCE_PREMIUM_MODE=false
```

### 📊 **OpenRouter Headers**
```bash
OR_SITE_URL=https://docs.all-hands.dev/
OR_APP_NAME=OpenHands-NovelWriting
```

## 🌐 Server Configuration

### 🖥️ **Basic Server Settings**
```bash
PORT=8000
HOST=0.0.0.0
DEBUG=false
SERVE_FRONTEND=false
```

### 🔒 **CORS Configuration**
```bash
# Development
CORS_ALLOWED_ORIGINS=*

# Production (recommended)
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app,https://your-custom-domain.com
```

## 🤖 Agent & Runtime Configuration

### 🎯 **Agent Settings**
```bash
RUNTIME=eventstream
DEFAULT_AGENT=CodeActAgent
MAX_CONCURRENT_CONVERSATIONS=5
```

### 🔐 **Security Settings**
```bash
SECURITY_CONFIRMATION_MODE=false
FILE_STORE_PATH=/tmp/openhands_storage
LOG_LEVEL=info
```

### 🚫 **Disabled Features (for Novel Writing)**
```bash
ENABLE_AUTO_LINT=false
ENABLE_AUTO_TEST=false
```

## 📋 Complete .env Template

Copy this to your `.env` file:

```bash
# ============================================================================
# OpenHands Backend Environment Variables - Novel Writing Mode
# ============================================================================

# ============================================================================
# REQUIRED: OpenRouter API Configuration
# ============================================================================
OPENROUTER_API_KEY=your_openrouter_api_key_here
LLM_API_KEY=your_openrouter_api_key_here
LLM_BASE_URL=https://openrouter.ai/api/v1

# ============================================================================
# Server Configuration
# ============================================================================
PORT=8000
HOST=0.0.0.0
DEBUG=false
SERVE_FRONTEND=false
CORS_ALLOWED_ORIGINS=*

# ============================================================================
# Novel Writing Mode Configuration
# ============================================================================
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307
NOVEL_WRITING_BUDGET_MODEL=openrouter/anthropic/claude-3-haiku-20240307
NOVEL_WRITING_PREMIUM_MODEL=openrouter/anthropic/claude-3-opus-20240229
NOVEL_PREMIUM_CONTENT_THRESHOLD=1500
NOVEL_PREMIUM_COMPLEXITY_THRESHOLD=3
NOVEL_FORCE_PREMIUM_MODE=false
OR_SITE_URL=https://docs.all-hands.dev/
OR_APP_NAME=OpenHands-NovelWriting

# ============================================================================
# Session & Agent Configuration
# ============================================================================
SESSION_API_KEY=your_session_api_key_here
RUNTIME=eventstream
DEFAULT_AGENT=CodeActAgent
MAX_CONCURRENT_CONVERSATIONS=5

# ============================================================================
# Security & Performance
# ============================================================================
SECURITY_CONFIRMATION_MODE=false
FILE_STORE_PATH=/tmp/openhands_storage
LOG_LEVEL=info
ENABLE_AUTO_LINT=false
ENABLE_AUTO_TEST=false
```

## 🚀 Render Deployment Variables

For **Render deployment**, set these in your Render dashboard:

### **Required Variables:**
```bash
OPENROUTER_API_KEY=or-your-actual-api-key-here
LLM_API_KEY=or-your-actual-api-key-here
SESSION_API_KEY=generate-random-string-here
```

### **Optional (auto-configured by render.yaml):**
```bash
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307
NOVEL_WRITING_BUDGET_MODEL=openrouter/anthropic/claude-3-haiku-20240307
NOVEL_WRITING_PREMIUM_MODEL=openrouter/anthropic/claude-3-opus-20240229
OR_SITE_URL=https://docs.all-hands.dev/
OR_APP_NAME=OpenHands-NovelWriting
PORT=8000
HOST=0.0.0.0
CORS_ALLOWED_ORIGINS=*
```

## 💰 Cost Optimization Variables

### **Budget Control:**
```bash
# Lower threshold = more premium usage = higher cost
NOVEL_PREMIUM_CONTENT_THRESHOLD=1500

# Higher threshold = less premium usage = lower cost  
NOVEL_PREMIUM_COMPLEXITY_THRESHOLD=3

# Force budget mode for cost control
NOVEL_FORCE_PREMIUM_MODE=false
```

### **Model Costs via OpenRouter:**
- **Claude 3.5 Haiku (Budget)**: ~$0.25/1M input, ~$1.25/1M output
- **Claude 3 Opus (Premium)**: ~$15/1M input, ~$75/1M output

## 🔍 Variable Validation

### **Check Required Variables:**
```bash
# Test if variables are set
echo $OPENROUTER_API_KEY
echo $LLM_API_KEY
echo $SESSION_API_KEY
```

### **Test Configuration:**
```bash
# Run verification script
python verify_implementation.py

# Test novel mode
python test_novel_mode.py
```

## ❌ Deprecated Variables

**These are NOT needed** (backend uses 100% OpenRouter):

```bash
# NOT NEEDED - Backend uses OpenRouter only
# OPENAI_API_KEY=not_needed
# ANTHROPIC_API_KEY=not_needed  
# GOOGLE_API_KEY=not_needed
```

## 🔧 Development vs Production

### **Development:**
```bash
DEBUG=true
LOG_LEVEL=debug
CORS_ALLOWED_ORIGINS=*
NOVEL_FORCE_PREMIUM_MODE=false
```

### **Production:**
```bash
DEBUG=false
LOG_LEVEL=info
CORS_ALLOWED_ORIGINS=https://your-domain.com
NOVEL_FORCE_PREMIUM_MODE=false
```

## 🆘 Troubleshooting

### **Common Issues:**

1. **"API key not found"**
   ```bash
   # Check if OPENROUTER_API_KEY is set
   echo $OPENROUTER_API_KEY
   ```

2. **"Model not available"**
   ```bash
   # Verify model names have openrouter/ prefix
   LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307
   ```

3. **"CORS error"**
   ```bash
   # Set correct frontend domain
   CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
   ```

4. **"High costs"**
   ```bash
   # Increase thresholds to use budget model more
   NOVEL_PREMIUM_CONTENT_THRESHOLD=2000
   NOVEL_PREMIUM_COMPLEXITY_THRESHOLD=4
   ```

## 📚 Related Documentation

- [Novel Writing Mode Guide](./NOVEL_WRITING_MODE.md)
- [Render Deployment Guide](./RENDER_DEPLOYMENT.md)
- [Security Improvements](./SECURITY_IMPROVEMENTS.md)

---

**Ready for deployment with OpenRouter API! 🚀**