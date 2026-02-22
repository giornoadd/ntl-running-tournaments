# Running Competition 2026 (Mandalorian vs IT System)

## Project Overview
This project manages the 2026 Running Competition between the Mandalorian and IT System teams. It automates the tracking, renaming, and reporting of running statistics provided by team members via screenshots.

**Goal**: Foster team engagement and health through a friendly quarterly competition.

## Directory Structure
- **`/docs`**: Project rules, participant lists, and process documentation.
  - [Rule Book](docs/Tournament%20Rules.md)
  - [Team Member List](docs/Team%20member%20list.md)
  - [Tournament Calendar](docs/Tournament%20Calendar.md)
  - [Process Workflow](docs/End-to-End%20Workflow.md)
- **`/member_results`**: Per-participant subfolders with evidence screenshots and individual READMEs.
- **`/results`**: Monthly CSV/MD statistics and [quarterly standings](results/README.md).
- **`/src`**: [Python automation scripts](src/README.md) for E2E processing.
  - `run_all.py`: Master pipeline — runs Steps 1→2→3→5→6 in sequence.
  - `reformat_files.py`: Standardizes filenames to `{nickname}-{yyyy}-{mon}-{dd}.{ext}`.
  - `add_date_watermark.py`: Adds date watermarks to evidence screenshots.
  - `add_name_watermark.py`: Adds owner name watermarks to evidence screenshots.
  - `analyze_with_gemini.py`: AI-powered OCR for date/distance extraction (requires `GEMINI_API_KEY`).
  - `recalculate_csv.py`: Validates distances, recalculates team statistics per year, and generates `results/README.md`.
  - `generate_member_readmes.py`: Generates individual member README profiles with stats and image links.
  - `activity_types.json`: OCR-verified activity types per member (walk/run detection).
- **`/tests`**: 48 pytest tests covering config, dates, files, recalculation, and member READMEs.
- **`/scripts`**: Archived standalone utilities from earlier phases.

## Key Workflows

### 1. Full Pipeline (Recommended)
Drop screenshots into `member_results/` then run:
```bash
python3 src/run_all.py
```
This executes: rename → watermark → recalculate → generate READMEs.

### 2. Individual Scripts
```bash
python3 src/recalculate_csv.py       # Recalculate all CSVs + results/README.md
python3 src/generate_member_readmes.py  # Regenerate member profiles
```

### 3. Competition Rules
- **Minimum Distance**: Run ≥ 1km, Walk ≥ 2km.
- **Scoring**:
  - **Team**: Average Distance (Total ÷ 10 members).
  - **Individual**: Total Distance.
- **Frequency**: Quarterly (Q1–Q4).
- **Accumulation**: Resets per year (tournament starts Jan 1).

## Status
- **Current Quarter**: Q1 (Jan – Mar 2026)
- **Status**: 🟢 Active (Week 9)
