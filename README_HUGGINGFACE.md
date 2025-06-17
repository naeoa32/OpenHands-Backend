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

## 🚀 Features

- ✅ **Public API** - No authentication required for testing
- ✅ **Local Runtime** - Works without Docker (perfect for Hugging Face Spaces)
- ✅ **CORS Enabled** - Ready for frontend integration
- ✅ **Multiple LLM Support** - OpenRouter, OpenAI, Anthropic, etc.
- ✅ **Anonymous Conversations** - Start chatting immediately

## 🔧 API Endpoints

### Get Configuration
```bash
GET /api/options/config
```

### Create Conversation
```bash
POST /api/conversations
Content-Type: application/json

{
  "initial_user_msg": "Hello! Can you help me with coding?"
}
```

### Health Check
```bash
GET /health
```

## 🌐 Frontend Integration

This backend is designed to work with frontends deployed on:
- **Vercel** (vercel.app)
- **Netlify** (netlify.app) 
- **GitHub Pages** (github.io)
- **Local development** (localhost)

## ⚙️ Environment Variables

Set these in your Hugging Face Space settings:

```bash
# Required for LLM functionality
LLM_API_KEY=your_openrouter_api_key
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307
LLM_BASE_URL=https://openrouter.ai/api/v1

# Optional
SESSION_API_KEY=your_session_key
DEBUG=false
```

## 🎯 Usage Example

```javascript
// Frontend code example
const response = await fetch('https://your-space.hf.space/api/conversations', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    initial_user_msg: 'Write a Python function to calculate fibonacci numbers'
  })
});

const conversation = await response.json();
console.log(conversation);
```

## 🔗 Related

- **Frontend Demo**: Deploy your own frontend on Vercel
- **Documentation**: [OpenHands GitHub](https://github.com/All-Hands-AI/OpenHands)
- **LLM Provider**: [OpenRouter](https://openrouter.ai)

## 📝 License

MIT License - Feel free to use in your projects!

---

**Ready to build AI-powered applications?** 🚀 Start by calling the API endpoints above!