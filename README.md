# OpenHands Backend

Backend API untuk aplikasi OpenHands yang mendukung AI assistant dengan berbagai LLM providers termasuk OpenRouter.

## 🚀 Deployment di Render

### Quick Deploy
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/maxwin66/OpenHands-Backend)

### Manual Deployment

1. **Fork repository ini**
2. **Buat Web Service di Render:**
   - Connect repository Anda
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m openhands.server`

3. **Set Environment Variables:**
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key
   CORS_ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
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

## 🔑 API Keys

### OpenRouter (Recommended)
1. Daftar di [OpenRouter](https://openrouter.ai/)
2. Dapatkan API key
3. Set `OPENROUTER_API_KEY` di environment variables

### Provider Lain
- OpenAI: Set `OPENAI_API_KEY`
- Anthropic: Set `ANTHROPIC_API_KEY`
- Google: Set `GOOGLE_API_KEY`

## 📡 API Endpoints

- `GET /api/health` - Health check
- `POST /api/conversation` - Start conversation
- `WebSocket /socket.io` - Real-time communication

## 🐳 Docker

```bash
# Build
docker build -t openhands-backend .

# Run
docker run -p 3000:3000 -e OPENROUTER_API_KEY=your_key openhands-backend
```

## 🔒 Security

- CORS dikonfigurasi untuk frontend domain
- Rate limiting untuk API endpoints
- JWT authentication support

## 📝 License

MIT License
