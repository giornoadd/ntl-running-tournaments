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
6. `generate_coach_analysis.py` (Generates `performance-report/` + `coach-analysis.md` for all members)

*Note: `analyze_with_gemini.py` is called internally by `reformat_files.py` if an API key is present.*

## 2. Using the AI Agent Workflows

The preferred operational method is using the AI Agent extensions configured in the IDE workspace. These agents execute specific contextual functions natively on the codebase.

Use the `/[slash command]` in your AI chat prompt to trigger the workflows defined in the `.agents/workflows/` directory.

### The Agent Roster

| Agent Name | Trigger Command | Purpose & Output |
| :--- | :--- | :--- |
| **🏟️ Coach Assistant** | `/coach-assistant` | **Primary operations handler.** Process a dropped evidence screenshot — OCR, file renaming, stat aggregation, CSV + personal-statistics updates, and rebuilds dashboard data. |
| **🏃 Running Coach** | `/running-coach` | **Personalized training.** Post-run analysis, goal setting, progress reviews, and `running-plan.md` creation using VDOT & periodization methods. Directly delegates to coach-assistant for new data. |
| **📈 Sports Analyst** | `/sports-analyst` | **Visualization & Data.** Validates data (Step 0), creates infographics, Top 5 tables, weekly/monthly recaps, README updates. Output: `resources/tournaments-reports/`. |
| **📣 Tournament Reporter** | `/tournament-reporter` | **Hype & Engagement.** E-Sports Caster energy! Writes LINE messages, Facebook posts, personal shoutouts, and **Auto-generates Infographics via Python** `matplotlib`. |
| **💻 Software Engineer** | `/software-engineer` | **Full pipeline.** Regenerates data (CSV → data.js → data.json), builds React dashboard, deploys to GitHub Pages. |
| **🔄 Update Dashboard** | `/update-dashboard` | **Quick rebuild.** Recalculate stats + build React app + push — lightweight alternative to `/software-engineer`. |

### Execution Example

```text
USER: "I've dropped a new file in GIO's folder. @[/coach-assistant], please process."
```

The system will autonomously execute the workflow: scan the directory, extract data from images, rename files, update CSV + personal-statistics, regenerate READMEs, rebuild the dashboard, and push to GitHub.
