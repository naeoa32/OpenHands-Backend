# 🚀 Complete Features Guide - OpenHands Backend

## 🎯 Overview

OpenHands Backend adalah AI agent platform yang powerful dengan berbagai fitur canggih, termasuk **Novel Writing Mode** dan **Multiple AI Agents** seperti saya! Berikut adalah panduan lengkap semua fitur yang tersedia.

## 🤖 AI Agents Available

### 1. **CodeActAgent** (Default - Seperti Saya!)
**Capabilities:**
- ✅ **Code Execution** - Menjalankan Python, JavaScript, Bash commands
- ✅ **File Operations** - Create, edit, read, delete files
- ✅ **Web Browsing** - Browse websites, extract information
- ✅ **Problem Solving** - Debug code, fix errors, optimize performance
- ✅ **Project Development** - Build complete applications
- ✅ **Data Analysis** - Process and analyze data
- ✅ **API Integration** - Connect to external services

**Tools Available:**
- `str_replace_editor` - Edit files with precision
- `bash` - Execute terminal commands
- `ipython` - Run Python code interactively
- `browser` - Browse and interact with websites
- `think` - Internal reasoning and planning
- `finish` - Complete tasks with results

### 2. **BrowsingAgent**
**Specialized for:**
- ✅ **Web Research** - Advanced web browsing and data extraction
- ✅ **Content Scraping** - Extract structured data from websites
- ✅ **Market Research** - Gather competitive intelligence
- ✅ **News Monitoring** - Track latest developments

### 3. **ReadOnlyAgent**
**Safe for:**
- ✅ **Code Review** - Analyze code without modifications
- ✅ **Documentation** - Generate docs from existing code
- ✅ **Security Audit** - Review code for vulnerabilities
- ✅ **Learning** - Understand codebases safely

### 4. **LocAgent** (Lines of Code)
**Optimized for:**
- ✅ **Code Generation** - Generate specific code snippets
- ✅ **Function Creation** - Create targeted functions
- ✅ **Quick Fixes** - Small, precise code changes

### 5. **VisualBrowsingAgent**
**Advanced browsing with:**
- ✅ **Visual Understanding** - Process screenshots and visual content
- ✅ **UI Interaction** - Interact with complex web interfaces
- ✅ **Visual Testing** - Test UI components

## 📝 Novel Writing Mode (Fitur Khusus Indonesia!)

### 🎨 Creative Writing Templates

#### 1. **Character Development** (`character-development`)
```bash
POST /novel/write
{
  "message": "Bantu saya mengembangkan karakter protagonis untuk novel fantasi",
  "template": "character-development"
}
```

**AI akan membantu dengan:**
- Latar belakang karakter yang mendalam
- Motivasi dan konflik internal
- Arc perkembangan karakter
- Hubungan dengan karakter lain

#### 2. **Plot Structure** (`plot-structure`)
```bash
POST /novel/write
{
  "message": "Saya punya ide cerita detektif tapi bingung strukturnya",
  "template": "plot-structure"
}
```

**AI akan membantu dengan:**
- Three-act structure
- Plot points dan turning points
- Pacing dan tension building
- Subplot integration

#### 3. **Dialogue Writing** (`dialogue-writing`)
```bash
POST /novel/write
{
  "message": "Dialog karakter saya terasa kaku dan tidak natural",
  "template": "dialogue-writing"
}
```

**AI akan membantu dengan:**
- Natural conversation flow
- Character voice differentiation
- Subtext dan implied meaning
- Dialogue tags dan action beats

#### 4. **World Building** (`world-building`)
```bash
POST /novel/write
{
  "message": "Butuh bantuan membangun dunia fantasi yang konsisten",
  "template": "world-building"
}
```

**AI akan membantu dengan:**
- Setting dan geography
- Culture dan social systems
- Magic systems atau technology
- History dan mythology

#### 5. **Style & Voice** (`style-voice`)
```bash
POST /novel/write
{
  "message": "Ingin mengembangkan gaya penulisan yang unik",
  "template": "style-voice"
}
```

