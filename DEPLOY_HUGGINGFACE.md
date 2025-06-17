# 🤗 Hugging Face Spaces Deployment Guide

## 📋 Quick Deploy Steps

### 1. Create New Space
- Go to [huggingface.co/new-space](https://huggingface.co/new-space)
- **Space name**: `openhands-backend` (or any name you prefer)
- **SDK**: Docker
- **Visibility**: Public
- **Hardware**: CPU basic (free tier)

### 2. Upload Files
Upload these files to your Space:

**Required files:**
- `Dockerfile` (main container config)
- `app_hf.py` (entry point for HF Spaces)
- `requirements.txt` (Python dependencies)
- `README.md` (with HF metadata)
- `openhands/` folder (entire application code)

### 3. Set Environment Variables
In your Space Settings → Environment Variables:

```bash
# Required
LLM_API_KEY=your_openrouter_api_key
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307
LLM_BASE_URL=https://openrouter.ai/api/v1

# Optional
SESSION_API_KEY=random_string_123
DEBUG=false
```

### 4. Deploy!
- HF will automatically build and deploy
- Your API will be available at: `https://your-username-space-name.hf.space`

## 🔧 Configuration Details

### Dockerfile
- Uses Python 3.12 slim image
- Installs system dependencies (git, curl, build-essential)
- Exposes port 7860 (HF Spaces requirement)
- Uses local runtime (no Docker needed in container)

### app_hf.py
- Entry point optimized for HF Spaces
- Configures port 7860 and host 0.0.0.0
- Sets up CORS for frontend integration
- Provides startup logging and diagnostics

### Environment Variables
- `OPENHANDS_RUNTIME=local` (no Docker in container)
- `CORS_ALLOWED_ORIGINS=*` (allows all frontends)
- `PORT=7860` (HF Spaces standard)
- `FILE_STORE_PATH=/tmp/openhands` (writable directory for file storage)
- `CACHE_DIR=/tmp/cache` (writable directory for caching)

## 🌐 Frontend Integration

Your deployed backend will work with frontends on:
- Vercel (*.vercel.app)
- Netlify (*.netlify.app)
- GitHub Pages (*.github.io)
- Local development (localhost)

## 🚀 API Endpoints

Once deployed, test these endpoints:

```bash
# Health check
GET https://your-space.hf.space/health

# Get config
GET https://your-space.hf.space/api/options/config

# Create conversation
POST https://your-space.hf.space/api/conversations
Content-Type: application/json
{
  "initial_user_msg": "Hello!"
}
```

## 🎯 Next Steps

1. **Deploy Backend**: Follow steps above
2. **Create Frontend**: Deploy UI on Vercel
3. **Connect**: Point frontend to your HF Space URL
4. **Test**: Create conversations and chat with AI!

## 💡 Tips

- **Free Tier**: CPU basic is sufficient for testing
- **Public Spaces**: Required for free tier
- **Environment Variables**: Set LLM_API_KEY for full functionality
- **CORS**: Pre-configured for common frontend platforms
- **Monitoring**: Check Space logs for debugging

Happy deploying! 🚀