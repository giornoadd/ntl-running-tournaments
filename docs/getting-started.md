# Getting Started

Follow these instructions to set up your local environment to run the Running Competition 2026 processing pipeline or contribute to the AI Agents.

## 1. Prerequisites

- **Python**: 3.10 or higher.
- **Git**: For version control.
- **macOS/Linux**: The scripts rely on standard bash/zsh behaviors and path separators.

## 2. Environment Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository_url>
   cd running-comp
   ```

2. **Create a Python Virtual Environment**:
   It is highly recommended to isolate the project dependencies.
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   Install the required image processing, AI, and charting libraries.
   ```bash
   pip install -r requirements.txt
   ```
   *Core dependencies typically include `Pillow`, `google-generativeai`, `matplotlib`, `seaborn`, and `pandas`.*

## 3. Configuration (`.env`)

The project requires specific environment variables to function properly, mostly concerning AI OCR for parsing evidence screenshots.

1. Copy the local template:
   ```bash
   cp .env.local .env
   ```

2. Edit `.env` and add your keys (See [auth-flows.md](auth-flows.md) for generation instructions):
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## 4. Run the Local Pipeline

To verify your installation, you can run the primary aggregation script. This will recalculate the current standings based on the existing filesystem data without needing new images.

```bash
python3 src/recalculate_csv.py
python3 src/generate_coach_analysis.py
```

If successful, you will see output like:
```text
Processing results/2026-January.csv...
  -> Saved results/2026-January.csv
  -> Generated results/2026-January.md
...
```

You are now ready to process new evidence or develop new AI Agent workflows!
