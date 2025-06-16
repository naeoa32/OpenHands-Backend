# OpenHands Backend - Render Deployment Guide

## 🚀 Quick Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## Overview

This OpenHands Backend is optimized for **Novel Writing Mode** - a specialized AI assistant for Indonesian creative writing. The backend integrates with OpenRouter API to provide intelligent, context-aware writing assistance.

## Features

### 🎨 Novel Writing Mode
- **Intelligent Model Selection**: Automatic switching between Claude 3.5 Haiku (budget) and Claude 3 Opus (premium)
- **Indonesian Language Focus**: Native Indonesian prompts and cultural understanding
- **Template-Based Assistance**: Character development, plot structure, dialogue writing, etc.
- **No Generic Responses**: AI always asks specific questions before giving advice

### 🔧 Technical Features
- WebSocket-based real-time communication
- OpenRouter API integration
- Event-driven architecture
- Automatic scaling on Render
- Health monitoring and error handling

## Deployment Steps

### 1. Fork/Clone Repository
```bash
git clone https://github.com/your-username/OpenHands-Backend.git
cd OpenHands-Backend
```

### 2. Create Render Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Use these settings:
   - **Name**: `openhands-novel-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m openhands.server.listen --host 0.0.0.0 --port $PORT`

### 3. Environment Variables

Set these environment variables in Render:

#### Required Variables
```bash
OPENROUTER_API_KEY=your_openrouter_api_key_here
LLM_API_KEY=your_openrouter_api_key_here
SESSION_API_KEY=your_session_api_key_here
```

#### Auto-configured Variables
The following are automatically set by `render.yaml`:
```bash
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307
OR_SITE_URL=https://docs.all-hands.dev/
OR_APP_NAME=OpenHands-NovelWriting
PORT=8000
HOST=0.0.0.0
CORS_ALLOWED_ORIGINS=*
```

### 4. Deploy

1. Click "Create Web Service"
2. Render will automatically deploy using `render.yaml` configuration
3. Wait for deployment to complete (~5-10 minutes)
4. Your backend will be available at `https://your-service-name.onrender.com`

## API Endpoints

### Health Check
```
GET /api/health
```

### WebSocket Connection
```
WSS /socket.io/
```

### Novel Writing Mode Usage

Send this JSON via WebSocket to activate Novel Writing Mode:

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

## Frontend Integration

### WebSocket Connection
```javascript
import io from 'socket.io-client';

const socket = io('https://your-backend.onrender.com', {
  query: {
    conversation_id: 'your-conversation-id',
    latest_event_id: -1
  }
});

// Send novel writing request
socket.emit('oh_user_action', {
  action: 'message',
  args: {
    content: 'Bantu saya mengembangkan karakter protagonis',
    novel_mode: true,
    original_prompt: 'Saya butuh bantuan karakter',
    template_used: 'character-development'
  }
});

// Listen for responses
socket.on('oh_event', (data) => {
  console.log('AI Response:', data);
});
```

### Available Templates
- `character-development`: Pengembangan karakter
- `plot-structure`: Struktur cerita dan plot
- `dialogue-writing`: Penulisan dialog
- `world-building`: Membangun dunia cerita
- `style-voice`: Gaya dan suara penulis
- `theme-symbolism`: Tema dan simbolisme
- `editing-revision`: Editing dan revisi

## Monitoring & Debugging

### Logs
View logs in Render Dashboard:
1. Go to your service
2. Click "Logs" tab
3. Monitor for errors or performance issues

### Health Check
```bash
curl https://your-backend.onrender.com/api/health
```

### Status Updates
The backend sends status updates for Novel Writing Mode:
```json
{
  "status_update": true,
  "type": "info",
  "id": "NOVEL_MODE_ACTIVATED",
  "message": "Novel Writing Mode diaktifkan dengan template: character-development"
}
```

## Cost Optimization

### Model Selection
- **Budget Mode**: Claude 3.5 Haiku (~$0.25/1M tokens)
- **Premium Mode**: Claude 3 Opus (~$15/1M tokens)

### Automatic Switching
The backend automatically chooses the appropriate model based on:
- Template complexity
- Content length
- User requirements

### Cost Control
- Set `MAX_CONCURRENT_CONVERSATIONS=5` to limit usage
- Monitor OpenRouter usage dashboard
- Use budget mode for development/testing

## Troubleshooting

### Common Issues

#### 1. Deployment Fails
- Check `requirements.txt` is present
- Verify Python version compatibility
- Check build logs for missing dependencies

#### 2. WebSocket Connection Fails
- Verify CORS settings
- Check if frontend is using correct URL
- Ensure WebSocket protocol (wss://) for HTTPS

#### 3. Novel Mode Not Working
- Verify `OPENROUTER_API_KEY` is set
- Check logs for error messages
- Test with regular mode first

#### 4. High Latency
- Check OpenRouter API status
- Monitor Render service metrics
- Consider upgrading Render plan

### Debug Commands
```bash
# Test novel mode locally
python test_novel_mode.py

# Start server with debug info
python start_novel_server.py

# Check environment variables
python -c "import os; print(os.environ.get('OPENROUTER_API_KEY', 'NOT SET'))"
```

## Performance Optimization

### Render Configuration
- **Plan**: Start with "Starter" plan
- **Auto-scaling**: Enabled by default
- **Health checks**: Configured for `/api/health`

### Backend Optimization
- Async WebSocket handling
- Efficient event streaming
- Optimized LLM parameters
- Intelligent model selection

## Security

### API Keys
- Store API keys as environment variables
- Never commit keys to repository
- Use Render's secret management

### CORS
- Currently set to `*` for development
- For production, specify exact frontend domains:
```bash
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-domain.com
```

### Session Management
- Use `SESSION_API_KEY` for additional security
- Implement rate limiting if needed

## Support

### Documentation
- [Novel Writing Mode Guide](./NOVEL_WRITING_MODE.md)
- [OpenHands Documentation](https://docs.all-hands.dev/)
- [OpenRouter API Docs](https://openrouter.ai/docs)

### Issues
1. Check Render logs first
2. Test with `test_novel_mode.py`
3. Verify environment variables
4. Check OpenRouter API status

### Contact
- GitHub Issues for bugs
- Render Support for deployment issues
- OpenRouter Support for API issues

## Next Steps

After successful deployment:

1. **Test the API** with your frontend
2. **Monitor usage** in OpenRouter dashboard
3. **Optimize costs** based on usage patterns
4. **Scale up** Render plan if needed
5. **Add custom domains** for production

## Example Frontend Integration

See the complete integration example in your frontend repository. The backend is designed to work seamlessly with the Novel Writing Mode frontend you've already built.

---

**Happy Writing! 📝✨**