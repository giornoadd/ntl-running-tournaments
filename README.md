# Running Competition 2026 🏃‍♂️

Welcome to the **Running Competition 2026** tracker!
This repository automates the tracking, watermarking, and continuous statistics reporting for the friendly inter-team running and step competition between the **Mandalorian** and **IT System** teams.

---

## 🏆 Live Standings — Q1 2026

> 📅 **Q1 Status:** 🟢 Active — Week 11 (8–14 Mar) | 3 weeks remaining  
> 📊 Data as of: **8 March 2026** | Source: [`results/README.md`](results/README.md)

### ⚔️ Team Battle

| Metric | 🪖 Mandalorian | 💻 IT System | Leader |
| :--- | ---: | ---: | :--- |
| **Total Distance (Q1)** | **556.94 km** | **631.45 km** | 💻 IT System |
| **Average / Person** | **55.69 km** | **63.14 km** | 💻 IT System |
| **Active Members** | 8/10 | 9/10 | 💻 IT System |

```
📊 Share of combined 1,188.39 km:
🪖 Manda  █████████░░░░░░░░░░░░░  46.9%
💻 IT     ███████████░░░░░░░░░░░  53.1%

🏅 IT System leads by +7.45 km/person
```

> Previous months: **Jan** — Manda: 208.94 km | IT: 245.88 km · **Feb** — Manda: 217.14 km | IT: 278.42 km · **Mar** — Manda: 130.86 km | IT: 107.15 km 🪖  
> 📋 [January](results/2026-January.md) · [February](results/2026-February.md) · [March](results/2026-March.md)

---

### 🌟 Top 5 Individual Runners — Q1 All-Time

| Rank | Name | Team | Total Distance | Active Days |
| :---: | :--- | :--- | ---: | :---: |
| 🥇 1 | **GIO** | 🪖 Mandalorian | **347.23 km** | 52 |
| 🥈 2 | **Jojo** | 💻 IT System | **192.78 km** | 37 |
| 🥉 3 | **O** | 💻 IT System | **144.91 km** | 22 |
| 🏅 4 | **Boy** | 💻 IT System | **111.92 km** | 18 |
| 🏅 5 | **Sand** | 🪖 Mandalorian | **70.25 km** | 22 |

📊 Full quarterly & monthly breakdowns → [`results/README.md`](results/README.md)

---

### 👥 Full Roster — Q1 2026

#### 🪖 Mandalorian

| Member | Distance | Active Days |
| :--- | ---: | :---: |
| GIO | 347.23 km | 52 |
| Sand | 70.25 km | 22 |
| Boat | 57.42 km | 9 |
| Chan | 41.23 km | 10 |
| EM | 30.37 km | 5 |
| Toro | 23.04 km | 5 |
| Mos | 20.74 km | 7 |
| Fuse | 12.76 km | 1 |
| Peck | 0.00 km | — |
| Neung | 0.00 km | — |
| **Total** | **603.04 km** | |

#### 💻 IT System

| Member | Distance | Active Days |
| :--- | ---: | :---: |
| Jojo | 192.78 km | 37 |
| O | 144.91 km | 22 |
| Boy | 111.92 km | 18 |
| Oat | 58.97 km | 11 |
| Palm | 55.64 km | 13 |
| Game | 44.89 km | 6 |
| Ton | 41.62 km | 16 |
| Oum | 16.70 km | 4 |
| PAN | 4.21 km | 2 |
| Tae | 0.00 km | — |
| **Total** | **671.64 km** | |

> ⚠️ Note: Roster distances include all sessions since member's first activity (including 2025). Team standings use 2026 Q1 CSV accumulation only.

---

## 📅 Tournament Calendar — Q1 2026

| Quarter | Period | Weeks | Status |
| :---: | :--- | :---: | :--- |
| **Q1** 🟢 | 1 Jan – 31 Mar 2026 | 13 | **In Progress (Week 10)** |
| **Q2** ⬜ | 1 Apr – 30 Jun 2026 | 13 | Upcoming |
| **Q3** ⬜ | 1 Jul – 30 Sep 2026 | 13 | Upcoming |
| **Q4** ⬜ | 1 Oct – 31 Dec 2026 | 13 | Upcoming |

**Q1 Remaining Weeks:**

| Week | Dates | Notes |
| :---: | :--- | :--- |
| 10 | 1 Mar – 7 Mar | |
| **11** | **8 Mar – 14 Mar** | 📍 **Current Week** |
| 12 | 15 Mar – 21 Mar | |
| 13 | 22 Mar – 28 Mar | |
| — | 29 Mar – 31 Mar | ⚡ Q1 Final Sprint! |

> ⚠️ **Q1 Deadline:** Submit all evidence by **31 March 2026, 23:59**  
> 📣 Q1 results & rewards announced in early April

---

## 📏 Competition Rules — Key Points

| Rule | Detail |
| :--- | :--- |
| **🏃 Run minimum** | ≥ 1.0 km per session |
| **🚶 Walk minimum** | ≥ 2.0 km per session |
| **📸 Submission** | Screenshot via LINE group within 24 hours |
| **🏆 Team Scoring** | Average Distance = Total ÷ 10 members |
| **🌟 Individual** | Top 5 by total accumulated distance |
| **📅 Reset** | Distance resets every quarter (Q1–Q4) |
| **❌ Prohibited** | Duplicate submissions, data tampering, micro-activities |

**Losing team penalties:** Sponsor lunch for winning team + wear funny costume + display "Declaration of Defeat" sign 🤡

📖 Full rules → [`docs/tournaments/Tournament Rules.md`](docs/tournaments/Tournament%20Rules.md)

---

## 🤖 AI Agent System

Four AI agents manage tournament operations via slash commands:

| Agent | Command | Role |
|---|---|---|
| 🏟️ Coach Assistant | `/coach-assistant` | Rename files, update CSV/stats, tournament ops |
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
   Drag & drop participant screenshots into their `running-pics/` subfolder under `member_results/`.

2. **Process with AI Agent (Recommended):**
   ```
   /coach-assistant
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
| `member_results/` | Per-member folders: `running-pics/` (evidence screenshots), READMEs, `personal-statistics.md`, `running-plan.md` |
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

---

*Last updated: 8 March 2026 — Auto-updated by Sports Analyst Agent*
