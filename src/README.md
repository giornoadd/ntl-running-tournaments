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
| — | **`run_all.py`** | Master pipeline — runs Steps 1→2→3→5→6 in sequence |

## Supporting Files

- **`activity_types.json`** — OCR-verified activity types per member (default + per-date overrides)
- **`utils/`** — Shared modules: `config.py`, `dates.py`, `files.py`, `image.py`, `ocr.py`

## Usage

```bash
# Full pipeline (recommended)
python3 src/run_all.py

# Individual scripts
python3 src/recalculate_csv.py
python3 src/generate_member_readmes.py
```
