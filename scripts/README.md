# Scripts Archive 📜

This directory contains standalone, legacy, or specialized utility scripts that are **not** part of the official End-to-End pipeline (which now lives in `src/`). 

They are preserved here for reference, debugging, or highly specific edge-cases.

## 🗃️ Archived Utilities List (`archive/`)

| Script Name | Objective / Purpose |
| :--- | :--- |
| **`rename_files.py`** | The original monolithic script for date-based renaming. Replaced by the more modular `src/reformat_files.py`. |
| **`check_duplicates_ocr.py`** | Scanned files using OCR to find duplicate submission screenshots based on visual text overlap. |
| **`deduplicate_files.py`** | Another logic variant for finding duplicate files based on content/naming hashes. |
| **`extract_running_stats.py`** | An early attempt at mining running statistics directly from images before the CSV workflow was established. |
| **`generate_report.py`** | Generated an older Markdown-based report style directly from directory parsing instead of CSV accumulation. |
| **`reformat_all_members.py`** | Experimental script to format all member directories sequentially. Incorporated into the modern `reformat_files.py` logic. |
| **`upload_to_drive.py`** | Connected to the Google Drive API to recursively upload local `member_results/` up to the shared Drive folder. |
| **`list_drive.py`** | Debugging utility that lists files inside the authenticated Google Drive folder to verify successful API bindings. |
| **`correct_gio_renames.py`** | A specialized, hardcoded script to fix a batch of improperly formatted file dates specifically for player `GIO`. |
| **`rename_gio_specialized.py`** | Another hotfix script tailored to `GIO`'s specific EXIF edge-cases. |
| **`resolve_ton_collision.py`** | A hotfix to handle duplicate filename collisions that occurred for player `Ton`. |
| **`rename_chan_ocr.py`** | A specialized script invoking OCR aggressively to fix dates explicitly for player `Chan`'s screenshots. |
| **`apply_manual_renames.py`** | A dictionary-driven renaming override script used to manually bypass automation for problematic file states. |
| **`create_folders.py`** | Utility to instantly bulk-generate the `/member_results` folder skeletons for the 20 registered generic IDs. |
| **`run_watermark_batch.sh`** | An older Bash shell script used to execute watermarking prior to the unified Python `src/run_all.py` pipeline. |
| **`verify_ocr.py`** / **`verify_rename.py`** | Minor validation scripts to independently test the Tesseract/Gemini regex extraction models against known inputs before bulk-applying. |
| **`sync_metadata.py`** / **`update_metadata_from_filename.py`** | Utilities that forcibly injected/corrected EXIF DateTimeOriginal metadata headers into JPG tracks based on their directory tree formatting. |
| **`convert_csv_to_md.py`** | Script used to parse the raw `results/*.csv` tracking files and generate formatted Markdown tables. |
| **`recover_csv.py`** | Emergency script used to reverse-engineer corrupted/truncated CSV files back into existence by reading their intact Markdown representations. |

---
*If you are looking for the active operational pipeline scripts (e.g. `run_all.py`, `reformat_files.py`, `recalculate_csv.py`), navigate back to the **`src/`** directory.*
