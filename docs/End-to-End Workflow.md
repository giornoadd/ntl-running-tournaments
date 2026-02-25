# End-to-End Workflow: Running Competition

This document outlines the operational process of ingesting runner's evidence screenshots, standardizing the data, and generating the competition statistics.

---

## 🤖 AI Agent Workflows (Recommended)

The tournament uses **3 AI agents** that automate most operations. Use these slash commands:

| Agent | Command | Use When |
| :--- | :--- | :--- |
| 🏟️ Coach Assistant | `/process-image` | New screenshot arrives — auto rename, extract data, update CSV |
| 🏃 Running Coach | `/running-coach` | Analyze a member's run, set goals, create training plans |
| 📈 Sports Analyst | `/sports-analyst` | Generate infographics, weekly recaps, personal stats cards |

### Typical Flow (Single Image):
```
1. Drop screenshot into member_results/{Folder}/
2. /process-image → Agent renames, extracts stats, updates CSV
3. /running-coach → Agent analyzes the run and gives feedback
```

### All agents can research via the [NotebookLM Knowledge Base](https://notebooklm.google.com/notebook/b1637cb3-37a1-4cdf-8f55-36b8ae810a9a).

---

## 📸 1. Evidence Submission

Participants send their running/walking screenshots via the LINE group.
Save these images into the respective member's folder under `member_results/`.

> [!NOTE]
> **Example Import Path:** `member_results/ITSystem-3_O (โอ)/IMG_1234.jpg`

---

## 🪄 2. Automated Processing (Full Batch)

After adding screenshots to `member_results/`, execute the master pipeline. This sequentially reformats files, applies watermarks, and recalculates all CSV standings.

```bash
python3 src/run_all.py
```

> [!WARNING]
> This re-watermarks ALL ~160+ images and can be slow. For processing **single files**, use the `/process-image` agent workflow instead.

---

## ⚙️ 3. Manual Processing Tools (Under the Hood)

If you need to manually perform the End-to-End process step by step:

### A. Format and Standardize Filenames
```bash
python3 src/reformat_files.py --dir "member_results"
```
> [!TIP]
> Pass `--folder "[Name]"` to process only a specific person. Add `--ocr` to search image content for dates.

### B. Apply Watermarks
```bash
# Add Date watermark to the bottom-right
python3 src/add_date_watermark.py

# Add Owner Name watermark to the bottom-center 
python3 src/add_name_watermark.py
```

### C. Distance Extraction (OCR via Gemini)
```bash
python3 src/analyze_with_gemini.py --dir "member_results"
```
> [!WARNING]
> Requires `GEMINI_API_KEY` in environment variables.

### D. Recalculate Statistics
```bash
python3 src/recalculate_csv.py
```

This script:
1. Validates distances: **Runs ≥ 1km**, **Walks ≥ 2km**.
2. Moves disqualified entries to "Invalid (ผิดกติกา)" column.
3. Computes Daily and Accumulated averages across all months.
4. Regenerates `results/README.md` with tournament standings.

### E. Generate Member READMEs
```bash
python3 src/generate_member_readmes.py
```

This script:
1. Parses all `results/yyyy-month.csv` files for each member's activities.
2. Links evidence images from `member_results/` folders.
3. Generates a `README.md` per member with all-time summary and monthly tables.

---

## 📂 Output Locations

| Output | Path |
|---|---|
| Monthly CSV stats | `results/{yyyy}-{Month}.csv` |
| Monthly MD tables | `results/{yyyy}-{Month}.md` |
| Tournament dashboard | `results/README.md` |
| Member profiles | `member_results/{Folder}/README.md` |
| Personal stats | `member_results/{Folder}/personal-statistics.md` |
| HM training plans | `member_results/{Folder}/Half_Marathon_Plan.md` |
| Infographic reports | `resources/tournaments-reports/` |

---
*Last updated: 2026-02-25*
