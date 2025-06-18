# 🚀 GitHub Actions Auto-Deploy Setup

## 📋 Overview

File GitHub Actions workflow sudah siap untuk auto-deploy ke HuggingFace Spaces setiap kali ada push ke repository utama.

## 🔧 Setup Required

### 1. **GitHub Secrets Configuration**

Di repository GitHub utama (`https://github.com/Minatoz997/OpenHands-Backend`), tambahkan secrets berikut:

**Go to: Settings → Secrets and variables → Actions → New repository secret**

```bash
# Required Secret
HF_TOKEN=your_huggingface_token_here

# Optional Secrets (sudah ada default)
HF_USERNAME=Minatoz997
HF_SPACE_NAME=Backend66
```

### 2. **HuggingFace Token Setup**

1. **Login ke HuggingFace**: https://huggingface.co/
2. **Go to Settings**: https://huggingface.co/settings/tokens
3. **Create New Token**:
   - Name: `GitHub-Actions-Deploy`
   - Type: `Write`
   - Scope: `Spaces`
4. **Copy token** dan paste ke GitHub Secrets sebagai `HF_TOKEN`

## 🎯 Workflow Features

### ✅ **Auto-Deploy Triggers**
- **Push to main/master**: Otomatis deploy
- **PR merged**: Deploy setelah PR di-merge
- **Manual trigger**: Bisa trigger manual dari GitHub Actions tab

### ✅ **Pre-Deploy Testing**
- Test novel writing imports
- Test novel writing functionality
- Verify all core features working

### ✅ **Deployment Process**
- Upload semua files ke HF Spaces
- Restart space untuk apply changes
- Test all endpoints (8 endpoints)
- Generate deployment summary

### ✅ **Post-Deploy Verification**
```bash
# Endpoints yang di-test:
- / (API info)
- /health (main health)
- /novel/ (novel service info)
- /novel/health (novel health)
- /novel/templates (writing templates)
- /chat/health (chat health)
- /openrouter/health (openrouter health)
- /memory-chat/health (memory chat health)
```

## 🚀 How to Use

### **Option 1: Automatic Deploy**
1. Push code ke branch `main` atau `master`
2. GitHub Actions akan otomatis trigger
3. Wait 2-3 minutes untuk deployment selesai
4. Check deployment summary di Actions tab

### **Option 2: Manual Deploy**
1. Go to GitHub repository
2. Click **Actions** tab
3. Click **Deploy to HuggingFace Spaces** workflow
4. Click **Run workflow** button
5. Select branch dan click **Run workflow**

### **Option 3: PR Merge Deploy**
1. Create PR ke main branch
2. Merge PR
3. Auto-deploy akan trigger setelah merge

## 📊 Deployment URLs

Setelah deploy berhasil, aplikasi akan tersedia di:

```bash
# Main URLs
🌐 Main API: https://minatoz997-backend66.hf.space
📚 API Docs: https://minatoz997-backend66.hf.space/docs
🎭 Novel Writing: https://minatoz997-backend66.hf.space/novel/
🤖 Chat API: https://minatoz997-backend66.hf.space/chat/

# Health Checks
❤️ Main Health: https://minatoz997-backend66.hf.space/health
🎭 Novel Health: https://minatoz997-backend66.hf.space/novel/health
🤖 Chat Health: https://minatoz997-backend66.hf.space/chat/health
```

## 🎭 Novel Writing Features Deployed

### **7 Writing Templates**:
1. `character-development` - Pengembangan karakter
2. `plot-structure` - Struktur cerita  
3. `dialogue-writing` - Penulisan dialog
4. `world-building` - Membangun dunia cerita
5. `style-voice` - Gaya dan suara penulisan
6. `theme-symbolism` - Tema dan simbolisme
7. `editing-revision` - Editing dan revisi

### **API Endpoints**:
```bash
POST /novel/write              # Main novel writing
GET /novel/templates           # List templates
GET /novel/questions/{template} # Template questions
GET /novel/sessions            # Session management
GET /novel/health              # Health check
```

## 🔍 Monitoring Deployment

### **Check Deployment Status**:
1. **GitHub Actions**: Repository → Actions tab
2. **HF Spaces**: https://huggingface.co/spaces/Minatoz997/Backend66
3. **Live Health**: https://minatoz997-backend66.hf.space/health

### **Deployment Logs**:
- GitHub Actions logs show detailed deployment process
- HF Spaces logs show runtime information
- Health endpoints show service status

## ⚠️ Troubleshooting

### **Common Issues**:

1. **HF_TOKEN Invalid**:
   - Regenerate token di HuggingFace
   - Update GitHub secret
   - Re-run workflow

2. **Space Not Starting**:
   - Check HF Spaces logs
   - Verify Dockerfile_HF syntax
   - Check requirements.txt

3. **Endpoints Not Working**:
   - Wait 2-3 minutes after deployment
   - Check /health endpoint first
   - Verify environment variables

### **Debug Steps**:
```bash
# 1. Check main health
curl https://minatoz997-backend66.hf.space/health

# 2. Check novel writing
curl https://minatoz997-backend66.hf.space/novel/health

# 3. Test novel endpoint
curl -X POST https://minatoz997-backend66.hf.space/novel/write \
  -H "Content-Type: application/json" \
  -d '{"message": "Test novel writing", "template": "character-development"}'
```

## 🎉 Success Indicators

### **Deployment Successful When**:
- ✅ GitHub Actions workflow completes without errors
- ✅ All 8 endpoints return 200 status
- ✅ HF Space shows "Running" status
- ✅ Health checks pass
- ✅ Novel writing endpoints respond correctly

### **Ready for Use When**:
- ✅ API docs accessible at `/docs`
- ✅ Novel templates available at `/novel/templates`
- ✅ Chat endpoints working at `/chat/health`
- ✅ OpenRouter integration ready at `/openrouter/health`

## 🔑 Environment Variables

**Set these in HuggingFace Space settings** (optional):

```bash
# For real AI responses
LLM_API_KEY=your_openrouter_api_key

# Model configuration
LLM_MODEL=openai/gpt-4o-mini
LLM_TEMPERATURE=0.7

# Novel writing specific
NOVEL_PREMIUM_CONTENT_THRESHOLD=1500
NOVEL_FORCE_PREMIUM_MODE=false
```

---

## 🎯 Quick Setup Checklist

- [ ] Add `HF_TOKEN` to GitHub Secrets
- [ ] Verify workflow file exists: `.github/workflows/deploy-hf-spaces.yml`
- [ ] Push to main branch or trigger manual deploy
- [ ] Wait 2-3 minutes for deployment
- [ ] Test endpoints: `/health`, `/novel/health`, `/chat/health`
- [ ] Add OpenRouter API key to HF Space settings (optional)
- [ ] Test novel writing: `/novel/write`

**🎉 Done! Your backend with novel writing features is now auto-deploying to HuggingFace Spaces!**