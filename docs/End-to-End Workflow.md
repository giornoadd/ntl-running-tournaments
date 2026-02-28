# End-to-End Workflow: Running Competition

This document outlines the operational process of ingesting runner's evidence screenshots, standardizing the data, and generating the competition statistics.

---

## 🤖 AI Agent Workflows (Recommended)

The tournament uses **4 AI agents** that automate most operations. Use these slash commands:

| Agent | Command | Use When |
| :--- | :--- | :--- |
| 🏟️ Coach Assistant | `/coach-assistant` | New screenshot arrives — rename, extract data, update CSV + stats |
| 🏃 Running Coach | `/running-coach` | Analyze a member's run, set goals, create training plans |
| 📈 Sports Analyst | `/sports-analyst` | Generate infographics, weekly recaps, personal stats cards, update README |
| 📣 Tournament Reporter | `/tournament-reporter` | Write LINE/Facebook posts, standings boards, personal shoutouts |

All agents can research via the [NotebookLM Knowledge Base](https://notebooklm.google.com/notebook/b1637cb3-37a1-4cdf-8f55-36b8ae810a9a) and use the Local Ollama (qwen3:8b) skill for text processing.

---

## Typical Flows

### Single Image Submission:
```
1. Drop screenshot into member_results/{Folder}/running-pics/
2. /coach-assistant → Agent renames, extracts stats, updates CSV + personal-statistics.md
3. /running-coach   → Agent analyzes the run and gives feedback
```

### Weekly Update:
```
1. /sports-analyst       → Validate data + generate weekly recap + infographic
2. /tournament-reporter  → Write LINE message / standings board
3. Share in LINE group
```

### End of Quarter:
```
1. /coach-assistant      → Tournament summary + duplicate check
2. /sports-analyst       → Quarter infographic + update README
3. /tournament-reporter  → Write quarter recap post
4. /coach-assistant      → Google Drive sync
```

---

## 📸 1. Evidence Submission

Participants send their running/walking screenshots via the LINE group.
Save these images into the respective member's `running-pics/` subfolder under `member_results/`.

> [!NOTE]
> **Example Import Path:** `member_results/ITSystem-3_O (โอ)/running-pics/IMG_1234.jpg`

---

## 🪄 2. Automated Processing (Full Batch)

After adding screenshots to `member_results/{Folder}/running-pics/`, execute the master pipeline. This sequentially reformats files, applies watermarks, and recalculates all CSV standings.

```bash
python3 src/run_all.py
```

> [!WARNING]
> This re-watermarks ALL ~160+ images and can be slow. For processing **single files**, use the `/coach-assistant` agent workflow instead.

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
2. Parses `personal-statistics.md` for advanced metrics (pace, cadence, HR, run/walk breakdown).
3. Links evidence images from `member_results/` folders.
4. Generates a `README.md` per member with all-time summary and monthly tables.

### F. Check for Duplicates
```bash
python3 scripts/check_duplicates.py
```

This script checks for:
- Same person, same date, multiple entries (likely duplicate submission)
- Same person, exact same distance on different dates (possible copy/paste error)

### G. Sync to Google Drive
```bash
python3 scripts/upload_to_drive.py
```

Uploads all files from `docs/`, `results/`, `member_results/`, and `resources/` to the shared Drive folder.
- **Drive Folder:** [Running Competition 2026](https://drive.google.com/drive/folders/1FHh4VKxjO2zJF6Bx42UZgxv80cmpsEdG)

---

## 📂 Output Locations

| Output | Path |
|---|---|
| Monthly CSV stats | `results/{yyyy}-{Month}.csv` |
| Monthly MD tables | `results/{yyyy}-{Month}.md` |
| Tournament dashboard | `results/README.md` |
| Member profiles | `member_results/{Folder}/README.md` |
| Personal stats | `member_results/{Folder}/personal-statistics.md` |
| Running plans | `member_results/{Folder}/running-plan.md` |
| Evidence screenshots | `member_results/{Folder}/running-pics/` |
| Infographic reports | `resources/tournaments-reports/` |
| NotebookLM logs | `resources/notebooklm-log/` |

---
*Last updated: 2026-02-28*
