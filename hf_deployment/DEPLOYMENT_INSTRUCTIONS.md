# 🚀 HF Spaces Deployment Instructions

## Files Ready for Upload:

1. **Dockerfile** - Container configuration
2. **requirements.txt** - Python dependencies (fixed)
3. **app.py** - Application entry point (fixed)
4. **README.md** - Space documentation with metadata
5. **openhands/** - Main application code
6. **.gitignore** - Git ignore rules

## Deployment Steps:

### 1. Create HF Space
- Go to https://huggingface.co/new-space
- Choose Docker SDK
- Set visibility to Public (required for free tier)

### 2. Upload Files
Upload all files in this directory to your HF Space

### 3. Set Environment Variables
In Space Settings → Environment Variables:
```
LLM_API_KEY=your_openrouter_api_key
```

### 4. Deploy!
HF will automatically build and deploy your space.

## Expected Result:
Your API will be available at: https://your-username-space-name.hf.space

## Test Endpoints:
- Health: GET /health
- Config: GET /api/options/config  
- Chat: POST /api/conversations

## Troubleshooting:
- Check build logs for any errors
- Verify environment variables are set
- Make sure all files uploaded correctly

Good luck! 🍀