**AI akan membantu dengan:**
- Narrative voice development
- Tone dan mood consistency
- Prose style refinement
- Point of view optimization

#### 6. **Theme & Symbolism** (`theme-symbolism`)
```bash
POST /novel/write
{
  "message": "Bagaimana mengintegrasikan tema keadilan dalam cerita?",
  "template": "theme-symbolism"
}
```

**AI akan membantu dengan:**
- Theme exploration
- Symbolic elements
- Metaphor development
- Deeper meaning layers

#### 7. **Editing & Revision** (`editing-revision`)
```bash
POST /novel/write
{
  "message": "Draft pertama sudah selesai, butuh bantuan revisi",
  "template": "editing-revision"
}
```

**AI akan membantu dengan:**
- Structural editing
- Line editing suggestions
- Consistency checks
- Flow improvement

### 🧠 Intelligent Model Selection

**Budget Mode (Claude 3.5 Haiku):**
- Draft writing
- Brainstorming
- Quick feedback
- Character sketches

**Premium Mode (Claude 3 Opus):**
- Complex narratives
- Literary fiction
- Deep character analysis
- Professional editing

**Auto-selection based on:**
- Template complexity
- Content length
- Writing sophistication needed

## 🌐 API Endpoints Complete List

### 🏥 Health & Status
```bash
GET /health                    # Overall health check
GET /novel/health             # Novel writing service health
GET /test-chat/health         # Test chat health
GET /openrouter/health        # OpenRouter connection health
```

### ⚙️ Configuration
```bash
GET /api/options/config       # Get system configuration
GET /api/options/models       # Available LLM models
GET /api/options/agents       # Available AI agents
```

### 💬 Conversations (Main Features)
```bash
# Standard AI Agent Conversations
POST /api/conversations
{
  "initial_user_msg": "Help me build a web app",
  "agent": "CodeActAgent"  # Optional, defaults to CodeActAgent
}

# Simple Quick Chat
POST /api/simple/conversation
{
  "message": "Explain quantum computing"
}

# Memory-based Conversations
POST /memory-chat/message
{
  "message": "Remember our previous discussion about AI",
  "session_id": "optional-session-id"
}

# Real-time Chat with OpenRouter
POST /chat/message
{
  "message": "Write a Python function for sorting",
  "model": "claude-3-haiku"  # Optional
}
```

### 📝 Novel Writing (Indonesian Creative Writing)
```bash
# Novel Writing with Templates
POST /novel/write
{
  "message": "Bantu saya mengembangkan karakter utama",
  "template": "character-development",
  "session_id": "optional",
  "force_premium": false
}

# Get Available Templates
GET /novel/templates

# Get Template Questions
GET /novel/questions/character-development

# Manage Sessions
GET /novel/sessions
GET /novel/sessions/{session_id}
DELETE /novel/sessions/{session_id}

# Model Information
GET /novel/models
```

### 🧪 Testing & Development
```bash
# Test Chat (Ultra Simple)
POST /test-chat/message
{
  "message": "Hello world"
}

# OpenRouter Direct Test
POST /openrouter/test
{
  "message": "Test message",
  "model": "claude-3-haiku"
}
```

## 🎯 Use Cases & Examples

### 1. **AI Coding Assistant** (Seperti Saya!)
```javascript
// Create coding conversation
const response = await fetch('/api/conversations', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    initial_user_msg: 'Build a REST API with FastAPI for a todo app',
    agent: 'CodeActAgent'
  })
});
```

### 2. **Indonesian Novel Writing**
```javascript
// Start novel writing session
const response = await fetch('/novel/write', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Saya ingin menulis novel romance contemporary',
    template: 'character-development'
  })
});
```

### 3. **Web Research Agent**
```javascript
// Use browsing agent for research
const response = await fetch('/api/conversations', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    initial_user_msg: 'Research the latest AI trends and create a summary',
    agent: 'BrowsingAgent'
  })
});
```

