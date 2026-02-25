# 🤖 AI Agent System — How to Use

This project uses **4 AI Agents** and **2 Shared Skills** to manage the Running Competition 2026. Each agent is specialized for a different aspect of tournament operations.

---

## Agent Overview

```
📸 /process-image       →  รับภาพ → rename → update stats → สรุปผล
🏃 /running-coach       →  วิเคราะห์การวิ่ง → ตั้งเป้า → แผนฝึก HM
📈 /sports-analyst      →  Infographic → Personal card → Recap
� /tournament-reporter →  ข่าว → LINE/Facebook → เชียร์ → motivation
�📚 NotebookLM Skill     →  Research กฎ/กลยุทธ์ (shared ทุก agent)
```

---

## 🏟️ Agent 1: Coach Assistant (`/process-image`)

### Objective
จัดการงาน operations ทั้งหมด — รับหลักฐานใหม่, rename ไฟล์, อัพเดตสถิติ, สรุปผล tournament

### Modes

| Mode | Description |
|---|---|
| 📸 **Process Evidence** | รับ screenshot ใหม่ → rename → extract data → update CSV + stats |
| 📊 **Tournament Summary** | สรุปคะแนนทีม, Top 5, active/inactive members |
| 🔄 **Batch Processing** | ประมวลผลหลายรูปพร้อมกัน |

### How to Use

```
# ส่งรูปใหม่เข้ามา
/process-image member_results/ITSystem-3_O (โอ)/IMG_1234.jpg

# สรุปผล tournament
/process-image สรุปผลการแข่งขัน

# Batch processing หลายรูป
/process-image ประมวลผลรูปใหม่ทั้งหมดใน member_results/
```

### Output
- ✅ Renamed file (e.g., `o-2026-feb-25.jpg`)
- ✅ Updated `personal-statistics.md`
- ✅ Updated `results/{month}.csv`
- ✅ Regenerated member README

---

## 🏃 Agent 2: Running Coach (`/running-coach`)

### Objective
โค้ชส่วนตัวสำหรับทุกคน — วิเคราะห์ผลวิ่ง, ติดตามแผน, ตั้งเป้าหมาย, ให้คำแนะนำพัฒนาการวิ่งครั้งถัดไป

### Modes

| Mode | Description |
|---|---|
| 📊 **Post-Run Analysis** | วิเคราะห์เซสซั่นล่าสุด เทียบกับ 5 ครั้งก่อนหน้า + ตรวจว่าตามแผนไหม |
| 🎯 **Goal Setting** | ถาม-ตอบกับนักกีฬาเพื่อตั้งเป้าหมายร่วมกัน |
| 📋 **Progress Review** | รีวิวรายสัปดาห์/เดือน + เทียบแผน vs จริง |
| 🏗️ **Plan Creation** | สร้าง `personal-statistics.md` + `running-plan.md` |

### How to Use

```
# วิเคราะห์ผลวิ่งล่าสุด
/running-coach วิเคราะห์ผลวิ่งล่าสุดของ Ton

# ตั้งเป้าหมาย
/running-coach ตั้งเป้าหมายให้ Sand

# รีวิวความก้าวหน้า
/running-coach รีวิวความก้าวหน้าของ O ตลอดเดือน Feb

# สร้างแผนฝึก HM ให้คนใหม่
/running-coach สร้างแผน Running Plan ให้ Boy
```

### Output
- 📊 Post-Run Analysis (comparison table + coach advice)
- 🎯 Updated goals in `running-plan.md`
- 📋 Progress report (plan vs actual)
- 🏗️ New `personal-statistics.md` + `running-plan.md`

---

## 📈 Agent 3: Sports Analyst (`/sports-analyst`)

### Objective
สร้าง content สำหรับ infographic, personal stats card, weekly/monthly recap — พร้อมแชร์ใน LINE group

### Content Types

| Type | Description |
|---|---|
| 🏆 **Tournament Infographic** | ภาพรวม: Team standings, Top 5, contribution chart |
| 👤 **Personal Stats Card** | สรุปสถิติรายบุคคล: progression, pace, achievements |
| 📅 **Weekly/Monthly Recap** | MVP, scoreboard, activity feed |
| 🎨 **Custom Visual** | เปรียบเทียบ, ranking, Head-to-Head |

### How to Use

```
# สรุปผล tournament
/sports-analyst สรุปผล tournament ประจำเดือน February

# ทำ personal card
/sports-analyst ทำ personal infographic ให้ GIO

# สรุปประจำสัปดาห์
/sports-analyst สรุปสัปดาห์นี้

# เปรียบเทียบ 2 คน
/sports-analyst เปรียบเทียบ Boy กับ Jojo

# ทำ ranking ทุกคน
/sports-analyst ranking สมาชิกทั้ง 20 คน
```

