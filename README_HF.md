# OpenHands Backend for Hugging Face Spaces

This is the backend API for OpenHands, optimized for deployment on Hugging Face Spaces.

## Features

- ✅ Public API endpoints (no authentication required)
- ✅ Local runtime (no Docker dependency)
- ✅ CORS enabled for frontend integration
- ✅ Anonymous conversation support

## Environment Variables

Set these in your Hugging Face Space settings:

```bash
# Required
LLM_API_KEY=your_openrouter_api_key
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307
LLM_BASE_URL=https://openrouter.ai/api/v1

# Optional
SESSION_API_KEY=your_session_key
OPENHANDS_RUNTIME=local
DEBUG=false

# File Storage (automatically configured)
FILE_STORE_PATH=/tmp/openhands
CACHE_DIR=/tmp/cache
```

## API Endpoints

- `GET /api/options/config` - Get configuration
- `POST /api/conversations` - Create new conversation
- `OPTIONS /api/conversations` - CORS preflight

## Frontend Integration

This backend is designed to work with frontends deployed on platforms like Vercel, Netlify, etc.

Make sure to configure CORS_ALLOWED_ORIGINS to include your frontend domain.