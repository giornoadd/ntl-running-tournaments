# Running Competition 2026 🏃‍♂️

Welcome to the **Running Competition 2026** tracker!
This repository automates the tracking, watermarking, and continuous statistics reporting for the friendly inter-team running and step competition between the **Mandalorian** and **IT System** teams.

## 🏆 Current Status
- **Quarter**: Q1 (Jan – Mar 2026)
- **Status**: 🟢 Active (Week 9)

### Live Standings

| Metric | ⚔️ Mandalorian | 💻 IT System | Leader |
| :--- | ---: | ---: | :--- |
| **Total Distance** | 357.78 km | 460.48 km | 💻 IT System |
| **Average / Person** | 35.78 km | 46.05 km | 💻 IT System |

> IT System leads by **10.27 km/person** 🏆

📊 Full quarterly & monthly breakdowns → [`results/README.md`](results/README.md)

---

## ⚙️ Project Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment (optional — for AI OCR only):**
   ```bash
   # .env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

---

## 🏃‍♀️ How To Use

The codebase relies on a **"Filesystem-as-Source-of-Truth"** model.

1. **Drop Evidence:**
   Drag & drop participant screenshots into their folder under `member_results/`.

2. **Run the Pipeline:**
   ```bash
   python3 src/run_all.py
   ```
   This will automatically: rename files → watermark → recalculate statistics → generate member READMEs.

---

## 📂 Directory Structure

| Directory | Purpose |
|-----------|---------|
| `docs/` | [Tournament Rules](docs/Tournament%20Rules.md), [Team Members](docs/Team%20member%20list.md), [Calendar](docs/Tournament%20Calendar.md), [Workflow](docs/End-to-End%20Workflow.md) |
| `member_results/` | Per-member folders with evidence screenshots and individual READMEs |
| `results/` | Monthly CSV/MD statistics and [quarterly standings](results/README.md) |
| `src/` | [Automation scripts](src/README.md) — pipeline, watermarking, recalculation, README generation |
| `tests/` | 48 pytest tests covering config, dates, files, recalculation, and member READMEs |

---

## 📚 Documentation

For architecture details, tournament rules, and the full E2E pipeline, see:

👉 **[GEMINI.md](GEMINI.md)**
