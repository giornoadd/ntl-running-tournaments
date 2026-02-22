# Running Competition 2026 🏃‍♂️

Welcome to the **Running Competition 2026** tracker! 
This repository automates the tracking, watermarking, and continuous statistics reporting for the friendly inter-team running and step competition between the "Mandalorian" and "IT System" teams.

## 🏆 Current Status
- **Quarter**: Q1 (Jan - Mar)
- **Status**: Active

---

## ⚙️ Project Setup

1. **Install Python Dependencies:**
   Ensure you have Python 3 installed, then install the required image processing and AI dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables:**
   A `.env` template file has been provided in the root. 
   If you plan to use the OCR vision utilities (`src/analyze_with_gemini.py`) to scrape exact distances out of screenshots, provide an active Gemini API key:
   
   *Update `.env`:*
   ```ini
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   *(Ensure to source or load your `.env` variables before running the crawler if bypassing the unified tools).*

---

## 🏃‍♀️ How To Use

The codebase relies on a **"Filesystem-as-Source-of-Truth"** model. 

1. **Drop Evidence:** 
   Drag and drop the participant screenshot files directly into their respective folders nested under `member_results/`.

2. **Run The Pipeline:** 
   Execute the unified End-to-End processing wrapper. This will automatically rename the files safely, burn-in the Name and Date watermarks to the images, and recalculate the daily and accumulated distances out to the `results/yyyy-month.csv` tracking sheets based on the official Tournament Rules.
   
   ```bash
   python3 src/run_all.py
   ```

---

## 📚 Documentation 
For deep-dives into the architecture, tournament rules, and explicit breakdown of the End-to-End operations pipeline, refer to the overarching documentation hub:

👉 **[GEMINI.md](GEMINI.md)**
