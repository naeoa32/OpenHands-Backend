---
title: OpenHands Backend API
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# 🤖 OpenHands Backend API

A powerful AI agent backend that can execute code, browse the web, and interact with various tools. Perfect for building AI-powered applications!

## 🚀 Quick Start

This Space provides a ready-to-use API for OpenHands AI agent. No authentication required for testing!

### API Endpoints

```bash
# Get configuration
GET /api/options/config

# Create conversation
POST /api/conversations
Content-Type: application/json
{
  "initial_user_msg": "Hello! Can you help me with coding?"
}

# Health check
GET /health
```

### Example Usage

```javascript
// Create a new conversation
const response = await fetch('https://your-space.hf.space/api/conversations', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    initial_user_msg: 'Write a Python function to calculate fibonacci numbers'
  })
});

const conversation = await response.json();
console.log(conversation);
```

## ⚙️ Configuration

Set these environment variables in your Space settings:

```bash
# Required for LLM functionality
LLM_API_KEY=your_openrouter_api_key
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307
LLM_BASE_URL=https://openrouter.ai/api/v1

# Optional
SESSION_API_KEY=your_session_key
DEBUG=false
```

## 🌐 Frontend Integration

This backend works perfectly with frontends deployed on:
- **Vercel** (*.vercel.app)
- **Netlify** (*.netlify.app) 
- **GitHub Pages** (*.github.io)
- **Local development** (localhost)

CORS is pre-configured to allow these domains.

## 🔧 Features

- ✅ **Public API** - No authentication required
- ✅ **Local Runtime** - Works without Docker in container
- ✅ **CORS Enabled** - Ready for frontend integration
- ✅ **Multiple LLM Support** - OpenRouter, OpenAI, Anthropic
- ✅ **Anonymous Conversations** - Start chatting immediately
- ✅ **Mobile Optimized** - Perfect for mobile development

## 📚 Documentation

- **OpenHands GitHub**: [All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)
- **LLM Provider**: [OpenRouter](https://openrouter.ai)
- **Frontend Examples**: Deploy your own UI on Vercel

## 🎯 Use Cases

- **AI Coding Assistant**: Help with programming tasks
- **Web Automation**: Browse and interact with websites  
- **Code Execution**: Run and test code snippets
- **Research Assistant**: Gather information from multiple sources
- **Educational Tools**: Interactive learning experiences

## 📝 License

MIT License - Feel free to use in your projects!

---

**Ready to build AI-powered applications?** 🚀 

Start by calling the API endpoints above or integrate with your frontend!