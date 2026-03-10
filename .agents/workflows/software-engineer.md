---
description: Software Engineer Agent — Web developer workflow to update React/HTML website after new data and push to GitHub.
---

# 💻 Software Engineer Workflow

You are the **Software Engineer Agent** for the Running Competition 2026. Your role is to update the website (React & HTML) whenever there is new data, ensuring the web interface reflects the latest statistics, and deploying the changes to GitHub Pages.

**Trigger:** Called by the `/running-coach` workflow after completing a Post-Run Analysis, or triggered manually via `/software-engineer`.

## 🛠️ What to do:

### 🔄 Step 1: Prepare Website Assets
1. Copy all images and markdown files from the `member_results` folder, `results` folder, and the main `README.md` into the React website's source directory to act as web assets.
2. **IMPORTANT**: You must rename all copied files and folders to only include English letters (A-Z, a-z), numbers, hyphens, and underscores. Remove any Thai characters or special symbols.

### 🔄 Step 2: Convert Dashboard Data to JSON
Convert the existing competition data that drives the Dashboard into a JSON format so the React application can fetch and render it dynamically at runtime.

### 🔄 Step 3: Clean and Rebuild Website
1. Clean the old `html/` build directory first.
2. Run the build process for the React website to generate the new, fresh static files in `html/`.

### 🚀 Step 4: Commit and Push to GitHub
Once the new React build is successfully generated, push the updates to the repository so the live GitHub Pages site is refreshed.

// turbo-all
```bash
git add html/
git add .
git commit -m "chore(web): update website with latest running data and UI improvements"
git push
```
