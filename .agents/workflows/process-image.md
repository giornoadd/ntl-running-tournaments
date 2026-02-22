---
description: Process incoming running competition evidence screenshots — identify owner, extract date & distance, rename, watermark, update CSV stats, and regenerate member READMEs.
---

# Process Running Competition Image

When a user provides an image file from `member_results/`, follow this workflow to process it.

---

## Step 1: Identify the Owner

Determine which team member the image belongs to based on the **parent folder name**.

**Folder format:** `{Team}-{ID}_{ThaiName} ({EnglishAlias})/`

| Folder Pattern | Alias (nickname) |
|---|---|
| `Manda-1_โจ (GIO)` | `gio` |
| `Manda-2_โบ๊ท (Boat)` | `boat` |
| `Manda-3_ต้อ (TORO)` | `toro` |
| `Manda-4_เอ็ม (EM)` | `em` |
| `Manda-5_แซนด์ (SAND)` | `sand` |
| `Manda-6_เป๊ก (peck)` | `peck` |
| `Manda-7_หนึ่ง (Neung)` | `neung` |
| `Manda-8_ฟิวส์ (fuse)` | `fuse` |
| `Manda-9_พี่ฉันท์ (Chan)` | `chan` |
| `Manda-10_มอส (Mos)` | `mos` |
| `ITSystem-1_Oat (โอ๊ต)` | `oat` |
| `ITSystem-2_Game (เกมส์)` | `game` |
| `ITSystem-3_O (โอ)` | `o` |
| `ITSystem-4_Palm (ปาล์ม)` | `palm` |
| `ITSystem-5_Oum (อุ้ม)` | `oum` |
| `ITSystem-6_Jojo (โจโจ้)` | `jojo` |
| `ITSystem-7_Tae (เต)` | `tae` |
| `ITSystem-8_Boy (บอย)` | `boy` |
| `ITSystem-9_Ton (ต้น)` | `ton` |
| `ITSystem-10_PAN (แพน)` | `pan` |

> The **nickname** is always the English alias in **lowercase**. Extract it from the folder name using the text inside parentheses `(...)` that contains English characters.

---

## Step 2: View the Image & Extract Information

Open the image using `view_file` and visually extract the following:

| Field | Where to Look |
|---|---|
| **Date** | Displayed on the screenshot (e.g. "October 17, 2025", "Jan 5, 2026", Thai date, or Buddhist Era date) |
| **Distance** | Usually shown prominently (e.g. "8.34 km") |
| **Activity Type** | Run or Walk (determines minimum distance threshold) |
| **Duration/Pace** | Optional but useful for context |

### Date Handling
- If the date uses **Buddhist Era (BE)** year (e.g., 2569), subtract 543 → AD year (2026).
- If the date says "Today" or "Yesterday", calculate the actual date from the file's context or ask the user.
- The date must be an **exact calendar date** — do not guess.

---

## Step 3: Rename the File

Rename the file to the standard format:

```
{nickname}-{yyyy}-{mon}-{dd}.{ext}
```

- `{nickname}` — lowercase alias from Step 1
- `{yyyy}` — 4-digit AD year
- `{mon}` — 3-letter lowercase month abbreviation: `jan`, `feb`, `mar`, `apr`, `may`, `jun`, `jul`, `aug`, `sep`, `oct`, `nov`, `dec`
- `{dd}` — 2-digit zero-padded day
- `{ext}` — original file extension in lowercase (e.g., `jpg`, `jpeg`, `png`)

**Examples:**
- `IMG_8764.JPG` → `gio-2025-oct-17.jpg`
- `Runna 5km Easy Run on Feb 9, 2026 - 04.59.17.JPEG` → `gio-2026-feb-09.jpeg`

### Collision Handling
If a file with the same name already exists in the folder, append `_1`, `_2`, etc.:
- `gio-2026-feb-07.jpg` (exists) → `gio-2026-feb-07_1.jpg`

### Rename Command
```bash
mv "member_results/{FolderName}/{original_filename}" "member_results/{FolderName}/{new_filename}"
```

---

## Step 4: Update the CSV

Manually add the extracted distance to the correct CSV file in `results/`.

### 4a: Determine the target CSV

The file is `results/{yyyy}-{Month}.csv` based on the date extracted in Step 2.
- Example: **Feb 22, 2026** → `results/2026-February.csv`
- If the file doesn't exist yet, create it with the header row (see existing CSVs for format).

### 4b: Add or update the entry

- If the **date row already exists**, append the new runner entry to the `Runners` column:
  - Before: `Boy: 6.31km`
  - After: `"Mos: 2.26km, Boy: 6.31km"`
- If the **date row doesn't exist**, add a new row at the correct chronological position:
  - Format: `{date},{Nickname}: {distance}km,,0,0,0,0,0,0`
  - The accumulation columns (0s) will be recalculated automatically in Step 5a.
