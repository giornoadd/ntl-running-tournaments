# Running Competition 2026 (Mandalorian vs IT System)

## Project Overview
This project manages the 2026 Running Competition between the Mandalorian and IT System teams. It automates the tracking, renaming, and reporting of running statistics provided by team members via screenshots.

**Goal**: Foster team engagement and health through a friendly quarterly competition.

## Directory Structure
- **`/docs`**: Project rules and participant lists.
  - [Rule Book](docs/Tournament%20Rules.md)
  - [Team Member List](docs/Team%20member%20list.md)
  - [Process Workflow](docs/End-to-End%20Workflow.md)
- **`/member_results`**: Directory containing subfolders for each participant, storing their evidence files (screenshots).
- **`/src`**: Python automation scripts for end-to-end processing.
  - `run_all.py`: Unified End-to-End runner script.
  - `reformat_files.py`: Renames evidence files to a standard format (`nickname-dd-mon-yyyy.jpg`).
  - `add_date_watermark.py`: Adds date watermarks to screenshots lacking clear dates.
  - `add_name_watermark.py`: Adds owner name watermarks to the bottom center of screenshots.
  - `analyze_with_gemini.py`: Uses extensive AI analysis for OCR distance extraction.
  - `recalculate_csv.py`: Applies distance rules and regenerates CSV statistics.
- **`/scripts`**: Contains archived and miscellaneous standalone utilities.

## Key Workflows

### 1. Evidence Submission & Renaming
Members upload screenshots to their respective folders in `member_results`.
To standardize filenames:
```bash
python3 src/run_all.py
```

### 2. Watermarking Evidence
After renaming, optionally add watermarks for proper crediting:
```bash
python3 src/add_date_watermark.py
python3 src/add_name_watermark.py
```

### 3. Competition Rules
- **Minimum Distance**: Run 1km, Walk 2km.
- **Scoring**: 
  - **Team**: Average Distance.
  - **Individual**: Total Distance.
- **Frequency**: Quarterly (Q1-Q4).

## Status
- **Current Quarter**: Q1 (Jan - Mar)
- **Status**: Active
