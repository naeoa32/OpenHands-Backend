---
title: Personal OpenHands Backend
emoji: 💕
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# 💕 Personal OpenHands Backend

A powerful AI agent backend made for you and your girlfriend! OpenRouter-only, no Google Cloud, simple authentication, and optimized for Hugging Face Spaces.

## 🚀 Quick Start

This Space provides a personal AI assistant backend for you and your girlfriend only! Simple authentication protects your privacy.

### 🔐 Authentication Required

Most endpoints require a Bearer token for security. You need to set a `PERSONAL_ACCESS_TOKEN` in your HF Spaces environment variables.

**What is Personal Access Token?** It's like a simple password to protect your AI backend so only you and your girlfriend can use it!

### 📋 Required Setup

Set these environment variables in your HF Spaces settings:

```bash
# Required - Your OpenRouter API key
LLM_API_KEY=your_openrouter_api_key

# Required - Your personal password/token (choose any password you like!)
PERSONAL_ACCESS_TOKEN=your_chosen_password_here

# Optional - LLM configuration (defaults provided)
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307
LLM_BASE_URL=https://openrouter.ai/api/v1
```

### 🔑 How to Create Personal Access Token

**Simple & Easy:** Just choose any password you like!

```bash
# Examples (choose one or create your own):
PERSONAL_ACCESS_TOKEN=backend-for-us-2024
PERSONAL_ACCESS_TOKEN=love-you-babe-123
PERSONAL_ACCESS_TOKEN=our-private-ai-key
PERSONAL_ACCESS_TOKEN=ai-assistant-secret
```

**Where to set it:**
1. Go to your HF Space settings
2. Add environment variable: `PERSONAL_ACCESS_TOKEN`
3. Set the value to your chosen password
4. Save and restart your space

### 🌐 API Endpoints

```bash
# Health check (public - no token needed)
GET /health

# Personal info (protected - token needed)
GET /personal-info
Authorization: Bearer your_chosen_password

# OpenHands API endpoints (protected - token needed)
GET /api/options/config
Authorization: Bearer your_chosen_password

# Create conversation (protected - token needed)
POST /api/conversations
Authorization: Bearer your_chosen_password
Content-Type: application/json
{
  "initial_user_msg": "Hello! Can you help me with coding?"
}

# 🚀 NEW: Fizzo.org Auto-Update (public)
POST /api/fizzo-auto-update
Content-Type: application/json
{
  "email": "your_email@gmail.com",
  "password": "your_password",
  "chapter_title": "Bab 28: Judul Chapter",
  "chapter_content": "Isi chapter novel minimal 1000 karakter..."
}
```

### 💻 Example Usage

```javascript
// Create a new conversation with authentication
const API_TOKEN = 'backend-for-us-2024'; // Your chosen password

const response = await fetch('https://your-space.hf.space/api/conversations', {
  method: 'POST',
  headers: { 
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_TOKEN}`
  },
  body: JSON.stringify({
    initial_user_msg: 'Write a Python function to calculate fibonacci numbers'
  })
});

const conversation = await response.json();
console.log(conversation);
```

### 🧪 Test Your Setup

```bash
# Test without token (should work)
curl https://your-space.hf.space/health

# Test with token (should work)
curl -H "Authorization: Bearer your_chosen_password" \
     https://your-space.hf.space/personal-info

# Test without token on protected endpoint (should fail)
curl https://your-space.hf.space/personal-info
```

## 🤖 Available AI Agents

Your backend includes 5 powerful AI agents:

1. **CodeActAgent** ⭐ (Default) - Complete coding assistant
2. **BrowsingAgent** 🌐 - Web research and automation
3. **ReadOnlyAgent** 📖 - Safe code review and analysis
4. **LocAgent** 🎯 - Targeted code generation
5. **VisualBrowsingAgent** 👁️ - Visual web interaction (limited in HF Spaces)

## 🌐 Frontend Integration

This backend works perfectly with frontends deployed on:
- **Vercel** (*.vercel.app)
- **Netlify** (*.netlify.app) 
- **GitHub Pages** (*.github.io)
- **Local development** (localhost)

CORS is pre-configured to allow these domains.

## 🔧 Features

- 🔐 **Personal Authentication** - Only you and your girlfriend can access
- ✅ **OpenRouter Only** - No need for multiple API keys
- ✅ **Local Runtime** - Works without Docker in container
- ✅ **CORS Enabled** - Ready for frontend integration
- ✅ **No Google Cloud** - Zero Google dependencies
- ✅ **HF Spaces Optimized** - Perfect for Hugging Face deployment
- ✅ **Indonesian Novel Writing** - Special support for creative writing
- ✅ **All-in-One File** - Single app.py file, no confusion
- 🚀 **NEW: Fizzo.org Auto-Update** - Automated novel chapter publishing

## 🎯 Use Cases

- **AI Coding Assistant**: Help with programming tasks
- **Web Automation**: Browse and interact with websites  
- **Code Execution**: Run and test code snippets
- **Research Assistant**: Gather information from multiple sources
- **Educational Tools**: Interactive learning experiences
- **Novel Writing**: Indonesian creative writing support
- 🚀 **Novel Publishing**: Auto-update chapters to fizzo.org platform

## 🔒 Security & Privacy

- **Bearer Token Authentication**: Simple password protection
- **No Google Login**: No complex OAuth setup needed
- **Private Access**: Only you and your girlfriend can use it
- **API Key Protection**: Your OpenRouter key is protected
- **CORS Security**: Only allowed domains can access

## 📚 Documentation

- **OpenHands GitHub**: [All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)
- **LLM Provider**: [OpenRouter](https://openrouter.ai)
- **Frontend Examples**: Deploy your own UI on Vercel

## 🚨 Troubleshooting

### "Invalid personal access token" error:
1. Check if you set `PERSONAL_ACCESS_TOKEN` in HF Spaces environment variables
2. Make sure you're using the same token in your API calls
3. Restart your HF Space after setting the token

### "Missing LLM_API_KEY" error:
1. Get your API key from [OpenRouter](https://openrouter.ai)
2. Set `LLM_API_KEY` in HF Spaces environment variables
3. Restart your HF Space

### Agent not working:
1. Check if your OpenRouter API key has credits
2. Try a different model (set `LLM_MODEL` environment variable)
3. Check the logs in HF Spaces

## 📝 License

MIT License - Feel free to use in your projects!

---

**Ready to build AI-powered applications?** 🚀 

Start by setting up your environment variables and calling the API endpoints above!# Auto deploy test - Sat Jun 21 22:57:03 UTC 2025
