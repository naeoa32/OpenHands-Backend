# 🚀 Fizzo.org Auto-Update Guide

Fitur automation untuk auto-update novel chapter ke fizzo.org menggunakan web automation.

## 🎯 Fitur

- ✅ **Auto Login** ke fizzo.org dengan email/password
- ✅ **Auto Navigate** ke form "New Chapter"
- ✅ **Auto Fill** chapter title dan content
- ✅ **Auto Publish** chapter ke platform
- ✅ **Error Handling** dan timeout management
- ✅ **Security** untuk credentials
- ✅ **Validation** content length (1,000-60,000 karakter)

## 📡 API Endpoint

```
POST /api/fizzo-auto-update
Content-Type: application/json
```

### Request Body

```json
{
  "email": "your_email@gmail.com",
  "password": "your_password",
  "chapter_title": "Bab 28: Judul Chapter",
  "chapter_content": "Isi chapter novel yang panjang minimal 1000 karakter..."
}
```

### Response Success

```json
{
  "success": true,
  "message": "Chapter berhasil diupload ke fizzo.org",
  "data": {
    "success": true,
    "message": "Chapter created successfully",
    "chapter_title": "Bab 28: Judul Chapter",
    "content_length": 2500,
    "published": true,
    "confirmed": true
  }
}
```

### Response Error

```json
{
  "success": false,
  "error": "Login failed"
}
```

## 🔧 Cara Penggunaan

### 1. Via cURL

```bash
curl -X POST "https://your-backend.hf.space/api/fizzo-auto-update" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your_email@gmail.com",
    "password": "your_password",
    "chapter_title": "Bab 28: Pertarungan Terakhir",
    "chapter_content": "Di tengah malam yang kelam, protagonis menghadapi musuh terbesarnya. Dengan tekad yang bulat, dia melangkah maju tanpa rasa takut. Pertarungan ini akan menentukan nasib seluruh kerajaan..."
  }'
```

### 2. Via JavaScript (Frontend)

```javascript
const updateNovel = async () => {
  const response = await fetch('/api/fizzo-auto-update', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: 'your_email@gmail.com',
      password: 'your_password',
      chapter_title: 'Bab 28: Pertarungan Terakhir',
      chapter_content: 'Isi chapter yang panjang...'
    })
  });
  
  const result = await response.json();
  
  if (result.success) {
    console.log('✅ Chapter berhasil diupload!');
    console.log(result.data);
  } else {
    console.error('❌ Upload gagal:', result.error);
  }
};
```

### 3. Via Python

```python
import requests

def upload_chapter(email, password, title, content):
    url = "https://your-backend.hf.space/api/fizzo-auto-update"
    
    payload = {
        "email": email,
        "password": password,
        "chapter_title": title,
        "chapter_content": content
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    if result.get("success"):
        print("✅ Chapter berhasil diupload!")
        return result["data"]
    else:
        print(f"❌ Upload gagal: {result.get('error')}")
        return None

# Contoh penggunaan
upload_chapter(
    email="your_email@gmail.com",
    password="your_password", 
    title="Bab 28: Pertarungan Terakhir",
    content="Isi chapter yang panjang minimal 1000 karakter..."
)
```

## ⚙️ Workflow Automation

Automation ini mengikuti workflow manual user:

1. **🌐 Buka fizzo.org**
2. **📱 Klik hamburger menu (☰)**
3. **✍️ Klik "Menulis Cerita"**
4. **📧 Klik "Lanjutkan dengan Email"**
5. **📝 Fill email field**
6. **🔒 Fill password field**
7. **🚀 Klik "Lanjut" button**
8. **⏳ Wait for dashboard**
9. **📝 Klik "New Chapter" button**
10. **📖 Fill chapter title**
11. **📄 Fill chapter content**
12. **✈️ Klik publish button**

## 🛡️ Security & Validation

### Input Validation
- ✅ Email dan password required
- ✅ Chapter title dan content required
- ✅ Content minimal 1,000 karakter
- ✅ Content maksimal 60,000 karakter

### Security Features
- ✅ Headless browser (tidak tampil UI)
- ✅ Auto-close browser setelah selesai
- ✅ Error handling untuk timeout
- ✅ No credential logging

### Browser Security
- ✅ No-sandbox mode untuk container
- ✅ Disable GPU untuk stability
- ✅ Mobile user agent
- ✅ Network idle wait

## 🚨 Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Login failed` | Email/password salah | Cek credentials |
| `Chapter content must be at least 1,000 characters` | Content terlalu pendek | Tambah content |
| `Chapter content must be less than 60,000 characters` | Content terlalu panjang | Potong content |
| `Could not find chapter content field` | Selector tidak ditemukan | Coba lagi atau report bug |
| `Browser timeout` | Network lambat | Coba lagi |

### Debugging

Untuk debugging, cek logs di HF Spaces:

```
🚀 Starting Fizzo auto-update for chapter: Bab 28
🌐 Navigating to fizzo.org...
📱 Clicking hamburger menu...
✍️ Clicking 'Menulis Cerita'...
📧 Clicking 'Lanjutkan dengan Email'...
📝 Filling email field...
🔒 Filling password field...
🚀 Clicking 'Lanjut' button...
⏳ Waiting for dashboard...
✅ Login successful - Dashboard loaded
📝 Clicking 'New Chapter' button...
📖 Filling chapter title: Bab 28
📄 Filling chapter content (2500 characters)...
💾 Waiting for auto-save...
🚀 Publishing chapter...
✅ Chapter creation completed
```

## 🔧 Deployment Notes

### HF Spaces Requirements
- ✅ Playwright akan auto-install Chromium browser
- ✅ Headless mode untuk container environment
- ✅ Memory optimized untuk HF Spaces limits
- ✅ Timeout handling untuk HF Spaces restrictions

### Performance
- ⏱️ **Login**: ~10-15 detik
- ⏱️ **Chapter Upload**: ~5-10 detik
- ⏱️ **Total**: ~15-25 detik per chapter
- 💾 **Memory**: ~200-300MB saat browser aktif

## 🎯 Integration dengan Frontend

### Vercel Frontend Example

```javascript
// components/FizzoUploader.js
import { useState } from 'react';

export default function FizzoUploader() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  
  const uploadChapter = async (formData) => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/fizzo-auto-update`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      const result = await response.json();
      setResult(result);
    } catch (error) {
      setResult({ success: false, error: error.message });
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div>
      {/* Form UI here */}
      {loading && <p>🚀 Uploading chapter...</p>}
      {result && (
        <div>
          {result.success ? 
            <p>✅ Chapter uploaded successfully!</p> : 
            <p>❌ Error: {result.error}</p>
          }
        </div>
      )}
    </div>
  );
}
```

## 📝 Changelog

### v1.0.0
- ✅ Initial implementation
- ✅ Complete automation workflow
- ✅ Error handling dan validation
- ✅ HF Spaces optimization
- ✅ Security features

---

**🎉 Selamat! Fitur Fizzo Auto-Update siap digunakan!**

Untuk pertanyaan atau bug report, silakan buat issue di repository ini.