### 4. **Quick Code Review**
```javascript
// Safe code review without modifications
const response = await fetch('/api/conversations', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    initial_user_msg: 'Review this Python code for security issues: [code]',
    agent: 'ReadOnlyAgent'
  })
});
```

## 🔧 Advanced Configuration

### Environment Variables
```bash
# Core LLM Configuration
LLM_API_KEY=your_openrouter_api_key
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307
LLM_BASE_URL=https://openrouter.ai/api/v1

# Novel Writing Models
NOVEL_WRITING_BUDGET_MODEL=openrouter/anthropic/claude-3-haiku-20240307
NOVEL_WRITING_PREMIUM_MODEL=openrouter/anthropic/claude-3-opus-20240229

# Agent Configuration
DEFAULT_AGENT=CodeActAgent
MAX_ITERATIONS=30

# Runtime Configuration
OPENHANDS_RUNTIME=local
DISABLE_SECURITY=true
OPENHANDS_DISABLE_AUTH=true
```

### Model Selection Strategy
```python
# Automatic model selection for novel writing
def select_model(template, content_length, force_premium=False):
    if force_premium:
        return "claude-3-opus"
    
    complex_templates = ["style-voice", "theme-symbolism", "editing-revision"]
    if template in complex_templates or content_length > 1500:
        return "claude-3-opus"  # Premium
    else:
        return "claude-3-haiku"  # Budget
```

## 🚀 Frontend Integration Examples

### React Integration
```jsx
import { useState } from 'react';

function AIChat() {
  const [messages, setMessages] = useState([]);
  
  const sendMessage = async (message, agent = 'CodeActAgent') => {
    const response = await fetch('/api/conversations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        initial_user_msg: message,
        agent: agent
      })
    });
    
    const data = await response.json();
    setMessages(prev => [...prev, data]);
  };
  
  return (
    <div>
      <button onClick={() => sendMessage('Help me code', 'CodeActAgent')}>
        Coding Help
      </button>
      <button onClick={() => sendMessage('Research AI trends', 'BrowsingAgent')}>
        Research
      </button>
    </div>
  );
}
```

### Novel Writing Interface
```jsx
function NovelWriter() {
  const [session, setSession] = useState(null);
  
  const writeWithTemplate = async (message, template) => {
    const response = await fetch('/novel/write', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        template,
        session_id: session?.id
      })
    });
    
    const data = await response.json();
    setSession(data);
  };
  
  return (
    <div>
      <button onClick={() => writeWithTemplate('Bantu karakter', 'character-development')}>
        Character Development
      </button>
      <button onClick={() => writeWithTemplate('Struktur cerita', 'plot-structure')}>
        Plot Structure
      </button>
    </div>
  );
}
```

## 🎉 Summary

**OpenHands Backend menyediakan:**

### 🤖 **AI Agents**
- **CodeActAgent** - Full-featured coding assistant (seperti saya!)
- **BrowsingAgent** - Web research specialist
- **ReadOnlyAgent** - Safe code review
- **LocAgent** - Targeted code generation
- **VisualBrowsingAgent** - Visual web interaction

### 📝 **Novel Writing Mode**
- **7 Templates** - Character, plot, dialogue, world-building, style, theme, editing
- **Indonesian Language** - Optimized untuk penulis Indonesia
- **Smart Model Selection** - Budget vs Premium berdasarkan kompleksitas
- **Session Management** - Persistent writing sessions

### 🌐 **API Endpoints**
- **20+ Endpoints** - Comprehensive API coverage
- **Multiple Chat Types** - Standard, simple, memory, real-time
- **Health Monitoring** - Service status tracking
- **Configuration** - Flexible model and agent selection

### ✅ **Ready Features**
- ✅ No authentication required
- ✅ CORS enabled for all frontends
- ✅ Memory-based storage (HF Spaces compatible)
- ✅ Error handling and fallbacks
- ✅ Multiple LLM providers support
- ✅ Real-time conversation capabilities

**Siap deploy ke Hugging Face Spaces dan langsung digunakan!** 🚀