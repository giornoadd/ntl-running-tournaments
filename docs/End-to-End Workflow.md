# End-to-End Workflow: Running Competition

This document outlines the operational process of ingesting runner's evidence screenshots, standardizing the data, and generating the competition statistics (`results/yyyy-month.csv`).

---

## 📸 1. Evidence Submission

Participants send their running/walking screenshots via the LINE group.
Save these images into the respective member's folder under the `member_results/` directory.

> [!NOTE]
> **Example Import Path:** `member_results/ITSystem-3_O (โอ)/IMG_1234.jpg`

---

## 🪄 2. Automated Processing (Recommended)

After adding screenshots to `member_results/`, execute the unified master script. This heavily automated script sequentially reformats files, applies watermarks, and recalculates the continuous CSV standings.

```bash
python3 src/run_all.py
```

---

## ⚙️ 3. Manual Processing Tools (Under the Hood)

If you need to manually perform the End-to-End process step by step, follow the sequential commands below:

### A. Format and Standardize Filenames
Ensure all files are uniformly tracked by using the `reformat_files.py` script.
This script attempts to parse the date from the filename or EXIF metadata and renames it to `[nickname]-[yyyy]-[mon]-[dd].jpg`.

```bash
python3 src/reformat_files.py --dir "member_results"
```
> [!TIP]
> You can pass `--folder "[Name]"` to process only a specific person's folder instead of the entire directory, and optionally `--ocr` to search the image content for a date.

### B. Apply Watermarks
For proper crediting and historical tracking, apply Date and Owner Name watermarks to the explicitly renamed screenshots.

```bash
# Add Date watermark to the bottom-right
python3 src/add_date_watermark.py

# Add Owner Name watermark to the bottom-center 
python3 src/add_name_watermark.py
```

### C. Distance Extraction (OCR via Gemini)
If the images contain dates but you need to rely on AI for distance validation, execute the `analyze_with_gemini.py` script.

```bash
python3 src/analyze_with_gemini.py --dir "member_results"
```
> [!WARNING]
> Ensure that the `GEMINI_API_KEY` is exported in your environment variables prior to running this step.

### D. Recalculate Statistics
The competition enforces strict distance rules: **Runs >= 1km** and **Walks >= 2km**. 
Once raw distances are logged into the `results/yyyy-month.csv` files, you must run the recalculation script. 

```bash
python3 src/recalculate_csv.py
```

This script:
1. Validates distances strictly against the `1km`/`2km` minimum criteria.
2. Moves disqualified runs to the "Invalid (ผิดกติกา)" column.
3. Automatically computes the Daily and Accumulated statistical averages across the active months.

### E. Generate Member READMEs
After recalculating the CSVs, generate individual member profile pages with stats, monthly breakdowns, and linked evidence screenshots.

```bash
python3 src/generate_member_readmes.py
```

This script:
1. Parses all `results/yyyy-month.csv` files to extract each member's activities.
2. Links available evidence images from the member's `member_results/` folder.
3. Generates a README.md per member with all-time summary, monthly tables, and image links.
