# 🚀 Setup Auto-Deploy ke HuggingFace Spaces

## 📋 **Langkah Setup (Sekali Saja):**

### 1. **Setup GitHub Secrets:**
Masuk ke repo utama: https://github.com/Minatoz997/OpenHands-Backend

1. Klik **Settings** → **Secrets and variables** → **Actions**
2. Klik **New repository secret**
3. Tambahkan secret:
   - **Name:** `HF_TOKEN`
   - **Value:** Token HuggingFace kamu

### 2. **Cara Dapat HF Token:**
1. Masuk ke https://huggingface.co/settings/tokens
2. Klik **New token**
3. Pilih **Write** access
4. Copy token yang dibuat

### 3. **Merge PR #22:**
1. Masuk ke https://github.com/Minatoz997/OpenHands-Backend/pull/22
2. Klik **Merge pull request**
3. Confirm merge

## 🎯 **Cara Deploy (Otomatis):**

### **Opsi 1: Auto Deploy saat Merge**
- Setiap kali merge PR ke `main` → otomatis deploy ke HF Spaces

### **Opsi 2: Manual Deploy**
1. Masuk ke repo: https://github.com/Minatoz997/OpenHands-Backend
2. Klik tab **Actions**
3. Pilih **Deploy to HuggingFace Spaces**
4. Klik **Run workflow** → **Run workflow**

## 📱 **Solusi untuk HP:**

### **Cara Restart Space dari HP:**
1. Buka: https://huggingface.co/spaces/Minatoz997/Backend66
2. Scroll ke bawah sampai ketemu tombol **Restart**
3. Atau gunakan mode desktop di browser HP

### **Alternatif - Restart via URL:**
Buka link ini di browser:
```
https://huggingface.co/spaces/Minatoz997/Backend66/restart
```

## 🔧 **File yang Dibutuhkan di HF Spaces:**

File `app.py` sudah ada dan siap:
```python
# File: app.py (sudah ada di repo)
import os
os.environ.setdefault('OPENHANDS_DEFAULT_AGENT', 'CodeActAgent')
os.environ.setdefault('RUNTIME', 'eventstream')

from app_hf import app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
```

## ✅ **Setelah Deploy Berhasil:**

Backend akan tersedia di:
- **Main URL:** https://Minatoz997-Backend66.hf.space
- **Health Check:** https://Minatoz997-Backend66.hf.space/health
- **Novel Writing:** https://Minatoz997-Backend66.hf.space/novel/health
- **API Docs:** https://Minatoz997-Backend66.hf.space/docs

## 🎭 **Fitur yang Akan Working:**

✅ **22+ Endpoints** termasuk:
- `/chat/message` - Real AI chat dengan OpenRouter
- `/novel/write` - Indonesian creative writing assistant
- `/memory-chat/message` - Memory-based chat fallback
- `/health` - Health monitoring
- `/docs` - Interactive API documentation

## 🔑 **Environment Variables di HF Spaces:**

Setelah deploy, set di HF Spaces Settings:
```bash
LLM_API_KEY=your-openrouter-api-key
LLM_MODEL=openai/gpt-4o-mini
RUNTIME=eventstream
```

## 🎉 **Ready to Use!**

Setelah setup ini, setiap update code akan otomatis deploy ke HF Spaces! 🚀