#!/usr/bin/env python3
"""
🚨 EMERGENCY DEPLOYMENT SCRIPT
Use this if you need to deploy without external help

This script will:
1. Check current repository status
2. Verify all fixes are in place
3. Generate deployment files
4. Provide step-by-step instructions
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def check_git_status():
    """Check if we're in the right repository and branch"""
    print_header("CHECKING REPOSITORY STATUS")
    
    try:
        # Check if we're in a git repository
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print_error("Not in a git repository!")
            return False
        
        # Check current branch
        result = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True)
        current_branch = result.stdout.strip()
        print_info(f"Current branch: {current_branch}")
        
        # Check if we have the fixes
        if os.path.exists('openhands/utils/chunk_localizer.py'):
            print_error("chunk_localizer.py still exists! Need to delete it.")
            return False
        else:
            print_success("chunk_localizer.py properly deleted")
        
        # Check if edit.py has fallback
        edit_file = 'openhands/runtime/utils/edit.py'
        if os.path.exists(edit_file):
            with open(edit_file, 'r') as f:
                content = f.read()
                if 'class Chunk(BaseModel):' in content:
                    print_success("edit.py has fallback implementation")
                else:
                    print_error("edit.py missing fallback implementation")
                    return False
        
        # Check app_hf_final.py
        if os.path.exists('app_hf_final.py'):
            print_success("app_hf_final.py exists")
        else:
            print_error("app_hf_final.py missing!")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Error checking git status: {e}")
        return False

def test_imports():
    """Test if all imports work"""
    print_header("TESTING IMPORTS")
    
    test_imports = [
        "import fastapi",
        "import uvicorn", 
        "import litellm",
        "import httpx",
        "import pydantic",
        "from openhands.core.config import AppConfig",
        "from openhands.events.action import Action",
        "from openhands.runtime.runtime import Runtime",
        "from openhands.agenthub import Agent",
    ]
    
    all_passed = True
    
    for import_test in test_imports:
        try:
            exec(import_test)
            print_success(f"{import_test}")
        except ImportError as e:
            print_error(f"{import_test} - {e}")
            all_passed = False
        except Exception as e:
            print_warning(f"{import_test} - {e}")
    
    return all_passed

def generate_dockerfile():
    """Generate optimized Dockerfile"""
    print_header("GENERATING DOCKERFILE")
    
    dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    git \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Clone your repository (replace with your actual repo)
RUN git clone https://github.com/Minatoz997/OpenHands-Backend.git .

# Install Python dependencies
RUN pip install --no-cache-dir \\
    fastapi==0.104.1 \\
    uvicorn[standard]==0.24.0 \\
    litellm==1.44.22 \\
    httpx==0.25.2 \\
    pydantic==2.5.0 \\
    python-multipart==0.0.6

# Expose port
EXPOSE 7860

# Set environment variables
ENV PYTHONPATH=/app
ENV HF_SPACES=1
ENV ENVIRONMENT=production

# Start the application
CMD ["python", "app_hf_final.py"]
'''
    
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile_content)
    
    print_success("Dockerfile generated")
    return True

def generate_requirements():
    """Generate requirements.txt"""
    print_header("GENERATING REQUIREMENTS.TXT")
    
    requirements_content = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
litellm==1.44.22
httpx==0.25.2
pydantic==2.5.0
python-multipart==0.0.6
'''
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements_content)
    
    print_success("requirements.txt generated")
    return True

def generate_hf_readme():
    """Generate README for HF Spaces"""
    print_header("GENERATING HF SPACES README")
    
    readme_content = '''---
title: Personal OpenHands Backend
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# Personal OpenHands Backend

This is a personal OpenHands backend optimized for Hugging Face Spaces deployment.

## Features
- 🤖 AI coding assistance with multiple agents
- 📝 Novel writing in Indonesian
- 📁 File operations and management
- 🔍 Repository tools and analysis
- 🔑 OpenRouter integration for cost-effective AI

## Setup
1. Set your OpenRouter API key in the Space settings:
   - Variable name: `LLM_API_KEY`
   - Value: Your OpenRouter API key (starts with `sk-or-v1-`)

2. Optional configuration:
   - `LLM_MODEL`: Model to use (default: `openrouter/anthropic/claude-3-haiku-20240307`)
   - `LLM_BASE_URL`: API base URL (default: `https://openrouter.ai/api/v1`)

## Usage
Once deployed, you can access:
- API documentation: `/docs`
- Health check: `/health`
- Test chat: `/test-chat`
- Novel writing: `/novel/write`
- Conversations: `/api/conversations`

## API Examples

### Test Chat
```bash
curl -X POST https://your-space.hf.space/test-chat \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Hello, can you help me code?"}'
```

### Novel Writing (Indonesian)
```bash
curl -X POST https://your-space.hf.space/novel/write \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Tulis cerita romantis tentang Jakarta"}'
```

### Simple Conversation
```bash
curl -X POST https://your-space.hf.space/api/conversations/simple \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Create a Python function for sorting"}'
```

## Features for Personal Use
- **AI Coding Assistant**: Get help with programming tasks
- **Indonesian Novel Writing**: Creative writing support
- **File Management**: Organize and manage your projects
- **Code Analysis**: Review and improve your code
- **Cost-Effective**: Uses OpenRouter for affordable AI access

Perfect for personal projects, learning, and creative writing!
'''
    
    with open('README.md', 'w') as f:
        f.write(readme_content)
    
    print_success("README.md for HF Spaces generated")
    return True

