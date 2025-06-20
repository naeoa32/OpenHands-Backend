# 🚀 Fizzo.org Auto-Update API Guide

## 📋 Overview

Fitur ini memungkinkan kamu untuk **otomatis upload chapter novel ke fizzo.org** melalui API call sederhana. Tidak perlu lagi manual login, navigate, copy-paste, dan publish chapter satu per satu!

## 🎯 Benefits

- ✅ **Hemat Waktu**: 15-25 detik vs 2-3 menit manual
- ✅ **Eliminasi Error**: Tidak ada typo atau lupa publish
- ✅ **Batch Processing**: Bisa upload multiple chapters sekaligus
- ✅ **Easy Integration**: Simple REST API call
- ✅ **Frontend Ready**: Bisa diintegrasikan ke website/app

## 📡 API Endpoint

```
POST /api/fizzo-auto-update
Content-Type: application/json
```

**Base URL**: `https://your-backend.hf.space` (ganti dengan URL HF Spaces kamu)

## 📝 Request Format

```json
{
  "email": "your_email@gmail.com",
  "password": "your_password",
  "chapter_title": "Bab 28: Pertarungan Terakhir",
  "chapter_content": "Isi chapter novel minimal 1000 karakter..."
}
```

### 🔧 Field Requirements

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | ✅ | Email login fizzo.org |
| `password` | string | ✅ | Password login fizzo.org |
| `chapter_title` | string | ✅ | Judul chapter (contoh: "Bab 28: Judul") |
| `chapter_content` | string | ✅ | Isi chapter (1,000-60,000 karakter) |

## 📊 Response Format

### ✅ Success Response (200)

```json
{
  "success": true,
  "message": "Chapter berhasil diupload ke fizzo.org",
  "data": {
    "success": true,
    "message": "Chapter created successfully",
    "chapter_title": "Bab 28: Pertarungan Terakhir",
    "content_length": 2847,
    "published": true,
    "confirmed": true
  }
}
```

### ❌ Error Response (400/500)

```json
{
  "success": false,
  "error": "Chapter content must be at least 1,000 characters"
}
```

## 🐍 Python Example

```python
import requests
import json

# Data chapter
chapter_data = {
    "email": "your_email@gmail.com",
    "password": "your_password",
    "chapter_title": "Bab 28: Pertarungan Terakhir",
    "chapter_content": """
    Angin malam bertiup kencang di atas atap gedung pencakar langit...
    [Isi chapter minimal 1000 karakter]
    """
}

# Send request
response = requests.post(
    "https://your-backend.hf.space/api/fizzo-auto-update",
    json=chapter_data,
    headers={"Content-Type": "application/json"}
)

# Check result
if response.status_code == 200:
    result = response.json()
    if result["success"]:
        print("✅ Chapter berhasil diupload ke fizzo.org!")
        print(f"📊 Data: {result['data']}")
    else:
        print(f"❌ Upload gagal: {result['error']}")
else:
    print(f"❌ HTTP Error: {response.status_code}")
```

## 🌐 JavaScript/Frontend Example

```javascript
// Data chapter
const chapterData = {
    email: "your_email@gmail.com",
    password: "your_password",
    chapter_title: "Bab 28: Pertarungan Terakhir",
    chapter_content: "Isi chapter minimal 1000 karakter..."
};

// Send request
fetch("https://your-backend.hf.space/api/fizzo-auto-update", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(chapterData)
})
.then(response => response.json())
.then(result => {
    if (result.success) {
        console.log("✅ Chapter berhasil diupload!");
        console.log("📊 Data:", result.data);
        
        // Update UI
        showSuccessMessage("Chapter berhasil dipublish ke fizzo.org!");
    } else {
        console.error("❌ Upload gagal:", result.error);
        showErrorMessage(result.error);
    }
})
.catch(error => {
    console.error("❌ Network error:", error);
    showErrorMessage("Koneksi bermasalah, coba lagi nanti");
});
```

## 🔄 Batch Upload Example

