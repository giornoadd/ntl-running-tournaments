# 🧠 Ollama Configuration Guide

คู่มือการตั้งค่า Local Ollama LLM สำหรับ AI Agent System

---

## Quick Start

```bash
# 1. Install
brew install ollama

# 2. Start server
ollama serve

# 3. Pull model
ollama pull qwen3:8b

# 4. Verify
curl http://localhost:11434/api/tags
```

---

## Environment Variables (`.env`)

```bash
# Local Ollama LLM
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:8b
OLLAMA_TEMPERATURE=0.7
OLLAMA_TOP_K=40
OLLAMA_TOP_P=0.9
```

---

## Generation Parameters

### Temperature

ควบคุมความ **random** ของผลลัพธ์

| ค่า | ผลลัพธ์ | ตัวอย่างใช้งาน |
|---|---|---|
| **0.0** | ให้ผลเหมือนกันทุกครั้ง (deterministic) | ไม่เหมาะกับ content |
| **0.1** | แม่นยำมาก ซ้ำได้ | ✅ Validate data, parse dates |
| **0.3** | ค่อนข้างแม่นยำ | ✅ Factual summaries |
| **0.5** | สมดุลระหว่างแม่นยำและสร้างสรรค์ | ✅ Coaching advice |
| **0.7** | สร้างสรรค์พอดี **(default)** | ✅ Captions, analysis |
| **0.9** | สร้างสรรค์มาก หลากหลาย | ✅ LINE/Facebook posts |
| **1.5+** | สุ่มมากเกินไป อาจไม่สอดคล้อง | ❌ หลีกเลี่ยง |

### Top-K

จำกัดจำนวน **token ที่พิจารณา** ในแต่ละ step

| ค่า | ผลลัพธ์ | ตัวอย่างใช้งาน |
|---|---|---|
| **1** | เลือกคำที่น่าจะเป็นมากที่สุดเท่านั้น | Greedy – ไม่แนะนำ |
| **10** | เลือกจาก 10 ตัวเลือก | ✅ Precise tasks |
| **40** | สมดุล **(default)** | ✅ General use |
| **50** | กว้างขึ้น | ✅ Creative content |
| **100** | กว้างมาก | สำหรับ brainstorming |

### Top-P (Nucleus Sampling)

เลือก tokens ที่รวมกันมี **ความน่าจะเป็นสะสม** ถึงค่าที่กำหนด

| ค่า | ผลลัพธ์ | ตัวอย่างใช้งาน |
|---|---|---|
| **0.1** | เฉพาะคำที่มั่นใจมากๆ | Very focused |
| **0.5** | ค่อนข้าง focused | ✅ Data validation |
| **0.8** | สมดุล | ✅ General advice |
| **0.9** | หลากหลายพอดี **(default)** | ✅ Content creation |
| **0.95** | หลากหลายมาก | ✅ Fun, creative writing |
| **1.0** | ไม่ filter เลย | ไม่แนะนำ |

---

## Agent Presets

Preset ที่ปรับแต่งมาให้เหมาะกับแต่ละ Agent แล้ว:

| Preset | Temperature | Top-K | Top-P | Agent ที่เหมาะ |
|---|---|---|---|---|
| `precise` | 0.1 | 10 | 0.5 | 🏟️ Coach Assistant |
| `balanced` | 0.5 | 40 | 0.8 | 🏃 Running Coach |
| `creative` | 0.7 | 40 | 0.9 | 📈 Sports Analyst |
| `fun` | 0.9 | 50 | 0.95 | 📣 Tournament Reporter |

### เมื่อไหร่ควรใช้ Preset ไหน

```
📸 ตรวจว่า activity เป็น run หรือ walk?     → precise
📊 วิเคราะห์ผลวิ่งและให้คำแนะนำ             → balanced  
🎨 เขียน caption สำหรับ infographic          → creative
📱 เขียนข้อความ LINE สนุกๆ                   → fun
```

---

## Python Usage

### ใช้ผ่าน config.py (แนะนำ)

```python
from src.utils.config import (
    OLLAMA_BASE_URL, OLLAMA_MODEL,
    OLLAMA_TEMPERATURE, OLLAMA_TOP_K, OLLAMA_TOP_P,
    OLLAMA_PRESETS,
)

# ใช้ preset
opts = OLLAMA_PRESETS["fun"]  # {"temperature": 0.9, "top_k": 50, "top_p": 0.95}

# หรือ override เอง
opts = {"temperature": 0.3, "top_k": 20, "top_p": 0.7}
```

### curl ตรงๆ

```bash
# Precise mode (validate data)
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3:8b",
  "messages": [{"role": "user", "content": "2.13km ใน 19:56 เป็นวิ่งหรือเดิน?"}],
  "stream": false,
  "options": {"temperature": 0.1, "top_k": 10, "top_p": 0.5}
}'

# Fun mode (LINE message)
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3:8b",
  "messages": [{"role": "user", "content": "เขียน LINE message สรุปสัปดาห์นี้แบบสนุกๆ"}],
  "stream": false,
  "options": {"temperature": 0.9, "top_k": 50, "top_p": 0.95}
}'
```

---

## Tips

1. **เริ่มจาก preset** แล้วค่อยปรับ — ไม่ต้อง set ค่าเองถ้าไม่จำเป็น
2. **Temperature + Top-P ทำงานด้วยกัน** — ถ้า temp ต่ำ top_p จะมีผลน้อย
3. **Top-K vs Top-P** — ใช้อันใดอันหนึ่งก็ได้ แต่ใช้ด้วยกันจะได้ผลดีกว่า
4. **ภาษาไทย** — อาจต้องใช้ temp สูงกว่าภาษาอังกฤษเล็กน้อย เพราะ token variety
5. **ถ้าผลลัพธ์วนซ้ำ** — เพิ่ม temperature ขึ้น 0.1-0.2
6. **ถ้าผลลัพธ์ไม่สัมพันธ์กัน** — ลด temperature ลง 0.1-0.2

---

## Troubleshooting

| ปัญหา | สาเหตุ | แก้ไข |
|---|---|---|
| ผลลัพธ์ซ้ำเหมือนกันทุกครั้ง | Temperature ต่ำเกินไป | เพิ่ม temperature เป็น 0.5+ |
| ผลลัพธ์ไม่สอดคล้อง พูดไม่รู้เรื่อง | Temperature สูงเกินไป | ลดเป็น 0.5-0.7 |
| ผลลัพธ์สั้นเกินไป | Top-K ต่ำเกินไป | เพิ่ม top_k เป็น 40+ |
| ตอบเรื่องอื่นที่ไม่เกี่ยว | Top-P สูงเกินไป | ลด top_p เป็น 0.8 |
| Connection refused | Server ไม่ได้เปิด | `ollama serve` |
| Model not found | ยังไม่ได้ pull | `ollama pull qwen3:8b` |

---

*Last updated: 2026-02-25*