- **Multiple entries same person same day**: combine distances into one entry (e.g. `GIO: 13.09km`), or list separately (e.g. `"GIO: 2.30km, GIO: 10.79km"`).

### 4c: Runner name format

Use the **capitalized display name** (not the lowercase nickname) in the CSV:
- `gio` → `GIO`, `boat` → `Boat`, `toro` → `Toro`, `em` → `EM`
- `sand` → `Sand`, `peck` → `Peck`, `neung` → `Neung`, `fuse` → `Fuse`
- `chan` → `Chan`, `mos` → `Mos`
- `oat` → `Oat`, `game` → `Game`, `o` → `O`, `palm` → `Palm`
- `oum` → `Oum`, `jojo` → `Jojo`, `tae` → `Tae`, `boy` → `Boy`
- `ton` → `Ton`, `pan` → `PAN`

---

## Step 5: Recalculate & Regenerate

After updating the CSV, run these two lightweight scripts (fast, ~1-2 seconds each):

### 5a: Recalculate statistics

// turbo
```bash
python3 src/recalculate_csv.py
```

This recalculates accumulations, averages, and generates MD tables + `results/README.md`.

### 5b: Generate Member READMEs

// turbo
```bash
python3 src/generate_member_readmes.py
```

This regenerates individual member profile pages with updated stats and image links.

> **Note:** Do NOT run `python3 src/run_all.py` for single-file processing. It re-watermarks ALL ~160+ images and is very slow. Use `run_all.py` only for batch processing (e.g., initial setup or processing many new files at once).

---

## Step 6: Report Summary

After processing, report back to the user with:

| Field | Value |
|---|---|
| **Owner** | {Alias} ({Thai Name}) |
| **Team** | Mandalorian / IT System |
| **Date** | {Extracted Date} |
| **Distance** | {Extracted Distance} km |
| **Activity** | 🏃 Run / 🚶 Walk |
| **Renamed** | `{original_filename}` → `{new_filename}` |
| **Status** | ✅ Processed / ⚠️ Review needed |
| **README** | Updated — {total_distance} km, {active_days} days |

### Validation Warnings

Flag the following issues to the user:

| Condition | Warning |
|---|---|
| Distance < 1.0 km (Run) | ⚠️ Below minimum run distance (1 km). Will be marked invalid. |
| Distance < 2.0 km (Walk) | ⚠️ Below minimum walk distance (2 km). Will be marked invalid. |
| Duplicate date for same person | ⚠️ Another entry already exists for this person on this date. |
| Cannot determine date from image | ❌ Unable to extract date. Ask user for the correct date. |

> **Note:** The competition officially starts Q1 2026, but pre-2026 statistics (e.g., Dec 2025) are tracked and accumulated into the results. Accumulation flows continuously across all months.

---

## Quick Reference

- **Project root:** `/Users/giornoadd/my-macos/running-comp`
- **Evidence folder:** `member_results/{Team}-{ID}_{ThaiName} ({Alias})/`
- **Results CSV:** `results/yyyy-Month.csv` (auto-generated for all months)
- **Results MD:** `results/yyyy-Month.md` (auto-generated tables)
- **Member READMEs:** `member_results/{FolderName}/README.md` (per-member profiles with stats)
- **Documentation:** `docs/` — [Tournament Rules](docs/Tournament%20Rules.md), [Team Member List](docs/Team%20member%20list.md), [Tournament Calendar](docs/Tournament%20Calendar.md), [End-to-End Workflow](docs/End-to-End%20Workflow.md)
- **Scripts:**
  - `src/run_all.py` — Master pipeline (reformat → watermark → recalculate)
  - `src/reformat_files.py` — Standardize filenames to `{nickname}-{yyyy}-{mon}-{dd}.{ext}`
  - `src/add_date_watermark.py` — Add date watermark (bottom-right)
  - `src/add_name_watermark.py` — Add owner name watermark (bottom-center)
  - `src/analyze_with_gemini.py` — AI-powered OCR distance extraction (requires `GEMINI_API_KEY`)
  - `src/recalculate_csv.py` — Validate distances and recalculate team statistics
  - `src/generate_member_readmes.py` — Generate individual member README profiles
- **Competition period:** Q1 (Jan-Mar), Q2 (Apr-Jun), Q3 (Jul-Sep), Q4 (Oct-Dec) 2026
- **Current quarter:** Q1 🟢 In Progress (Week 9 as of 22 Feb 2026)
- **Pre-2026 data:** Tracked and accumulated (e.g., 2025-October, 2025-December)
- **Scoring:** Team = Average Distance (Total ÷ 10 members), Individual = Total Distance
- **Minimum distance:** Run ≥ 1.0 km, Walk ≥ 2.0 km