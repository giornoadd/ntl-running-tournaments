# Technical Architecture

This document describes the technical architecture and pipeline logic of the **Running Competition 2026** project.

## 1. Core Architecture Pattern: "Filesystem-as-Source-of-Truth"

The project fundamentally relies on the files and directories themselves to represent the current state of the competition. 
Instead of a traditional relational database, we use standard file formats (Markdown, CSV) organized in a strict hierarchy.

### Why this pattern?
- **AI-Agent Friendly**: Agents can natively read, parse, and write Markdown/CSV using standard tooling without database connectors.
- **Git-Trackable**: Every run, statistic update, and infographic is trackable through standard version control.
- **Human-Readable**: Participants can browse the repository locally or on GitHub/GitLab and immediately understand the data.

## 2. The Data Pipeline (`src/run_all.py`)

The end-to-end pipeline handles the ingestion of runner evidence (screenshots) through to final statistical calculation.

### Pipeline Stages

1. **Ingestion & Normalization (`src/reformat_files.py`)**
   - Scans `member_results/*/running-pics/` for new image files.
   - Using AI Vision (via Gemini API in `analyze_with_gemini.py` or local Ollama), extracts the `date`, `distance`, and `activity type`.
   - Renames the file to the strict standard: `{nickname}-{yyyy}-{mon}-{dd}.{ext}`.

2. **Watermarking (`src/add_date_watermark.py` & `src/add_name_watermark.py`)**
   - Applies automated text overlays to the evidence images.
   - Prevents duplicate usage of the same image across different days or different members.

3. **Aggregation (`src/recalculate_csv.py`)**
   - Reads the newly curated images/data.
   - Cross-references distances against the rules (`activity_types.json` for walk vs run minimums).
   - Updates the monthly aggregation tables in `results/{yyyy}-{Month}.csv`.
   - Regenerates the overarching `results/README.md` leaderboard.

4. **Profile Generation (`src/generate_member_readmes.py`)**
   - Aggregates the individual statistics for each runner.
   - Regenerates the `member_results/*/README.md` files to reflect their active tracking, current pace, and contribution percentages.

5. **Coach Analysis Generation (`src/generate_coach_analysis.py`)**
   - Parses `personal-statistics.md` for all 20 members.
   - Creates `performance-report/personal-performance-report.md` with: Stats Card, Achievement Badges, Distance & Pace Evolution, HR/Cadence trends, PR Timeline, Coach Recommendations.
   - Also writes `coach-analysis.md` at member root for website data pipeline.

6. **Website Deployment (`scripts/deploy_website.sh`)**
   - Generates `data.js` from CSV → converts to `data.json` + per-roster JSON files.
   - Copies markdown files from `member_results/` into `assets_data/` for the React app.
   - Builds React app (TypeScript + Vite) → deploys to `docs/html/`.
   - The React dashboard reads all data dynamically including Coach Analysis tab.

## 3. Technology Stack

- **Core Engine**: Python 3.10+
- **Image Processing**: Pillow (`PIL`)
- **AI/Vision**: `google-generativeai` (Gemini Pro Vision) for reliable OCR and contextual data extraction.
- **Data Persistence**: CSV (`csv` module) and Markdown (`markdown` construction).
- **Frontend**: React 19 + TypeScript + Vite 7, deployed via GitHub Pages.
- **Agent System**: Uses standard markdown-based workflow definitions (`.agents/workflows/`) triggered via IDE extensions or CLI bots. Features advanced integrations like the Google Python Interpreter for autonomous infographic generation.
