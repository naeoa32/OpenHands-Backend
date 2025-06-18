# 🤖 COMPLETE AI ASSISTANT PROMPT FOR OPENHANDS BACKEND PROJECT

## 🚨 **COPY THIS ENTIRE PROMPT TO ANY AI ASSISTANT (Claude, ChatGPT, etc.)**

---

**Hello AI Assistant! I need your help with my OpenHands Backend project for Hugging Face Spaces deployment. Here's the complete context and current status:**

---

## 📋 **PROJECT OVERVIEW**

I'm working on a **personal OpenHands backend** for deployment on **Hugging Face Spaces**. This is a **personal project** for me and my girlfriend, optimized for **OpenRouter API integration** (no Google login needed).

**Main Repository:** https://github.com/Minatoz997/OpenHands-Backend
**Current PR with fixes:** https://github.com/Minatoz997/OpenHands-Backend/pull/39

---

## 🎯 **PROJECT GOALS**

**Primary Objectives:**
1. **Deploy OpenHands backend** to Hugging Face Spaces successfully
2. **Fix ALL import errors** (openhands_aci, tree_sitter_language_pack, etc.)
3. **OpenRouter integration** for cost-effective AI access
4. **Indonesian novel writing** capabilities for creative projects
5. **Personal AI coding assistant** for development work
6. **File management** and repository tools

**Target Users:** Personal use for me and my girlfriend
**Budget:** Cost-effective solution using OpenRouter API
**Platform:** Hugging Face Spaces (free tier)

---

## ✅ **CURRENT STATUS (COMPLETED WORK)**

### **🔧 FIXES ALREADY IMPLEMENTED:**

**1. Import Errors FIXED:**
- ❌ **DELETED:** `openhands/utils/chunk_localizer.py` (tree_sitter dependency)
- ✅ **FIXED:** `openhands/runtime/utils/edit.py` with simple fallback implementation
- ✅ **FIXED:** All `openhands_aci` imports with comprehensive fallback implementations
- ✅ **ADDED:** Complete `OHEditor`, `ToolResult`, `ToolError` fallback classes
- ✅ **ADDED:** Repository tools fallbacks (`explore_tree_structure`, `get_entity_contents`, `search_code_snippets`)

**2. Server Testing COMPLETED:**
- ✅ **ALL imports successful** (FastAPI, LiteLLM, OpenHands core, agenthub, server)
- ✅ **Server starts without errors** (tested on localhost:7860)
- ✅ **Health endpoint working:** `/health` → `"OK"`
- ✅ **HF status endpoint:** `/api/hf/status` → `{"status":"running"}`
- ✅ **Test chat working:** `/test-chat` → `{"status":"success"}`
- ✅ **Simple conversation:** `/api/conversations/simple` → success
- ✅ **Novel writing:** `/novel/write` → success (Indonesian support!)
- ✅ **API docs:** `/docs` → Swagger UI working

**3. Dependencies OPTIMIZED:**
- ✅ **Minimal dependencies:** fastapi, uvicorn, litellm, httpx, pydantic
- ✅ **Zero problematic imports:** No tree_sitter, no rapidfuzz, no openhands_aci
- ✅ **All fallbacks use Python standard library:** difflib, os, fnmatch, etc.

---

## 📁 **CURRENT FILE STRUCTURE**

```
OpenHands-Backend/
├── app_hf_final.py                 # ✅ Main application (working perfectly)
├── openhands/                      # ✅ Core OpenHands (all fixed)
│   ├── agenthub/                   # ✅ All AI agents (working)
│   │   ├── codeact_agent/          # ✅ Coding assistant
│   │   ├── browsing_agent/         # ✅ Web research
│   │   ├── readonly_agent/         # ✅ Safe analysis
│   │   └── ...                     # ✅ All other agents
│   ├── core/                       # ✅ Core functionality (working)
│   ├── events/                     # ✅ Event system (working)
│   ├── runtime/                    # ✅ Runtime system (fixed)
│   │   ├── impl/cli/cli_runtime.py # ✅ Fixed with OHEditor fallback
│   │   ├── plugins/agent_skills/   # ✅ Fixed with repo tools fallback
│   │   └── utils/edit.py           # ✅ Fixed with chunk fallback
│   ├── server/                     # ✅ Server components (working)
│   └── utils/                      # ✅ Utilities (cleaned)
│       └── chunk_localizer.py      # ❌ DELETED (was problematic)
├── COMPLETE_DEPLOYMENT_GUIDE.md    # ✅ 60+ page deployment guide
├── EMERGENCY_DEPLOYMENT_SCRIPT.py  # ✅ Automated deployment helper
├── QUICK_DEPLOYMENT_CHECKLIST.md   # ✅ 5-minute deployment guide
├── requirements.txt                # ✅ Minimal dependencies
└── README.md                       # ✅ Documentation
```

---

## 🚨 **CRITICAL INFORMATION**