```python
import requests
import time

def upload_multiple_chapters(chapters):
    """Upload multiple chapters dengan delay"""
    
    results = []
    
    for i, chapter in enumerate(chapters):
        print(f"📝 Uploading chapter {i+1}/{len(chapters)}: {chapter['chapter_title']}")
        
        response = requests.post(
            "https://your-backend.hf.space/api/fizzo-auto-update",
            json=chapter,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                print(f"✅ Success: {chapter['chapter_title']}")
                results.append({"chapter": chapter['chapter_title'], "status": "success"})
            else:
                print(f"❌ Failed: {result['error']}")
                results.append({"chapter": chapter['chapter_title'], "status": "failed", "error": result['error']})
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            results.append({"chapter": chapter['chapter_title'], "status": "http_error"})
        
        # Delay antar upload untuk menghindari rate limiting
        if i < len(chapters) - 1:
            print("⏳ Waiting 30 seconds before next upload...")
            time.sleep(30)
    
    return results

# Example usage
chapters = [
    {
        "email": "your_email@gmail.com",
        "password": "your_password",
        "chapter_title": "Bab 28: Pertarungan Terakhir",
        "chapter_content": "Content chapter 28..."
    },
    {
        "email": "your_email@gmail.com", 
        "password": "your_password",
        "chapter_title": "Bab 29: Kemenangan Pahit",
        "chapter_content": "Content chapter 29..."
    }
]

results = upload_multiple_chapters(chapters)
print(f"📊 Upload completed: {results}")
```

## ⚠️ Important Notes

### 🔒 Security
- **Jangan hardcode credentials** di frontend code
- Gunakan environment variables atau secure storage
- Consider menggunakan authentication token untuk production

### ⏱️ Performance
- Setiap upload memakan waktu **15-25 detik**
- Untuk batch upload, beri **delay 30 detik** antar request
- Jangan spam request untuk menghindari rate limiting

### 🛡️ Error Handling
- Selalu check `response.status_code` dan `result.success`
- Handle network errors dengan try-catch
- Implement retry logic untuk network failures

### 📏 Content Guidelines
- **Minimal**: 1,000 karakter
- **Maksimal**: 60,000 karakter
- **Format**: Plain text (HTML akan di-strip)
- **Encoding**: UTF-8 untuk karakter Indonesia

## 🚨 Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Email and password are required` | Missing credentials | Check email/password fields |
| `Chapter content must be at least 1,000 characters` | Content too short | Add more content |
| `Login failed` | Wrong credentials | Verify fizzo.org login |
| `Could not find chapter title field` | Fizzo.org UI changed | Report to developer |
| `Network timeout` | Slow connection | Retry request |

## 🔧 Troubleshooting

### 1. Login Issues
```bash
# Test credentials manually di fizzo.org
# Pastikan bisa login normal via browser
```

### 2. Content Issues
```python
# Check content length
content = "Your chapter content..."
print(f"Content length: {len(content)} characters")

# Minimum 1000 characters required
if len(content) < 1000:
    print("❌ Content too short, add more text")
```

### 3. Network Issues
```python
import requests

try:
    response = requests.post(url, json=data, timeout=60)
except requests.exceptions.Timeout:
    print("❌ Request timeout, try again")
except requests.exceptions.ConnectionError:
    print("❌ Connection error, check internet")
```

## 🎯 Best Practices

### 1. **Content Preparation**
```python
def prepare_chapter_content(raw_content):
    """Prepare content for fizzo upload"""
    
    # Remove excessive whitespace
    content = " ".join(raw_content.split())
    
    # Ensure minimum length
    if len(content) < 1000:
        raise ValueError("Content too short")
    
    # Ensure maximum length  
    if len(content) > 60000:
        content = content[:60000] + "..."
        
    return content
```

### 2. **Error Handling**
```python
def safe_upload_chapter(chapter_data):
    """Upload with comprehensive error handling"""
    
    try:
        response = requests.post(
            endpoint,
            json=chapter_data,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                return {"status": "success", "data": result["data"]}
            else:
                return {"status": "failed", "error": result["error"]}
        else:
            return {"status": "http_error", "code": response.status_code}
            
    except requests.exceptions.Timeout:
        return {"status": "timeout"}
    except requests.exceptions.ConnectionError:
        return {"status": "connection_error"}
    except Exception as e:
        return {"status": "unknown_error", "error": str(e)}
```

### 3. **Frontend Integration**
```javascript
class FizzoUploader {
    constructor(backendUrl) {
        this.backendUrl = backendUrl;
    }
    
    async uploadChapter(chapterData) {
        try {
            const response = await fetch(`${this.backendUrl}/api/fizzo-auto-update`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(chapterData)
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                return { success: true, data: result.data };
            } else {
                return { success: false, error: result.error || 'Unknown error' };
            }
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
}

// Usage
const uploader = new FizzoUploader('https://your-backend.hf.space');
const result = await uploader.uploadChapter(chapterData);
```

## 🚀 Ready to Use!

1. **Deploy backend** ke HF Spaces
2. **Update URL** di code examples
3. **Test dengan credentials** asli
4. **Integrate ke frontend** kamu
5. **Enjoy automated publishing!** 🎉

---

**Happy Writing! 📝✨**