### Output Location
```
resources/tournaments-reports/
```

| Content | Filename |
|---|---|
| Tournament | `tournament-monthly-2026-02-25.md` |
| Personal | `personal-gio-2026-02-25.md` |
| Recap | `recap-weekly-2026-02-25.md` |
| Custom | `custom-boy-vs-jojo-2026-02-25.md` |

---

## 📚 Shared Skill: NotebookLM Research

ทุก agent สามารถค้นคว้าข้อมูลการแข่งขันจาก [NotebookLM Knowledge Base](https://notebooklm.google.com/notebook/b1637cb3-37a1-4cdf-8f55-36b8ae810a9a) ได้

### Example Queries

| Agent | Query |
|---|---|
| Coach Assistant | "กฎการนับระยะทาง Run กับ Walk" |
| Running Coach | "แผนฝึก Running Plan สำหรับมือใหม่" |
| Sports Analyst | "สถิติการแข่งขันเดือนที่แล้ว" |

---

## 🧠 Shared Skill: Local Ollama (qwen3:8b)

ทุก agent สามารถใช้ Local LLM ผ่าน Ollama สำหรับ text processing โดยไม่ต้องใช้ API ภายนอก

| Config | Value |
|---|---|
| Base URL | `http://localhost:11434/` |
| Model | `qwen3:8b` |
| .env vars | `OLLAMA_BASE_URL`, `OLLAMA_MODEL` |

### Use Cases
| Agent | Use Case |
|---|---|
| Coach Assistant | Validate activity type (run/walk), parse Thai dates |
| Running Coach | Workout analysis, motivation text, plan suggestions |
| Sports Analyst | Summarize stats, generate captions, trend analysis |
| Tournament Reporter | LINE messages, Facebook posts, personal shoutouts |

```bash
# Prerequisites
brew install ollama
ollama serve
ollama pull qwen3:8b
```


## 📣 Agent 4: Tournament Reporter (`/tournament-reporter`)

### Objective
นักข่าวกีฬาประจำ tournament — สร้าง content สนุกสนาน กระตุ้นให้สมาชิกอยากวิ่ง ในหลาย format พร้อมแชร์

### Content Formats

| Format | Description |
|---|---|
| 📱 **LINE Message** | ข้อความสั้น กระชับ สำหรับ LINE group |
| 📘 **Facebook Post** | เล่าเรื่องราว dramatic สำหรับ social media |
| 🎨 **Infographic Content** | ข้อมูลพร้อมทำเป็นรูปภาพ |
| 🏅 **Personal Shoutout** | เชียร์รายบุคคล — ทั้งฉลองและกระตุ้น |
| 📊 **Standings Board** | กระดานคะแนนสำหรับ screenshot แชร์ |

### How to Use

```
# สรุปสัปดาห์แบบ LINE message
/tournament-reporter เขียนสรุปสัปดาห์นี้แบบ LINE message

# โพสต์ Facebook ประจำเดือน
/tournament-reporter เขียน Facebook post สรุปเดือน February

# เชียร์คนที่ห่างหาย
/tournament-reporter เขียน motivation ให้ Tae กับ Peck กลับมาวิ่ง

# กระดานคะแนนล่าสุด
/tournament-reporter ทำ standings board
```

### Output Location
```
resources/tournaments-reports/
```

| Format | Filename |
|---|---|
| LINE | `line-weekly-2026-02-25.md` |
| Facebook | `facebook-monthly-2026-02-25.md` |
| Infographic | `infographic-weekly-2026-02-25.md` |
| Shoutout | `shoutout-ton-2026-02-25.md` |
| Standings | `standings-2026-02-25.md` |

---

## 📋 Common Workflows

### Workflow 1: สมาชิกส่งหลักฐานใหม่
```
1. /process-image → rename + update stats
2. /running-coach → วิเคราะห์ผลวิ่ง + คำแนะนำ
```

### Workflow 2: สรุปผลประจำสัปดาห์
```
1. /sports-analyst → สรุปสัปดาห์ + MVP
2. แชร์ใน LINE group
```

### Workflow 3: สมาชิกใหม่ / สร้างแผนฝึก
```
1. /running-coach → สร้าง personal-statistics.md + running-plan.md
2. /sports-analyst → ทำ personal stats card
```

### Workflow 4: End of Quarter
```
1. /process-image → สรุปผล tournament
2. /sports-analyst → ทำ infographic ไตรมาส
```

---

## 🔗 Related Documents

- [Tournament Rules](tournaments/Tournament%20Rules.md)
- [Team Member List](tournaments/Team%20member%20list.md)
- [Tournament Calendar](tournaments/Tournament%20Calendar.md)
- [End-to-End Workflow](End-to-End%20Workflow.md)

---
*Last updated: 2026-02-25*