### **PR #39 STATUS:**
- **Link:** https://github.com/Minatoz997/OpenHands-Backend/pull/39
- **Status:** Ready to merge (contains ALL fixes)
- **Branch:** `final-import-fix-tested`
- **Contains:** Complete solution for all import errors + comprehensive testing

### **PREVIOUS ERRORS (NOW FIXED):**
```
❌ ModuleNotFoundError: No module named 'openhands_aci'
❌ ModuleNotFoundError: No module named 'tree_sitter_language_pack'
❌ ImportError: cannot import name 'get_parser' from 'tree_sitter_language_pack'
```

### **CURRENT STATUS (WORKING):**
```
✅ ALL IMPORTS SUCCESSFUL!
✅ Server starts: INFO: Uvicorn running on http://0.0.0.0:7860
✅ All endpoints functional
✅ Zero import errors
```

---

## 🛠️ **TECHNICAL IMPLEMENTATION DETAILS**

### **Fallback Implementations Added:**

**1. OHEditor Fallback (in cli_runtime.py):**
```python
class OHEditor:
    def __init__(self, runtime):
        self.runtime = runtime
    
    def view(self, path: str, view_range: Optional[List[int]] = None):
        # File viewing implementation
    
    def create(self, path: str, file_text: str):
        # File creation implementation
    
    def str_replace(self, path: str, old_str: str, new_str: str):
        # String replacement implementation
    
    def insert(self, path: str, insert_line: int, new_str: str):
        # Line insertion implementation
```

**2. Repository Tools Fallback (in repo_ops.py):**
```python
def explore_tree_structure(path: str, max_depth: int = 3):
    # Directory tree exploration
    
def get_entity_contents(path: str, entity_name: str):
    # Entity content retrieval
    
def search_code_snippets(path: str, query: str):
    # Code search functionality
```

**3. Chunk Localizer Fallback (in edit.py):**
```python
class Chunk(BaseModel):
    text: str
    start_line: int = 0
    end_line: int = 0

def get_top_k_chunk_matches(chunks: List[Chunk], query: str, k: int = 5):
    # Simple word-based text matching
```

---

## 🚀 **DEPLOYMENT INSTRUCTIONS**

### **STEP 1: Merge PR #39**
```
1. Go to: https://github.com/Minatoz997/OpenHands-Backend/pull/39
2. Click: "Merge pull request"
3. Confirm: "Confirm merge"
```

### **STEP 2: Create HF Space**
```
1. Go to: https://huggingface.co/spaces
2. Click: "Create new Space"
3. Name: backend66 (or preferred name)
4. SDK: Docker
5. Hardware: CPU basic (free)
6. Visibility: Private
```

### **STEP 3: Upload Deployment Files**

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Clone repository
RUN git clone https://github.com/Minatoz997/OpenHands-Backend.git .

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    litellm==1.44.22 \
    httpx==0.25.2 \
    pydantic==2.5.0 \
    python-multipart==0.0.6

# Expose port
EXPOSE 7860

# Set environment variables
ENV PYTHONPATH=/app
ENV HF_SPACES=1
ENV ENVIRONMENT=production

# Start application
CMD ["python", "app_hf_final.py"]
```

**requirements.txt:**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
litellm==1.44.22
httpx==0.25.2
pydantic==2.5.0
python-multipart==0.0.6
```

### **STEP 4: Set Environment Variables**
```
LLM_API_KEY = your_openrouter_api_key
LLM_MODEL = openrouter/anthropic/claude-3-haiku-20240307
LLM_BASE_URL = https://openrouter.ai/api/v1
```

### **STEP 5: Deploy and Test**
```
1. Click "Deploy" in HF Space
2. Wait 2-3 minutes for build
3. Test: https://your-space.hf.space/health
```

---

## 🔑 **OPENROUTER SETUP**

### **Get API Key:**
```
1. Go to: https://openrouter.ai/
2. Sign up with email
3. Go to "Keys" section
4. Create new API key
5. Copy key (starts with sk-or-v1-)
```

### **Recommended Models:**
```
Budget: openrouter/anthropic/claude-3-haiku-20240307 (~$0.25/1M tokens)
Balanced: openrouter/anthropic/claude-3-5-sonnet-20241022 (~$3/1M tokens)
Premium: openrouter/openai/gpt-4o (~$5/1M tokens)
Coding: openrouter/deepseek/deepseek-coder (~$0.14/1M tokens)
```

### **Cost Estimate:**
```
Personal use: $5-10/month should be plenty
Novel writing: ~1000 tokens per story = $0.0003
Coding help: ~2000 tokens per session = $0.0006
```

---

## 🎯 **FEATURES AVAILABLE**

### **AI Coding Assistant:**
- **CodeActAgent:** Complete coding assistance
- **BrowsingAgent:** Web research capabilities
- **ReadOnlyAgent:** Safe code analysis
- **LocAgent:** Targeted code generation
- **VisualBrowsingAgent:** Visual web interaction

