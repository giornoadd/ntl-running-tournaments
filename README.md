# Running Competition 2026 🏃‍♂️

Welcome to the **Running Competition 2026** tracker!
This repository automates the tracking, watermarking, and continuous statistics reporting for the friendly inter-team running and step competition between the **Mandalorian** and **IT System** teams.

## 🏆 Current Status
- **Quarter**: Q1 (Jan – Mar 2026)
- **Status**: 🟢 Active (Week 9)

### Live Standings

| Metric | 🪖 Mandalorian | 💻 IT System | Leader |
| :--- | ---: | ---: | :--- |
| **Total Distance** | 393.22 km | 481.20 km | 💻 IT System |
| **Average / Person** | 39.32 km | 48.12 km | 💻 IT System |

> IT System leads by **8.80 km/person** 🏆

### 🌟 Top 5 Individual Runners

| Rank | Name | Team | Distance |
| :---: | :--- | :--- | ---: |
| 🥇 1 | GIO | 🪖 Mandalorian | 241.35 km |
| 🥈 2 | Jojo | 💻 IT System | 151.09 km |
| 🥉 3 | O | 💻 IT System | 86.56 km |
| 🏅 4 | Boy | 💻 IT System | 84.46 km |
| 🏅 5 | Oat | 💻 IT System | 43.77 km |

📊 Full quarterly & monthly breakdowns → [`results/README.md`](results/README.md)

---

## 🤖 AI Agent System

Four AI agents manage tournament operations:

| Agent | Command | Role |
|---|---|---|
| 🏟️ Coach Assistant | `/process-image` | Rename files, update CSV/stats, tournament ops |
| 🏃 Running Coach | `/running-coach` | Post-run analysis, goal setting, running plans |
| 📈 Sports Analyst | `/sports-analyst` | Infographic content, personal stats cards, recaps |
| 📣 Tournament Reporter | `/tournament-reporter` | News, LINE/Facebook posts, motivation & engagement |

📚 All agents share a [NotebookLM Knowledge Base](https://notebooklm.google.com/notebook/b1637cb3-37a1-4cdf-8f55-36b8ae810a9a) for research.

👉 **[Full Agent Guide](docs/AI%20Agent%20System.md)**

---

## ⚙️ Project Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment (optional — for AI OCR only):**
   ```bash
   # .env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

---

## 🏃‍♀️ How To Use

The codebase relies on a **"Filesystem-as-Source-of-Truth"** model.

1. **Drop Evidence:**
   Drag & drop participant screenshots into their folder under `member_results/`.

2. **Process with AI Agent (Recommended):**
   ```
   /process-image
   ```
   The agent will automatically: rename → extract stats → update CSV → regenerate READMEs.

3. **Or run the full pipeline:**
   ```bash
   python3 src/run_all.py
   ```

---

## 📂 Directory Structure

| Directory | Purpose |
|-----------|---------|
| `docs/` | [Tournament Rules](docs/tournaments/Tournament%20Rules.md), [Team Members](docs/tournaments/Team%20member%20list.md), [Calendar](docs/tournaments/Tournament%20Calendar.md), [Workflow](docs/End-to-End%20Workflow.md), [Agent Guide](docs/AI%20Agent%20System.md) |
| `member_results/` | Per-member folders: evidence screenshots, READMEs, `personal-statistics.md`, `running-plan.md` |
| `results/` | Monthly CSV/MD statistics and [quarterly standings](results/README.md) |
| `resources/` | Agent output: [tournament reports](resources/tournaments-reports/), [NotebookLM logs](resources/notebooklm-log/) |
| `src/` | [Automation scripts](src/README.md) — pipeline, watermarking, recalculation, README generation |
| `.agents/` | AI agent [workflows](.agents/workflows/) and [skills](.agents/skills/) |
| `tests/` | 48 pytest tests covering config, dates, files, recalculation, and member READMEs |

---

## 📚 Documentation

For architecture details, tournament rules, and the full E2E pipeline, see:

👉 **[GEMINI.md](GEMINI.md)** — Project context for AI agents
👉 **[docs/](docs/README.md)** — Full documentation index
