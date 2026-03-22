---
description: Quick dashboard rebuild — regenerate data, build React app, deploy to GitHub Pages. Use /junior-swe for fast updates without full evidence processing.
---

# 🔄 Update Dashboard Workflow

**🤖 Agent Persona: Junior Software Engineer**
* **Role:** Dashboard Automation & Deployment Specialist. Responsible for executing rapid, lightweight updates to the live tournament dashboard after data modifications, bypassing the heavy processing pipelines.
* **Core Skills:**
    * **Data Processing:** Python (`recalculate_csv.py`, `build_website_data.py`)
    * **Frontend Build:** React, HTML/CSS generation
    * **Automation & Scripting:** Bash shell scripting (`deploy_website.sh`)
    * **Version Control & Hosting:** Git operations, GitHub Pages deployment

---

Quick-fire workflow to **rebuild and deploy the dashboard** after data changes. This is a lightweight alternative to `/senior-swe` — use it when CSVs or member data have already been updated and you just need to refresh the website.

**Trigger:** After any data update (CSV edits, manual fixes, stat corrections), or when you want to refresh the live dashboard without full evidence processing.

**When to use:**
| Situation | Use |
|---|---|
| Processed new evidence screenshots | `/running-coach` → auto-calls `/senior-swe` |
| Quick CSV fix or stat correction | ✅ `/junior-swe` |
| Recalculated data, need quick deploy | ✅ `/junior-swe` |
| Full pipeline with watermarks + READMEs | `/senior-swe` |

## 📊 What Gets Updated

The dashboard reads **all data dynamically** from `data.json`. Rebuilding refreshes:

| Dashboard Feature | Auto-Updated |
|---|---|
| **StandingsPage** — team totals, avg/person | ✅ |
| **CalendarPage → ACC-GAP** — weekly gap bar chart | ✅ |
| **CalendarPage → Avg Gap/Person** — gap column in Q1 table | ✅ |
| **History** — daily activity feed | ✅ |
| **Roster** — member profiles & images | ✅ |
| **Roster → Coach Analysis tab** — performance reports | ✅ |
| **Landing page** — tournament calendar + rules | ✅ |

## 🛠️ Steps

### Step 1: Recalculate & Regenerate Data

// turbo-all
```bash
python3 src/recalculate_csv.py
python3 src/generate_member_readmes.py
python3 src/generate_coach_analysis.py
python3 src/build_website_data.py
```

### Step 2: Build & Deploy

// turbo-all
```bash
chmod +x scripts/deploy_website.sh
./scripts/deploy_website.sh
```

### Step 3: Push to GitHub

// turbo-all
```bash
git add docs/ webapp-react/ results/ member_results/ resources/ src/
git commit -m "chore(dashboard): refresh data and rebuild"
git push
```

### Step 4: Verify (Optional)

Open the live dashboard in browser to confirm updates are reflected:
- Landing page: https://giornoadd.github.io/ntl-running-tournaments/
- Dashboard: https://giornoadd.github.io/ntl-running-tournaments/html/

## ✅ Done!

Dashboard is live at: https://giornoadd.github.io/ntl-running-tournaments/html/

| Page | URL |
|---|---|
| 🏠 Landing | `/ntl-running-tournaments/` |
| 🏆 Standings | `/ntl-running-tournaments/html/` |
| 👥 Roster | `/ntl-running-tournaments/html/roster` |
| 📜 History | `/ntl-running-tournaments/html/history` |
| 📅 Calendar + ACC-GAP | `/ntl-running-tournaments/html/calendar` |