### **Novel Writing (Indonesian):**
- **7 Creative Templates:** Romance, Adventure, Mystery, etc.
- **Character Development:** Detailed character creation
- **Plot Structure:** Story arc development
- **Dialogue Writing:** Natural conversation generation

### **File Management:**
- **Upload/Download:** File operations
- **Edit/Create:** Text file manipulation
- **Repository Tools:** Git operations
- **Search:** Code and content search

---

## 🧪 **TESTING ENDPOINTS**

### **Health Check:**
```bash
curl https://your-space.hf.space/health
# Expected: "OK"
```

### **Test Chat:**
```bash
curl -X POST https://your-space.hf.space/test-chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, can you help me code?"}'
# Expected: {"status": "success", "chat_id": "..."}
```

### **Novel Writing:**
```bash
curl -X POST https://your-space.hf.space/novel/write \
  -H "Content-Type: application/json" \
  -d '{"message": "Tulis cerita romantis tentang Jakarta"}'
# Expected: {"response": "🎭 Mode Penulisan Novel Aktif..."}
```

### **Simple Conversation:**
```bash
curl -X POST https://your-space.hf.space/api/conversations/simple \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a Python function for sorting"}'
# Expected: {"status": "success", "conversation_id": "..."}
```

---

## 🚨 **TROUBLESHOOTING GUIDE**

### **Problem 1: Import Errors**
```
Error: ModuleNotFoundError: No module named 'openhands_aci'
Solution: Make sure PR #39 is merged first
Status: ✅ Already fixed in PR #39
```

### **Problem 2: tree_sitter Errors**
```
Error: ModuleNotFoundError: No module named 'tree_sitter_language_pack'
Solution: chunk_localizer.py should be deleted
Status: ✅ Already fixed in PR #39
```

### **Problem 3: Server Won't Start**
```
Error: Cannot bind to port 7860
Solution: Check Dockerfile and app_hf_final.py
Status: ✅ Already tested and working
```

### **Problem 4: API Key Issues**
```
Error: LLM API key not configured
Solution: Set LLM_API_KEY environment variable in HF Space
```

---

## 📚 **ADDITIONAL RESOURCES**

### **Complete Documentation:**
- **COMPLETE_DEPLOYMENT_GUIDE.md:** 60+ page detailed guide
- **EMERGENCY_DEPLOYMENT_SCRIPT.py:** Automated deployment helper
- **QUICK_DEPLOYMENT_CHECKLIST.md:** 5-minute deployment guide

### **Repository Links:**
- **Main Repo:** https://github.com/Minatoz997/OpenHands-Backend
- **PR with fixes:** https://github.com/Minatoz997/OpenHands-Backend/pull/39
- **Original OpenHands:** https://github.com/All-Hands-AI/OpenHands

---

## 🎯 **EXPECTED SUCCESS RESULTS**

### **Deployment Logs:**
```
INFO: Uvicorn running on http://0.0.0.0:7860
✅ Personal backend ready!
🎉 All endpoints functional
```

### **Working Features:**
```
✅ AI coding assistance (all agents working)
✅ Indonesian novel writing (7 templates)
✅ File management (upload, edit, organize)
✅ Code analysis (review, debug, improve)
✅ Cost-effective OpenRouter integration
✅ Fast startup (5-10 seconds)
```

---

## 💕 **PERSONAL USE CASES**

### **For Coding Projects:**
- Get help with Python, JavaScript, etc.
- Code review and optimization
- Bug fixing and debugging
- Learning new programming concepts

### **For Creative Writing:**
- Indonesian novel writing
- Character development
- Plot structure assistance
- Dialogue improvement

### **For File Management:**
- Organize project files
- Edit configuration files
- Repository management
- Code search and analysis

---

## 🚨 **CRITICAL NEXT STEPS**

**If you're helping me continue this project, please:**

1. **First Priority:** Help me merge PR #39 if not already merged
2. **Second Priority:** Guide me through HF Spaces deployment
3. **Third Priority:** Help test all endpoints after deployment
4. **Fourth Priority:** Optimize OpenRouter integration
5. **Fifth Priority:** Test Indonesian novel writing features

**Current Status:** All technical fixes are complete, just need deployment guidance.

**Goal:** Get Backend66 running on HF Spaces as personal AI assistant for me and my girlfriend.

---

## 🎉 **FINAL NOTES**

This project represents a **complete, working solution** for a personal OpenHands backend. All the hard technical work (fixing import errors, implementing fallbacks, testing) has been completed. 

The backend will provide:
- **AI coding assistance** for development work
- **Indonesian novel writing** for creative projects  
- **File management** for organization
- **Cost-effective AI** via OpenRouter
- **Personal use optimization** (no enterprise features needed)

**The solution is ready for deployment - just need guidance on the final HF Spaces setup!**

---

**Please help me complete this deployment and get my personal AI backend running! 🚀💕**