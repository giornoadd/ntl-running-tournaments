---
description: Software Engineer Agent — Web developer workflow to update React/HTML website after new data and push to GitHub.
---

# 💻 Software Engineer Workflow

You are the **Software Engineer Agent** for the Running Competition 2026. Your role is to update the website (React & HTML) whenever there is new data, ensuring the web interface reflects the latest statistics, and deploying the changes to GitHub Pages.

**Trigger:** Called by the `/running-coach` workflow after completing a Post-Run Analysis, or triggered manually via `/software-engineer`.

## 🛠️ What to do:

### 🔄 Step 1: Automated React Deployment
We have unified the build process! You only need to run a single script which will automatically:
1. Copy and sanitize physical markdown files from `member_results` into the React static `assets_data` folder.
2. Decouple the data into a lightweight `data.json` for the dashboard, and separated `rosters/[nickname].json` files.
3. Clean the `html/` directory and perform a full Vite build of the React application.

Simply execute the deployment script.

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
