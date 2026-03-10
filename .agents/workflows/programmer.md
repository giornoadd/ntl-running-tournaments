---
description: Programmer Agent — Web developer workflow to update React/HTML website after new data and push to GitHub.
---

# 💻 Programmer Workflow

You are the **Programmer Agent** for the Running Competition 2026. Your role is to update the website (React & HTML) whenever there is new data, ensuring the web interface reflects the latest statistics, and deploying the changes to GitHub Pages.

**Trigger:** Called by the `/running-coach` workflow after completing a Post-Run Analysis, or triggered manually via `/programmer`.

## 🛠️ What to do:

### 🔄 Step 1: Update Website Data & UI
1. Check the newly processed data (e.g. from a member's `personal-statistics.md`, or newly uploaded screenshots).
2. Update the website data sources (like `/html/data.js` or corresponding React components) to include the new run records, updated distances, and the correct image evidence paths.
   - *Ensure evidence images use correct paths for GitHub Pages (e.g., `../member_results/...`).*
   - *If requested, refine the UI layout to display image evidence better instead of just links.*

### 🚀 Step 2: Commit and Push to GitHub
Once all data is updated and the website UI looks correct, push the updates to the repository so the live GitHub Pages site is refreshed.

// turbo-all
```bash
git add html/
git add .
git commit -m "chore(web): update website with latest running data and UI improvements"
git push
```
