#!/usr/bin/env python3
"""
Single CLI entrypoint to run the entire End-to-End Workflow securely.
Usage:
    python3 src/run_all.py

This wrapper executes the workflow outlined in `docs/End-to-End Workflow.md`
in chronological order to reformat evidence, add watermarks, recalculate
statistics, and generate member READMEs.
"""

import os
import subprocess
import sys

# Compute the root base directory based on where this script lives
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPTS_DIR)

def run_script(script_name, *args):
    print(f"\n{'='*50}")
    print(f"🚀 Running: {script_name} {' '.join(args)}")
    print(f"{'='*50}")
    
    cmd = [sys.executable, os.path.join(SCRIPTS_DIR, script_name)] + list(args)
    result = subprocess.run(cmd, cwd=BASE_DIR)
    
    if result.returncode != 0:
        print(f"\n❌ Error executing {script_name}. Aborting workflow.")
        sys.exit(result.returncode)
    print(f"✅ Finished: {script_name}")

def main():
    print("🌟 Starting End-to-End Running Competition Workflow...\n")
    
    # Step 1: Evidence Submission is a manual drop-in via the users.
    
    # Step 2: Reformat and Standardize Filenames
    run_script("reformat_files.py", "--dir", "member_results")
    
    # Step 3: Apply Watermarks
    run_script("add_date_watermark.py")
    run_script("add_name_watermark.py")
    
    # Step 4: Distance Extraction (OCR via Gemini)
    # The workflow mentions this is optional or relies on Gemini
    print(f"\n{'='*50}")
    print("⏭ Skipping optional `analyze_with_gemini.py` to avoid accidental API charges.")
    print("   If you need to strictly OCR new files with AI, run manually:")
    print("   python3 src/analyze_with_gemini.py")
    print(f"{'='*50}\n")
    
    # Step 5: Recalculate Statistics and Apply Rules
    run_script("recalculate_csv.py")
    
    # Step 6: Generate Member READMEs
    run_script("generate_member_readmes.py")
    
    print("\n🎉 End-to-End Workflow completed successfully!\n")

if __name__ == "__main__":
    main()
