# Running Competition 2026 (Mandalorian vs IT System)

## Project Overview
This project manages the 2026 Running Competition between the Mandalorian and IT System teams. It automates the tracking, renaming, and reporting of running statistics provided by team members via screenshots.

**Goal**: Foster team engagement and health through a friendly quarterly competition.

## Directory Structure
- **`/docs`**: Project rules, participant lists, and process documentation.
  - [Rule Book](docs/tournaments/Tournament%20Rules.md)
  - [Team Member List](docs/tournaments/Team%20member%20list.md)
  - [Tournament Calendar](docs/tournaments/Tournament%20Calendar.md)
  - [Process Workflow](docs/End-to-End%20Workflow.md)
  - [AI Agent System Guide](docs/AI%20Agent%20System.md)
- **`/member_results`**: Per-participant subfolders with evidence screenshots, individual READMEs, personal statistics, and running plans.
- **`/results`**: Monthly CSV/MD statistics and [quarterly standings](results/README.md).
- **`/resources`**: Output files from AI agents.
  - `/resources/tournaments-reports`: Infographics, recaps, and news content.
  - `/resources/notebooklm-log`: NotebookLM conversation logs per agent per day.
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
- **`/.agents`**: AI agent workflows and skills.
  - `workflows/process-image.md`: Coach Assistant Agent — file processing & tournament ops.
  - `workflows/running-coach.md`: Running Coach Agent — personal coaching & running plans.
  - `workflows/sports-analyst.md`: Sports Analyst Agent — infographic & data viz content.
  - `workflows/tournament-reporter.md`: Tournament Reporter Agent — news & engagement content.
  - `skills/notebooklm-research/SKILL.md`: Shared skill for querying NotebookLM knowledge base.
  - `skills/local-ollama/SKILL.md`: Shared skill for local LLM processing via Ollama (qwen3:8b).

## AI Agent System

Four AI agents manage tournament operations via slash commands:

| Agent | Command | Role |
|---|---|---|
| 🏟️ Coach Assistant | `/process-image` | Rename files, update CSV/stats, tournament operations |
| 🏃 Running Coach | `/running-coach` | Post-run analysis, goal setting, running plans |
| 📈 Sports Analyst | `/sports-analyst` | Infographic content, personal stats cards, recaps |
| 📣 Tournament Reporter | `/tournament-reporter` | News, LINE/Facebook posts, motivation & engagement |

**Shared Skill:** All agents can query the [NotebookLM Knowledge Base](https://notebooklm.google.com/notebook/b1637cb3-37a1-4cdf-8f55-36b8ae810a9a).

## Key Workflows

### 1. AI Agent Processing (Recommended)
```
/process-image    # Process a single screenshot
/running-coach    # Analyze runs, create training plans
/sports-analyst   # Generate infographics and recaps
/tournament-reporter  # Write news and motivation content
```

### 2. Full Pipeline (Batch)
```bash
python3 src/run_all.py
```
This executes: rename → watermark → recalculate → generate READMEs.

### 3. Individual Scripts
```bash
python3 src/recalculate_csv.py       # Recalculate all CSVs + results/README.md
python3 src/generate_member_readmes.py  # Regenerate member profiles
```

### 4. Competition Rules
- **Minimum Distance**: Run ≥ 1km, Walk ≥ 2km.
- **Scoring**:
  - **Team**: Average Distance (Total ÷ 10 members).
  - **Individual**: Total Distance.
- **Frequency**: Quarterly (Q1–Q4).
- **Accumulation**: Resets per year (tournament starts Jan 1).

## Status
- **Current Quarter**: Q1 (Jan – Mar 2026)
- **Status**: 🟢 Active (Week 9)
