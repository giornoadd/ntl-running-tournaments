---
name: NotebookLM Research
description: Query the Running Competition 2026 knowledge base via NotebookLM MCP to research rules, history, strategies, and competition data.
---

# 📚 NotebookLM Research Skill

This skill allows any agent to research competition data from the centralized **NotebookLM knowledge base** via MCP tools.

## Notebook Info

| Field | Value |
|---|---|
| **Notebook ID** | `b1637cb3-37a1-4cdf-8f55-36b8ae810a9a` |
| **URL** | https://notebooklm.google.com/notebook/b1637cb3-37a1-4cdf-8f55-36b8ae810a9a |
| **Contains** | Tournament rules, team member profiles, competition history, training resources |

---

## How to Use

### 1. Query the Knowledge Base

Use `mcp_notebooklm_notebook_query` to ask questions about competition data:

```
Tool: mcp_notebooklm_notebook_query
Arguments:
  notebook_id: "b1637cb3-37a1-4cdf-8f55-36b8ae810a9a"
  query: "กฎการแข่งขันวิ่งเรื่องระยะทางขั้นต่ำ"
```

### 2. Get Notebook Summary

Use `mcp_notebooklm_notebook_describe` for an AI-generated overview:

```
Tool: mcp_notebooklm_notebook_describe
Arguments:
  notebook_id: "b1637cb3-37a1-4cdf-8f55-36b8ae810a9a"
```

### 3. List Sources

Use `mcp_notebooklm_notebook_get` to see what documents are in the notebook:

```
Tool: mcp_notebooklm_notebook_get
Arguments:
  notebook_id: "b1637cb3-37a1-4cdf-8f55-36b8ae810a9a"
```

### 4. Read a Specific Source

After getting source IDs from step 3, read the full content:

```
Tool: mcp_notebooklm_source_get_content
Arguments:
  source_id: "{source_id from notebook_get}"
```

### 5. Get AI Summary of a Source

```
Tool: mcp_notebooklm_source_describe
Arguments:
  source_id: "{source_id}"
```

---

## Common Research Queries

Use these as starting points for each agent role:

### 🏟️ Coach Assistant (process-image)
| Query | Purpose |
|---|---|
| "กฎการนับระยะทาง Run กับ Walk ต่างกันไหม" | Validate distance thresholds |
| "การคำนวณคะแนนทีมทำยังไง" | Understand team scoring |
| "ไตรมาสไหนแข่งอะไรบ้าง" | Quarterly schedule |
| "กติกาเรื่องหลักฐานภาพ" | Evidence requirements |

### 🏃 Running Coach (running-coach)
| Query | Purpose |
|---|---|
| "แผนฝึกซ้อม Half Marathon สำหรับมือใหม่" | Training plan references |
| "เทคนิค Walk-Run Interval" | Coaching methodology |
| "วิธีป้องกันการบาดเจ็บสำหรับนักวิ่งมือใหม่" | Injury prevention |
| "โภชนาการสำหรับนักวิ่ง" | Nutrition advice |
| "การฝึก Pace ให้คงที่" | Pace training techniques |

### 📈 Sports Analyst (sports-analyst)
| Query | Purpose |
|---|---|
| "สถิติการแข่งขันเดือนที่แล้ว" | Historical data for comparison |
| "สมาชิกทีมไหนวิ่งเยอะสุด" | Top performer research |
| "แนวโน้มผลการแข่งขัน" | Trend analysis |
| "เปรียบเทียบผลงาน 2 ทีม" | Team comparison data |

---

### 📣 Tournament Reporter (tournament-reporter)
| Query | Purpose |
|---|---|
| "ไฮไลท์การแข่งขันสัปดาห์นี้" | Content for weekly recap |
| "สมาชิกที่ยังไม่เคยวิ่ง" | Motivation shoutout targets |
| "ความสำเร็จที่น่าสนใจ" | Achievement highlights |
| "เปรียบเทียบ 2 ทีมเชิงสถิติ" | Drama narrative data |

---

## 📝 Conversation Logging (MANDATORY)

> [!IMPORTANT]
> **ทุกครั้ง** ที่ใช้ NotebookLM query, search, หรือ add source ต้อง **log ไว้เสมอ**

### Log Directory
```
resources/notebooklm-log/
```

### Log Filename Convention
```
{agent}-{yyyy-mm-dd}.md
```

| Agent | Filename Example |
|---|---|
| Coach Assistant | `process-image-2026-02-25.md` |
| Running Coach | `running-coach-2026-02-25.md` |
| Sports Analyst | `sports-analyst-2026-02-25.md` |
| Tournament Reporter | `tournament-reporter-2026-02-25.md` |

### Log Format

Each log file is **append-only**. If the file already exists for today, append to it. If not, create a new one.

```markdown
# 📝 NotebookLM Log — {Agent Name}
📅 Date: {yyyy-mm-dd}

---

## [{HH:MM}] Query
**Tool:** notebook_query
**Query:** {the question asked}
**Response Summary:** {brief summary of the answer received}
**Used For:** {what the agent used this info for}

---

## [{HH:MM}] Add Source
**Tool:** notebook_add_text
**Title:** {source title}
**Content Preview:** {first 100 chars}
**Reason:** {why this was added}

---

## [{HH:MM}] Research
**Tool:** research_start
**Query:** {search query}
**Mode:** fast/deep
**Sources Found:** {N}
**Imported:** {N} sources
```

### Rules
1. **Always log** — no exceptions. Every NotebookLM tool call gets logged.
2. **Append, don't overwrite** — multiple entries per day in the same file.
3. **Include timestamps** — use `[HH:MM]` format from the current time.
4. **Summarize responses** — don't paste full responses, write a brief summary.
5. **Note the purpose** — explain what the info was used for (context for future reference).

### Logging Procedure

After every NotebookLM tool call:

1. Check if `resources/notebooklm-log/{agent}-{yyyy-mm-dd}.md` exists.
2. If **yes** → append a new `## [{HH:MM}]` section.
3. If **no** → create the file with the header and the first entry.

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Authentication error | Run `notebooklm-mcp-auth` in terminal |
| Query timeout | Set `timeout: 180` in the query call |
| Empty results | Try rephrasing the query or check if sources exist with `notebook_get` |

