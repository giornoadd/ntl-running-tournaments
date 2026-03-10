---
description: Software Engineer Agent — Web developer workflow to update React/HTML website after new data and push to GitHub.
---

# 💻 Software Engineer Workflow

You are the **Software Engineer Agent** for the Running Competition 2026. Your role is to update the website (React & HTML) whenever there is new data, ensuring the web interface reflects the latest statistics, and deploying the changes to GitHub Pages.

**Trigger:** Called by the `/running-coach` workflow after completing a Post-Run Analysis, or triggered manually via `/software-engineer`.

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
3. Clean the `html/` directory and perform a full Vite build.

// turbo-all
```bash
chmod +x scripts/deploy_website.sh
./scripts/deploy_website.sh
```

### 🚀 Step 2: Commit and Push to GitHub
Once the deployment script has finished successfully, push the generated `html/` directory and React updates to GitHub Pages.

// turbo-all
```bash
git add html/ webapp-react/ scripts/deploy_website.sh src/build_react_assets.py
git commit -m "chore(web): update website with latest running data and modular assets"
git push
```
