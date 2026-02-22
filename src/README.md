# Running Competition Scripts

This directory contains the core automation python scripts utilized for the "Running Competition 2026" repository. 

## Active Scripts
These scripts align directly with the steps detailed in `docs/End-to-End Workflow.md`:

1. **`reformat_files.py`**: Searches through `member_results` and renames evidence images into the standardized format (`nickname-yyyy-mon-dd.jpg`).
2. **`add_date_watermark.py`**: Appends the extracted date to the bottom-right corner of the image for accountability.
3. **`add_name_watermark.py`**: Appends the runner's nickname to the bottom-center of the image for crediting.
4. **`analyze_with_gemini.py`**: Optionally performs Google Gemini Vision OCR to extract missing dates and exact distances (Requires `GEMINI_API_KEY`).
5. **`recalculate_csv.py`**: Applies rule logic (1km run, 2km walk minimum) to raw output and regenerates the metric averages and totals in `results/yyyy-month.csv` files.
6. **`run_all.py`**: The unified End-to-End runner script. Executes the standard pipeline in chronological order automatically after images are dropped in.

## Archived Scripts
Older scripts and one-off utilities from earlier repository phases have been relocated into the `archive/` folder to maintain cleanliness.
