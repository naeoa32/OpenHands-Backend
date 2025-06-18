#!/usr/bin/env python3
"""
Script to prepare files for HF Spaces deployment
Creates a clean deployment package with all fixes applied
"""
import os
import shutil
import tempfile
from pathlib import Path

def prepare_deployment():
    """Prepare deployment files for HF Spaces"""
    
    print("📦 Preparing HF Spaces Deployment Package")
    print("=" * 50)
    
    # Create deployment directory
    deploy_dir = Path("/workspace/OpenHands-Backend/hf_deployment")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    print(f"📁 Created deployment directory: {deploy_dir}")
    
    # 1. Copy and rename Dockerfile
    print("\n1️⃣ Preparing Dockerfile...")
    shutil.copy2("Dockerfile_HF_Final", deploy_dir / "Dockerfile")
    print("✅ Dockerfile_HF_Final → Dockerfile")
    
    # 2. Copy and rename requirements
    print("\n2️⃣ Preparing requirements.txt...")
    shutil.copy2("requirements_hf_fixed.txt", deploy_dir / "requirements.txt")
    print("✅ requirements_hf_fixed.txt → requirements.txt")
    
    # 3. Copy app file
    print("\n3️⃣ Preparing app.py...")
    shutil.copy2("app_hf_final.py", deploy_dir / "app.py")
    print("✅ app_hf_final.py → app.py")
    
    # 4. Copy README with HF metadata
    print("\n4️⃣ Preparing README.md...")
    readme_content = """---
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
# Health check
GET /health

# Get configuration
GET /api/options/config

# Create conversation
POST /api/conversations
Content-Type: application/json
{
  "initial_user_msg": "Hello! Can you help me with coding?"
}
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

# Optional (already set as defaults)
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307
LLM_BASE_URL=https://openrouter.ai/api/v1
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
"""
    
    with open(deploy_dir / "README.md", "w") as f:
        f.write(readme_content)
    print("✅ README.md created with HF metadata")
    
    # 5. Copy openhands folder
    print("\n5️⃣ Copying openhands folder...")
    shutil.copytree("openhands", deploy_dir / "openhands")
    print("✅ openhands/ folder copied")
    
    # 6. Create .gitignore
    print("\n6️⃣ Creating .gitignore...")
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
.tmp/

# Cache
.cache/
"""
    
    with open(deploy_dir / ".gitignore", "w") as f:
        f.write(gitignore_content)
    print("✅ .gitignore created")
    
    # 7. Create deployment instructions
    print("\n7️⃣ Creating deployment instructions...")
    instructions = """# 🚀 HF Spaces Deployment Instructions

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
"""
    
    with open(deploy_dir / "DEPLOYMENT_INSTRUCTIONS.md", "w") as f:
        f.write(instructions)
    print("✅ DEPLOYMENT_INSTRUCTIONS.md created")
    
    # 8. Show summary
    print("\n" + "=" * 50)
    print("🎉 DEPLOYMENT PACKAGE READY!")
    print("=" * 50)
    print(f"📁 Location: {deploy_dir}")
    print("\n📋 Files prepared:")
    for file in deploy_dir.rglob("*"):
        if file.is_file():
            rel_path = file.relative_to(deploy_dir)
            print(f"   ✅ {rel_path}")
    
    print(f"\n📊 Total files: {len(list(deploy_dir.rglob('*')))}")
    print(f"📦 Package size: {sum(f.stat().st_size for f in deploy_dir.rglob('*') if f.is_file()) / 1024 / 1024:.1f} MB")
    
    print("\n🚀 Next Steps:")
    print("1. Upload all files from hf_deployment/ to your HF Space")
    print("2. Set LLM_API_KEY environment variable")
    print("3. Deploy and test!")
    
    return deploy_dir

if __name__ == "__main__":
    deploy_dir = prepare_deployment()
    print(f"\n✅ Deployment package ready at: {deploy_dir}")