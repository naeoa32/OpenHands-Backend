# OpenHands Backend with Novel Writing Mode

Backend API untuk aplikasi OpenHands yang mendukung **Novel Writing Mode** - AI assistant khusus untuk creative writing dalam bahasa Indonesia menggunakan OpenRouter API.

## ✨ Features

### 🎨 **Novel Writing Mode**
- **Indonesian Creative Writing Focus** - Native Indonesian prompts dan cultural understanding
- **Intelligent Model Selection** - Automatic switching antara Claude 3.5 Haiku (budget) dan Claude 3 Opus (premium)
- **Template-Based Assistance** - 7 specialized templates untuk berbagai aspek penulisan
- **No Generic Responses** - AI selalu bertanya detail spesifik sebelum memberikan saran
- **Real-time WebSocket** - Komunikasi real-time dengan frontend

### 🤖 **Supported Templates**
- `character-development` - Pengembangan karakter yang kompleks
- `plot-structure` - Bantuan struktur cerita dan plot
- `dialogue-writing` - Penulisan dialog yang natural
- `world-building` - Membangun dunia cerita yang immersive
- `style-voice` - Mengembangkan gaya dan suara penulis
- `theme-symbolism` - Eksplorasi tema dan simbolisme
- `editing-revision` - Bantuan editing dan revisi

## 🚀 Deployment di Render

### Quick Deploy
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Manual Deployment

1. **Fork repository ini**
2. **Buat Web Service di Render:**
   - Connect repository Anda
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m openhands.server.listen --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables (Required):**
   ```bash
   # OpenRouter API (Required)
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   LLM_API_KEY=your_openrouter_api_key_here
   SESSION_API_KEY=your_session_api_key_here
   
   # CORS Configuration
   CORS_ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
   
   # Server Configuration
   DEBUG=false
   SERVE_FRONTEND=false
   ```

## 🔧 Local Development

### Prerequisites
- Python 3.12+
- Poetry (recommended) atau pip

### Installation

#### Dengan Poetry:
```bash
poetry install
poetry run python -m openhands.server
```

#### Dengan pip:
```bash
pip install -r requirements.txt
python -m openhands.server
```

### Environment Variables
Copy `.env.example` ke `.env` dan isi dengan konfigurasi Anda:

```bash
cp .env.example .env
```

## 🔑 API Configuration

### OpenRouter API (Required)
Backend ini **100% menggunakan OpenRouter API** untuk akses ke Claude models:

1. **Daftar di [OpenRouter](https://openrouter.ai/)**
2. **Deposit balance** untuk usage
3. **Dapatkan API key** dari dashboard
4. **Set environment variables:**
   ```bash
   OPENROUTER_API_KEY=or-your-api-key-here
   LLM_API_KEY=or-your-api-key-here  # Same as above
   ```

### Model Pricing via OpenRouter
- **Claude 3.5 Haiku** (Budget): ~$0.25/1M input tokens, ~$1.25/1M output tokens
- **Claude 3 Opus** (Premium): ~$15/1M input tokens, ~$75/1M output tokens

**Note:** Tidak perlu API key dari OpenAI, Anthropic, atau Google. Semua akses melalui OpenRouter.

## 📡 API Endpoints

### Health Check
- `GET /api/health` - Server health status

### WebSocket Communication
- `WebSocket /socket.io/` - Real-time communication untuk Novel Writing Mode

### Novel Writing Mode Usage
Send via WebSocket:
```json
{
  "action": "message",
  "args": {
    "content": "Enhanced prompt dari novel service",
    "novel_mode": true,
    "original_prompt": "Input asli user",
    "template_used": "character-development"
  }
}
```

## 🔧 Full Environment Variables

Copy dari `.env.example` dan sesuaikan:

```bash
# Server Configuration
PORT=8000
HOST=0.0.0.0
CORS_ALLOWED_ORIGINS=*

# OpenRouter API Configuration (Required)
OPENROUTER_API_KEY=your_openrouter_api_key_here
LLM_API_KEY=your_openrouter_api_key_here
LLM_BASE_URL=https://openrouter.ai/api/v1

# Default LLM Model
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307

# Novel Writing Mode Configuration
NOVEL_WRITING_BUDGET_MODEL=openrouter/anthropic/claude-3-haiku-20240307
NOVEL_WRITING_PREMIUM_MODEL=openrouter/anthropic/claude-3-opus-20240229

# Novel Writing Mode Thresholds (configurable)
NOVEL_PREMIUM_CONTENT_THRESHOLD=1500
NOVEL_PREMIUM_COMPLEXITY_THRESHOLD=3
NOVEL_FORCE_PREMIUM_MODE=false

# OpenRouter Specific Headers
OR_SITE_URL=https://docs.all-hands.dev/
OR_APP_NAME=OpenHands-NovelWriting

# Session Configuration
SESSION_API_KEY=your_session_api_key_here
RUNTIME=eventstream
DEFAULT_AGENT=CodeActAgent
MAX_CONCURRENT_CONVERSATIONS=5

# Security & Performance
SECURITY_CONFIRMATION_MODE=false
FILE_STORE_PATH=/tmp/openhands_storage
LOG_LEVEL=INFO
DEBUG=false
SERVE_FRONTEND=false
ENABLE_AUTO_LINT=false
ENABLE_AUTO_TEST=false
```

## 🎨 Novel Writing Mode Integration

### Frontend Integration
```javascript
import io from 'socket.io-client';

const socket = io('https://your-backend.onrender.com', {
  query: {
    conversation_id: 'your-conversation-id',
    latest_event_id: -1
  }
});

// Activate Novel Writing Mode
socket.emit('oh_user_action', {
  action: 'message',
  args: {
    content: 'Bantu saya mengembangkan karakter protagonis',
    novel_mode: true,
    original_prompt: 'Saya butuh bantuan karakter',
    template_used: 'character-development'
  }
});

// Listen for AI responses
socket.on('oh_event', (data) => {
  console.log('AI Response:', data);
});
```

## 🔒 Security Features

- **SecretStr API Key Handling** - API keys tidak ter-expose di logs
- **Session Isolation** - Setiap novel writing session terisolasi
- **CORS Configuration** - Dikonfigurasi untuk frontend domain
- **Environment-based Configuration** - Semua sensitive data via environment variables
- **Error Handling** - Proper error classification tanpa expose internal details

## 📚 Documentation

- [Novel Writing Mode Guide](./NOVEL_WRITING_MODE.md)
- [Render Deployment Guide](./RENDER_DEPLOYMENT.md)
- [Security Improvements](./SECURITY_IMPROVEMENTS.md)

## 🧪 Testing

```bash
# Test implementation
python test_novel_mode.py

# Verify all components
python verify_implementation.py

# Start server with novel mode
python start_novel_server.py
```

## 📝 License

MIT License
