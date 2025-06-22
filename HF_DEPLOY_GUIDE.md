# 🚀 Deploy Guide: Backend dengan Playwright ke Hugging Face Spaces

## 📋 **Files yang Perlu Diupload ke HF Spaces:**

### **1. Dockerfile** (Rename jadi `Dockerfile`)
```dockerfile
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/tmp/playwright_browsers

# Install system dependencies yang diperlukan Playwright
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxss1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium
COPY . .
EXPOSE 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```

### **2. requirements.txt**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
requests==2.31.0
playwright==1.40.0
```

### **3. app.py** 
(Yang sudah diupdate dari repository kamu)

### **4. fizzo_automation.py**
(File untuk scraping Fizzo.org)

## 🔧 **Langkah Deploy:**

### **Step 1: Upload Files**
1. Buka https://huggingface.co/spaces/minatoz997/backend66
2. Klik "Files and versions"
3. Upload 4 files di atas

### **Step 2: Set Space Type**
1. Klik "Settings" 
2. Ubah "Space hardware" ke **Docker**
3. Save settings

### **Step 3: Restart**
1. Space akan auto-rebuild dengan Docker
2. Tunggu 5-10 menit untuk build selesai
3. Playwright akan terinstall otomatis

## ✅ **Test Setelah Deploy:**

```bash
# Test endpoint
curl -X POST https://minatoz997-backend66.hf.space/api/fizzo-list-novel \
  -H "Content-Type: application/json" \
  -d '{"email": "minatoz1997@gmail.com", "password": "Luthfi123*"}'
```

**Expected Response:**
```json
{
  "novels": [
    {
      "id": "real-novel-id-123",
      "title": "Novel Asli dari Fizzo.org",
      "description": "...",
      "status": "ongoing"
    }
  ]
}
```

## 🎯 **Hasil Akhir:**

- ✅ Playwright terinstall dengan system dependencies
- ✅ Backend bisa scrape novel real dari Fizzo.org  
- ✅ Frontend bisa pilih novel asli untuk upload
- ✅ No more dummy data!

**Docker approach ini paling reliable untuk HF Spaces!** 🐳