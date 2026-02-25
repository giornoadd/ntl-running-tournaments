# Running Competition Scripts

This directory contains the core automation Python scripts for the **Running Competition 2026**.

## Active Scripts

These scripts align directly with the steps in [`docs/End-to-End Workflow.md`](../docs/End-to-End%20Workflow.md):

| # | Script | Description |
|---|--------|-------------|
| 1 | **`reformat_files.py`** | Standardizes evidence filenames to `{nickname}-{yyyy}-{mon}-{dd}.{ext}` |
| 2 | **`add_date_watermark.py`** | Adds date watermark to bottom-right corner |
| 3 | **`add_name_watermark.py`** | Adds runner's nickname watermark to bottom-center |
| 4 | **`analyze_with_gemini.py`** | AI-powered OCR to extract dates and distances (requires `GEMINI_API_KEY`) |
| 5 | **`recalculate_csv.py`** | Validates distances (Run ≥ 1km, Walk ≥ 2km), recalculates team statistics, and generates `results/README.md` |
| 6 | **`generate_member_readmes.py`** | Generates individual member README profiles with stats and image links |
| — | **`run_all.py`** | Master pipeline — runs Steps 1→2→3→5→6→7 in sequence |

## Scripts (`scripts/`)

Utility scripts not part of the main pipeline:

| Script | Description |
|--------|-------------|
| **`check_duplicates.py`** | Detects duplicate entries in CSVs (same person same day, or same exact distance) |
| **`upload_to_drive.py`** | Uploads docs/, results/, member_results/, resources/ to Google Drive |
| **`check_duplicates_files.py`** | Detects duplicate evidence files by filename patterns |
| **`convert_csv_to_md.py`** | Converts CSV results to Markdown tables |
| **`recover_csv.py`** | Recovers corrupted CSV files from Markdown representations |

## Supporting Files

- **`activity_types.json`** — OCR-verified activity types per member (default + per-date overrides)
- **`utils/`** — Shared modules:
  - `config.py` — Central project paths, constants, .env loading, Ollama/Drive config
  - `dates.py` — Date parsing (Buddhist Era, filename, OCR formats)
  - `files.py` — Nickname extraction, image listing
  - `image.py` — Watermark rendering
  - `ocr.py` — Tesseract OCR preprocessing and text extraction

## Usage

### AI Agent Processing (Recommended)
```
/process-image    # Process a single screenshot
/running-coach    # Analyze runs, create training plans
/sports-analyst   # Generate infographics and recaps
/tournament-reporter  # Write news content
```

### Full Pipeline
```bash
python3 src/run_all.py
```

### Individual Scripts
```bash
python3 src/recalculate_csv.py         # Recalculate all CSVs + results/README.md
python3 src/generate_member_readmes.py  # Regenerate member profiles
python3 scripts/check_duplicates.py     # Check for duplicate entries
python3 scripts/upload_to_drive.py      # Upload to Google Drive
```

## Environment Variables

Configured via `.env` at project root:

```bash
GEMINI_API_KEY=your-api-key           # For Gemini Vision OCR
OLLAMA_BASE_URL=http://localhost:11434 # Local Ollama LLM
OLLAMA_MODEL=qwen3:8b                 # Ollama model name
GOOGLE_DRIVE_FOLDER_ID=1FHh...        # Target Drive folder
```
