# Workflow & Automation Usage

This project supports two core modes of operation: **Batch Execution** via Python scripts, and **Autonomous AI Execution** via Workflows. Both interact with the exact same underlying filesystem data structure.

## 1. Operating the Python Pipeline (Batch Mode)

The traditional method of updating the leaderboard is ensuring all screenshots are correctly dropped into the correct member folders, and running the single root pipeline script.

```bash
# Run the entire pipeline (Steps 1 through 6)
python3 src/run_all.py
```

Under the hood, this executes the following sequence:
1. `reformat_files.py` (Renames files to `{nickname}-{yyyy}-{mon}-{dd}.{ext}`)
2. `add_date_watermark.py`
3. `add_name_watermark.py`
4. `recalculate_csv.py` (Validates and updates `results/README.md`)
5. `generate_member_readmes.py` (Updates individual statistics markdown profiles)

*Note: `analyze_with_gemini.py` is called internally by `reformat_files.py` if an API key is present.*

## 2. Using the AI Agent Workflows

The preferred operational method is using the AI Agent extensions configured in the IDE workspace. These agents execute specific contextual functions natively on the codebase.

Use the `/[slash command]` in your AI chat prompt to trigger the workflows defined in the `.agents/workflows/` directory.

### The Agent Roster

| Agent Name | Trigger Command | Purpose & Output |
| :--- | :--- | :--- |
| **🏟️ Coach Assistant** | `/coach-assistant` | **Primary operations handler.** Use this to process a single dropped evidence screenshot. It handles OCR, file moving, stat aggregation, and personal/team statistic updates end-to-end. |
| **🏃 Running Coach** | `/running-coach` | **Personalized training.** Reads a user's recent activity from `personal-statistics.md` and generates a structured weekly plan in their `running-plan.md` file. |
| **📈 Sports Analyst** | `/sports-analyst` | **Visualization & Data.** Creates polished infographics, Top 5 tables, and standalone `.md` reports. Outputs strictly to `resources/tournaments-reports/`. |
| **📣 Tournament Reporter** | `/tournament-reporter` | **Hype & Engagement.** Takes the raw data and creates stylized, motivational social media posts, LINE group recaps, and dramatic narratives. |

### Execution Example

```text
USER: "I've dropped a new file in GIO's folder. @[/coach-assistant], please process."
```

The system will autonomously execute the workflow: scan the directory, use the OCR python script for analysis, run renaming/watermarking shell commands, use search/replace tools for markdown files, and notify the user when the entry is finalized on the leaderboard.
