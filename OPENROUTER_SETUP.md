# 🎯 Personal OpenHands Backend - OpenRouter Setup

## 💕 Perfect untuk Anda dan Pacar!

Setup super simple dengan **HANYA OpenRouter API key** - tidak perlu yang lain!

---

## 🚀 Quick Setup di HF Spaces

### 1. Upload Files ke Backend66:
```
✅ requirements_personal.txt → ganti nama jadi requirements.txt
✅ app_personal.py → ganti nama jadi app.py
```

### 2. Set Environment Variables di HF Spaces:
```bash
LLM_API_KEY=your_openrouter_api_key_here
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307
```

### 3. Done! 🎉

---

## 🔑 OpenRouter API Key Setup

### Cara Dapat API Key:
1. **Daftar di:** https://openrouter.ai/
2. **Go to:** Account → API Keys
3. **Create new key**
4. **Copy key** (format: `sk-or-...`)

### Model Recommendations:
```bash
# Budget-friendly (untuk daily use):
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307

# Premium (untuk complex tasks):
LLM_MODEL=openrouter/anthropic/claude-3-5-sonnet-20241022

# GPT Alternative:
LLM_MODEL=openrouter/openai/gpt-4o-mini
```

---

## 📦 Dependencies Comparison

### ❌ Fallback Version (Heavy):
```
50+ packages including:
- openai==1.57.0
- anthropic==0.40.0  
- google-cloud-storage
- docker
- redis
- e2b
Total: ~500MB
```

### ✅ Personal Version (Light):
```
15+ packages including:
- litellm==1.52.14 (handles OpenRouter)
- fastapi==0.115.4
- uvicorn==0.32.0
- httpx==0.27.2
Total: ~200MB
```

**Hemat 300MB!** 🎯

---

## 🎮 Features Available

### 🤖 AI Agents (Full Power):
- **CodeActAgent** - Complete coding assistant
- **BrowsingAgent** - Web research & data extraction
- **ReadOnlyAgent** - Safe code review
- **LocAgent** - Targeted code generation

### 📝 Novel Writing (Indonesian):
- **7 Creative Templates**
- **Character development**
- **Plot structure** 
- **Dialogue writing**
- **World building**

### 📁 File Operations:
- **view** - Display files with line numbers
- **create** - Create new files
- **str_replace** - Replace text content
- **insert** - Insert text at specific lines

---

## 🌐 API Endpoints

### Test Your Backend:
```bash
# Health check
curl https://minatoz997-backend66.hf.space/health

# Personal info
curl https://minatoz997-backend66.hf.space/personal-info

# Create AI conversation
curl -X POST https://minatoz997-backend66.hf.space/api/conversations \
  -H "Content-Type: application/json" \
  -d '{"initial_user_msg": "Help me code a Python function", "agent": "CodeActAgent"}'

# Novel writing (Indonesian)
curl -X POST https://minatoz997-backend66.hf.space/novel/write \
  -H "Content-Type: application/json" \
  -d '{"message": "Bantu saya buat cerita romantis", "template": "character-development"}'
```

---

## 💰 Cost Estimation

### OpenRouter Pricing (approximate):
- **Claude Haiku:** $0.25 per 1M tokens
- **Claude Sonnet:** $3 per 1M tokens  
- **GPT-4o Mini:** $0.15 per 1M tokens

### Typical Usage:
- **Daily coding help:** ~$0.10-0.50/day
- **Novel writing:** ~$0.20-1.00/session
- **General chat:** ~$0.05-0.20/day

**Perfect untuk personal budget!** 💕

---

## 🔧 Troubleshooting

### Common Issues:

**1. "LLM_API_KEY not set"**
```bash
Solution: Add your OpenRouter API key to HF Spaces environment variables
```

**2. "Model not found"**
```bash
Solution: Check available models at https://openrouter.ai/models
Update LLM_MODEL environment variable
```

**3. "Rate limit exceeded"**
```bash
Solution: Add credits to your OpenRouter account
Or switch to cheaper model (claude-haiku)
```

---

## 🎯 Why This Setup is Perfect

### ✅ Advantages:
- **One API key** untuk semua models
- **No vendor lock-in** (bisa ganti model kapan saja)
- **Transparent pricing** (pay per use)
- **All latest models** available
- **Super lightweight** backend

### 💕 Perfect for Couples:
- **Shared API key** (easy billing)
- **Budget control** (set limits di OpenRouter)
- **Simple setup** (no technical complexity)
- **All features** available

---

## 🚀 Ready to Deploy!

**Your personal AI assistant is ready!** 

**Just upload the files and set your OpenRouter API key!** 🎉