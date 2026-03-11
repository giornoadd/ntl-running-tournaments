---
description: Software Engineer Agent — Web developer workflow to update React/HTML website after new data and push to GitHub.
---

# 💻 Software Engineer Workflow

You are the **Software Engineer Agent** for the Running Competition 2026. Your role is to update the website (React & HTML) whenever there is new data, ensuring the web interface reflects the latest statistics, and deploying the changes to GitHub Pages.

**Trigger:** Called by the `/running-coach` workflow after completing a Post-Run Analysis, or triggered manually via `/software-engineer`.

**Output Structure:**
- `docs/index.html` — Tournament landing page (rules, calendar, dashboard link)
- `docs/html/` — React Dashboard app (standings, roster, history)

## 🛠️ What to do:

### 📊 Step 0: Regenerate Source Data
**Always** refresh the data pipeline from the original source files before building the website. This ensures all new runs, stats, and member profiles are included.

// turbo-all
```bash
python3 src/recalculate_csv.py
python3 src/generate_member_readmes.py
python3 src/build_website_data.py
```

### 🔄 Step 1: Automated React Deployment
Run the deployment script which will automatically:
1. Convert `data.js` into a lightweight `data.json` + separated `rosters/[nickname].json` files.
2. Copy and sanitize physical markdown files from `member_results` into `assets_data/`.
3. Build the React app into `docs/html/`.
4. Generate the tournament landing page at `docs/index.html`.

// turbo-all
```bash
chmod +x scripts/deploy_website.sh
./scripts/deploy_website.sh
```

### 🚀 Step 2: Commit and Push to GitHub
Once the deployment script has finished successfully, push the generated `docs/` directory and React updates to GitHub Pages.

// turbo-all
```bash
git add docs/ webapp-react/ scripts/ src/build_react_assets.py src/build_website_data.py src/generate_landing_page.py
git commit -m "chore(web): update website with latest running data"
git push
```
