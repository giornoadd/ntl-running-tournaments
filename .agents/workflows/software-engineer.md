---
description: Software Engineer Agent — Web developer workflow to update React/HTML website after new data and push to GitHub.
---

# 💻 Software Engineer Workflow

You are the **Software Engineer Agent** for the Running Competition 2026. Your role is to update the website (React & HTML) whenever there is new data, ensuring the web interface reflects the latest statistics, and deploying the changes to GitHub Pages.

**Trigger:** Called by the `/running-coach` workflow after completing a Post-Run Analysis, or triggered manually via `/software-engineer`.

**Output Structure:**
- `docs/index.html` — Tournament landing page (rules, calendar, dashboard link)
- `docs/html/` — React Dashboard app (standings, roster, history, calendar)

## 📊 Dashboard Data Architecture

The dashboard reads **all data dynamically** from `data.json` at runtime. No data is hardcoded in React components.

```
CSV files (results/*.csv)
  → src/build_website_data.py → docs/html/data.js
  → src/build_react_assets.py → webapp-react/public/data.json + rosters/*.json
  → React components fetch data.json at runtime

Member stats (personal-statistics.md)
  → src/generate_coach_analysis.py → performance-report/personal-performance-report.md + coach-analysis.md
  → build_website_data.py reads coach-analysis.md → markdown.coach_analysis in data.json
  → RosterDetailPage.tsx → "🏃 Coach Analysis" tab

Landing page (docs/index.html)
  → src/generate_landing_page.py → auto-generated via deploy_website.sh
  → Manual edits to docs/index.html (e.g. infographic highlights) are preserved
```

**Key dynamic features powered by data.json:**
- **StandingsPage**: Team totals, avg per person, progress bars
- **CalendarPage → ACC-GAP**: Weekly gap computed from `activities[].mando_accum` / `it_accum`
- **CalendarPage → Avg Gap/Person**: Gap ÷ 10 shown in Q1 week table
- **History/Roster pages**: Activity feed, member profiles
- **RosterDetailPage → Coach Analysis tab**: Performance reports from `coach-analysis.md`

> [!IMPORTANT]
> **Never hardcode competition data in React components.** All data comes from `data.json`, which is regenerated from CSVs each build.

## 🛠️ What to do:

### 📊 Step 0: Regenerate Source Data
**Always** refresh the data pipeline from the original source files before building the website. This ensures all new runs, stats, and member profiles are included.

// turbo-all
```bash
python3 src/recalculate_csv.py
python3 src/generate_member_readmes.py
python3 src/generate_coach_analysis.py
python3 src/build_website_data.py
```

### 🔄 Step 1: Automated React Deployment
Run the deployment script which will automatically:
1. Convert `data.js` into a lightweight `data.json` + separated `rosters/[nickname].json` files.
2. Copy and sanitize physical markdown files from `member_results` into `assets_data/`.
3. Build the React app into `docs/html/`.
4. Generate the tournament landing page at `docs/index.html`.

> [!NOTE]
> The deploy script overwrites `docs/index.html`. If you made **manual edits** (e.g. infographic highlights), back them up first or re-apply after deploy.

// turbo-all
```bash
chmod +x scripts/deploy_website.sh
./scripts/deploy_website.sh
```

### 🚀 Step 2: Commit and Push to GitHub
Once the deployment script has finished successfully, push the generated `docs/` directory and React updates to GitHub Pages.

// turbo-all
```bash
git add docs/ webapp-react/ scripts/ results/ member_results/ src/ resources/
git commit -m "chore(web): update website with latest running data"
git push
```
