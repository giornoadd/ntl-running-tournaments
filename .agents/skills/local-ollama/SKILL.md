---
name: Local Ollama AI
description: Use local Ollama LLM (qwen3:8b) for text analysis, summarization, and Thai language processing without external API calls.
---

# 🧠 Local Ollama Skill

This skill allows any agent to use a **local Ollama LLM** for text processing tasks — no external API calls, no costs, fully private.

## Configuration

| Field | Value | .env Variable |
|---|---|---|
| **Base URL** | `http://localhost:11434/` | `OLLAMA_BASE_URL` |
| **Model** | `qwen3:8b` | `OLLAMA_MODEL` |
| **Temperature** | `0.7` (default) | `OLLAMA_TEMPERATURE` |
| **Top-K** | `40` (default) | `OLLAMA_TOP_K` |
| **Top-P** | `0.9` (default) | `OLLAMA_TOP_P` |

### Generation Parameter Guide

| Parameter | Range | Low = | High = |
|---|---|---|---|
| **Temperature** | 0.0 – 2.0 | แม่นยำ ซ้ำได้ deterministic | สร้างสรรค์ หลากหลาย |
| **Top-K** | 1 – 100 | เลือกจากคำน้อย conservative | กว้าง diverse |
| **Top-P** | 0.0 – 1.0 | เฉพาะคำที่น่าจะเป็นไปได้มาก | รวมคำหลากหลาย |

### Agent Presets

ใช้ preset เหล่านี้แทนการ set ค่าเอง:

| Preset | Temperature | Top-K | Top-P | ใช้กับ |
|---|---|---|---|---|
| `precise` | 0.1 | 10 | 0.5 | 🏟️ Coach: validate data, parse dates |
| `balanced` | 0.5 | 40 | 0.8 | 🏃 Running Coach: advice, analysis |
| `creative` | 0.7 | 40 | 0.9 | 📈 Sports Analyst: captions, summaries |
| `fun` | 0.9 | 50 | 0.95 | 📣 Reporter: LINE/Facebook, motivation |

---

## How to Use

### 1. Chat Completion (Text Generation)

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3:8b",
  "messages": [
    {"role": "system", "content": "You are a running coach. Respond in Thai."},
    {"role": "user", "content": "วิเคราะห์ผลวิ่ง: 5km, pace 8:30/km, HR 145bpm"}
  ],
  "stream": false,
  "options": {
    "temperature": 0.5,
    "top_k": 40,
    "top_p": 0.8
  }
}'
```

### 2. Text Generation (Simple)

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "qwen3:8b",
  "prompt": "สรุปผลการแข่งขันวิ่ง: Mandalorian 393km vs IT System 481km",
  "stream": false
}'
```

### 3. Health Check

```bash
curl http://localhost:11434/api/tags
```

---

## Use Cases per Agent

### 🏟️ Coach Assistant (process-image)
| Use Case | Prompt Hint |
|---|---|
| Validate activity type | "This activity shows 2.13km in 19:56. Is this a run or walk?" |
| Date parsing | "Parse this Thai date: 25 กุมภาพันธ์ 2569" |

### 🏃 Running Coach (running-coach)
| Use Case | Prompt Hint |
|---|---|
| Workout analysis | "Analyze: 5km at 8:30/km pace, HR 145bpm. Give coaching advice in Thai." |
| Plan suggestions | "Suggest next week's training based on: 3 runs, avg 4km, pace 9:00/km" |
| Motivation text | "Write a motivational message for a beginner runner who just ran 2km" |

### 📈 Sports Analyst (sports-analyst)
| Use Case | Prompt Hint |
|---|---|
| Summarize stats | "Summarize: GIO 241km/37 sessions, Jojo 151km/30 sessions. Compare." |
| Generate captions | "Write an infographic caption for a team scoring 481km total" |
| Trend analysis | "Week 1-4 avg 10km/week, Week 5-8 avg 15km/week. Analyze the trend." |

### 📣 Tournament Reporter (tournament-reporter)
| Use Case | Prompt Hint |
|---|---|
| LINE message | "Write a fun LINE update: IT System leads by 8.80km/person, Week 9" |
| Facebook post | "Write an exciting Facebook post about GIO reaching 241km" |
| Shoutout | "Write a gentle, funny motivation for Tae who hasn't run yet" |

---

## Python Integration

Use via `src/utils/config.py` (recommended) or standalone:

```python
import requests
from src.utils.config import (
    OLLAMA_BASE_URL, OLLAMA_MODEL,
    OLLAMA_TEMPERATURE, OLLAMA_TOP_K, OLLAMA_TOP_P,
    OLLAMA_PRESETS,
)

def ask_ollama(prompt: str, system: str = "", preset: str = None) -> str:
    """Send a prompt to local Ollama and return the response.
    
    Args:
        prompt: The question or instruction
        system: System prompt (role, language, style)
        preset: One of 'precise', 'balanced', 'creative', 'fun'
                Uses .env defaults if not specified
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    
    # Get generation options from preset or defaults
    if preset and preset in OLLAMA_PRESETS:
        opts = OLLAMA_PRESETS[preset]
    else:
        opts = {"temperature": OLLAMA_TEMPERATURE, "top_k": OLLAMA_TOP_K, "top_p": OLLAMA_TOP_P}
    
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
            "options": opts,
        },
        timeout=120
    )
    response.raise_for_status()
    return response.json()["message"]["content"]

# Examples:
# Coach (precise):   ask_ollama("Is 2.13km in 19:56 a run or walk?", preset="precise")
# Reporter (fun):    ask_ollama("เขียน LINE message สรุปสัปดาห์", preset="fun")
# Custom:            ask_ollama("วิเคราะห์ pace", system="You are a coach.")
```

---

## Prerequisites

1. **Ollama installed and running:**
   ```bash
   # Install (macOS)
   brew install ollama
   
   # Start server
   ollama serve
   ```

2. **Model pulled:**
   ```bash
   ollama pull qwen3:8b
   ```

3. **Verify:**
   ```bash
   curl http://localhost:11434/api/tags
   # Should list qwen3:8b
   ```

---

## When to Use Ollama vs Gemini

| Scenario | Use | Why |
|---|---|---|
| Thai text generation | ✅ Ollama | Free, fast, private |
| Motivational messages | ✅ Ollama | No API costs |
| Simple summarization | ✅ Ollama | Low latency |
| Image OCR/analysis | ❌ Gemini | Ollama can't read images |
| Complex reasoning | ⚖️ Either | Depends on quality needed |
| Batch processing text | ✅ Ollama | No rate limits |

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Connection refused | Run `ollama serve` first |
| Model not found | Run `ollama pull qwen3:8b` |
| Slow response | Check system RAM (8B model needs ~6GB) |
| Out of memory | Close other apps or use smaller model |
