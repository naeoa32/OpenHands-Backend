# Novel Writing Mode - OpenHands Backend

## Overview

Novel Writing Mode adalah fitur khusus di OpenHands Backend yang dioptimalkan untuk membantu penulisan kreatif berbahasa Indonesia. Mode ini menggunakan konfigurasi AI yang disesuaikan untuk creative writing dengan system prompt yang dirancang khusus untuk memberikan bantuan penulisan yang mendalam dan personal.

## Features

### 🎯 **Intelligent Model Selection**
- **Budget Mode**: Claude 3.5 Haiku untuk draft writing dan brainstorming
- **Premium Mode**: Claude 3 Opus untuk penulisan kompleks dan literary fiction
- Automatic model selection berdasarkan template dan kompleksitas content

### 🎨 **Creative Writing Templates**
- `character-development`: Pengembangan karakter yang kompleks
- `plot-structure`: Bantuan struktur cerita dan plot
- `dialogue-writing`: Penulisan dialog yang natural
- `world-building`: Membangun dunia cerita yang immersive
- `style-voice`: Mengembangkan gaya dan suara penulis
- `theme-symbolism`: Eksplorasi tema dan simbolisme
- `editing-revision`: Bantuan editing dan revisi

### 🧠 **AI Configuration**
- **Temperature**: 0.8 (optimal untuk kreativitas)
- **Max Tokens**: 4000 (untuk respons yang komprehensif)
- **Top P**: 0.9 (keseimbangan kreativitas dan konsistensi)

### 🇮🇩 **Indonesian Language Focus**
- System prompt dalam bahasa Indonesia
- Pemahaman nuansa budaya dan konteks Indonesia
- Gaya bahasa yang natural dan ekspresif

## API Integration

### Frontend Request Format

Frontend mengirim data melalui WebSocket dengan format:

```json
{
  "action": "message",
  "args": {
    "content": "Enhanced prompt dari novel service",
    "novel_mode": true,
    "original_prompt": "Input asli user",
    "template_used": "character-development"
  }
}
```

### Backend Processing

1. **Detection**: Backend mendeteksi `novel_mode: true`
2. **Model Selection**: Menentukan model berdasarkan template dan kompleksitas
3. **Configuration**: Mengaplikasikan parameter AI yang optimal
4. **System Prompt**: Menginjeksi system prompt khusus creative writing
5. **Response**: AI memberikan bantuan yang spesifik dan mendalam

## Deployment Configuration

### Environment Variables

```bash
# OpenRouter Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
LLM_API_KEY=your_openrouter_api_key_here
LLM_BASE_URL=https://openrouter.ai/api/v1

# Novel Writing Models
NOVEL_WRITING_BUDGET_MODEL=openrouter/anthropic/claude-3-haiku-20240307
NOVEL_WRITING_PREMIUM_MODEL=openrouter/anthropic/claude-3-opus-20240229

# OpenRouter Headers
OR_SITE_URL=https://docs.all-hands.dev/
OR_APP_NAME=OpenHands-NovelWriting
```

### Render Deployment

File `render.yaml` sudah dikonfigurasi untuk deployment di Render dengan:
- Auto-scaling berdasarkan traffic
- Environment variables yang diperlukan
- Health check endpoint
- Resource allocation yang optimal

## Usage Examples

### Character Development
```json
{
  "action": "message",
  "args": {
    "content": "Bantu saya mengembangkan karakter protagonis untuk novel fantasi saya",
    "novel_mode": true,
    "original_prompt": "Saya butuh bantuan karakter utama",
    "template_used": "character-development"
  }
}
```

### Plot Structure
```json
{
  "action": "message", 
  "args": {
    "content": "Saya punya ide cerita tentang seorang detektif, tapi bingung strukturnya",
    "novel_mode": true,
    "original_prompt": "Bantuan struktur plot detektif",
    "template_used": "plot-structure"
  }
}
```

## AI Behavior

### No Generic Responses
AI akan **selalu** bertanya detail spesifik sebelum memberikan saran:

❌ **Generic**: "Untuk mengembangkan karakter, Anda bisa..."
✅ **Specific**: "Ceritakan tentang karakter utama Anda - apa yang membuatnya unik? Apa konflik internal terbesar yang dihadapinya?"

### Deep Questioning
AI menggunakan pertanyaan yang membantu penulis mengeksplorasi ide mereka:
- Motivasi dan konflik internal karakter
- Detail sensory untuk world-building
- Subteks dalam dialog
- Tema dan simbolisme yang mendalam

### Cultural Awareness
AI memahami dan mengintegrasikan:
- Nuansa budaya Indonesia
- Konteks sosial dan sejarah
- Gaya bahasa yang sesuai
- Referensi yang relevan

## Technical Implementation

### Files Modified/Created

1. **`openhands/events/action/message.py`**
   - Extended MessageAction dengan novel_mode fields

2. **`openhands/core/novel_writing_prompts.py`**
   - System prompts untuk creative writing
   - Template-specific questions

3. **`openhands/core/novel_writing_config.py`**
   - LLM configuration untuk novel writing
   - Model selection logic

4. **`openhands/server/session/session.py`**
   - Novel mode detection dan handling
   - Dynamic LLM config switching

### Error Handling

- Graceful fallback ke regular mode jika novel mode gagal
- Detailed error messages untuk debugging
- Status updates untuk user feedback

### Performance Optimization

- Intelligent model selection untuk cost efficiency
- Optimized parameters untuk creative writing
- Minimal latency dengan proper async handling

## Monitoring & Analytics

Backend menyediakan status updates untuk monitoring:

```json
{
  "status_update": true,
  "type": "info",
  "id": "NOVEL_MODE_ACTIVATED", 
  "message": "Novel Writing Mode diaktifkan dengan template: character-development"
}
```

```json
{
  "status_update": true,
  "type": "info",
  "id": "NOVEL_MODEL_SELECTED",
  "message": "Menggunakan Claude 3 Opus (Premium) untuk kualitas penulisan optimal"
}
```

## Future Enhancements

- [ ] Custom system prompts per user
- [ ] Writing style analysis dan recommendations
- [ ] Integration dengan grammar checking
- [ ] Multi-language support
- [ ] Advanced analytics untuk writing patterns
- [ ] Collaborative writing features

## Support

Untuk issues atau questions terkait Novel Writing Mode:
1. Check logs untuk error messages
2. Verify environment variables
3. Test dengan regular mode untuk isolate issues
4. Monitor status updates dari backend