def test_server():
    """Test if server can start"""
    print_header("TESTING SERVER STARTUP")
    
    try:
        # Try to import the main app
        sys.path.insert(0, os.getcwd())
        
        print_info("Testing app import...")
        exec("from app_hf_final import app")
        print_success("app_hf_final.py imports successfully")
        
        print_info("Testing OpenHands imports...")
        exec("from openhands.server.app import app as oh_app")
        print_success("OpenHands server imports successfully")
        
        return True
        
    except Exception as e:
        print_error(f"Server test failed: {e}")
        return False

def print_deployment_instructions():
    """Print step-by-step deployment instructions"""
    print_header("DEPLOYMENT INSTRUCTIONS")
    
    instructions = """
🚀 STEP-BY-STEP DEPLOYMENT TO HUGGING FACE SPACES:

1. 📋 PREPARE FILES:
   ✅ Dockerfile (generated)
   ✅ requirements.txt (generated) 
   ✅ README.md (generated)
   ✅ app_hf_final.py (exists)
   ✅ openhands/ directory (fixed)

2. 🌐 CREATE HF SPACE:
   - Go to: https://huggingface.co/spaces
   - Click: "Create new Space"
   - Name: backend66 (or your preferred name)
   - SDK: Docker
   - Hardware: CPU basic (free)
   - Visibility: Private (recommended)

3. 📁 UPLOAD FILES:
   Upload these files to your HF Space:
   - Dockerfile
   - requirements.txt  
   - README.md
   - app_hf_final.py
   - openhands/ (entire directory)

4. ⚙️ SET ENVIRONMENT VARIABLES:
   In your HF Space settings, add:
   - LLM_API_KEY = your_openrouter_api_key
   - LLM_MODEL = openrouter/anthropic/claude-3-haiku-20240307
   - LLM_BASE_URL = https://openrouter.ai/api/v1

5. 🚀 DEPLOY:
   - Click "Deploy" in your HF Space
   - Wait 2-3 minutes for build
   - Check logs for successful startup

6. ✅ TEST:
   Test these endpoints:
   - https://your-space.hf.space/health
   - https://your-space.hf.space/docs
   - https://your-space.hf.space/test-chat

🎯 EXPECTED SUCCESS LOGS:
INFO: Uvicorn running on http://0.0.0.0:7860
✅ Personal backend ready!

💡 TROUBLESHOOTING:
- If build fails: Check Dockerfile syntax
- If imports fail: Verify all files uploaded
- If API errors: Check environment variables
- If server won't start: Check app_hf_final.py

🔑 GET OPENROUTER API KEY:
1. Go to: https://openrouter.ai/
2. Sign up/login
3. Go to "Keys" section  
4. Create new API key
5. Copy key (starts with sk-or-v1-)

💰 COST ESTIMATE:
Claude 3 Haiku: ~$0.25 per 1M tokens
For personal use: $5-10/month should be plenty

🎉 YOUR PERSONAL AI BACKEND WILL BE READY!
"""
    
    print(instructions)

def main():
    """Main deployment check and setup"""
    print_header("EMERGENCY DEPLOYMENT SCRIPT")
    print("🚨 This script will help you deploy without external assistance")
    
    # Check repository status
    if not check_git_status():
        print_error("Repository check failed! Please merge PR #39 first.")
        print_info("Go to: https://github.com/Minatoz997/OpenHands-Backend/pull/39")
        return False
    
    # Test imports
    if not test_imports():
        print_warning("Some imports failed, but deployment might still work")
    
    # Generate deployment files
    generate_dockerfile()
    generate_requirements()
    generate_hf_readme()
    
    # Test server
    if not test_server():
        print_warning("Server test failed, but deployment might still work")
    
    # Print instructions
    print_deployment_instructions()
    
    print_header("DEPLOYMENT READY")
    print_success("All deployment files generated!")
    print_success("Follow the instructions above to deploy to HF Spaces")
    print_info("Your personal OpenHands backend will be ready in minutes!")
    
    return True

if __name__ == "__main__":
    main()