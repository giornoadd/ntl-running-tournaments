#!/usr/bin/env python3
"""
Scan all renamed images in member_results/ and add a date watermark
to the bottom-right corner if the image doesn't clearly show its date.

Usage:
    python3 src/add_date_watermark.py [--dry-run]
"""

import os
import sys
from utils.config import RENAMED_PATTERN, MEMBER_RESULTS_DIR
from utils.image import add_text_watermark

def extract_date_from_filename(filename):
    """Extract date string from filename for watermark display."""
    match = RENAMED_PATTERN.match(filename)
    if not match:
        return None
    
    year = match.group(2)
    month = match.group(3).lower()
    day = match.group(4)
    
    # Format: "21 Feb 2026"
    date_str = f"{int(day)} {month.capitalize()} {year}"
    return date_str

def scan_and_watermark(dry_run=False, target_files=None):
    """Scan all renamed images and add watermarks where needed."""
    if target_files:
        files_to_process = target_files
    else:
        files_to_process = []
        for root, dirs, files in os.walk(MEMBER_RESULTS_DIR):
            for f in files:
                if RENAMED_PATTERN.match(f):
                    files_to_process.append(os.path.join(root, f))
    
    files_to_process.sort()
    
    print(f"\nFound {len(files_to_process)} renamed image(s) to process\n")
    
    watermarked = 0
    skipped = 0
    errors = 0
    
    for filepath in files_to_process:
        filename = os.path.basename(filepath)
        folder = os.path.basename(os.path.dirname(filepath))
        date_text = extract_date_from_filename(filename)
        
        if not date_text:
            print(f"  ⏭️  Skipping {filename} (cannot extract date)")
            skipped += 1
            continue
        
        print(f"[{folder}] {filename} → watermark: '{date_text}'")
        
        if add_text_watermark(filepath, date_text, position="bottom-right", dry_run=dry_run):
            watermarked += 1
        else:
            errors += 1
    
    print(f"\n{'='*50}")
    print(f"Summary: {watermarked} watermarked, {skipped} skipped, {errors} errors")
    print(f"Total: {len(files_to_process)} files processed")

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    target_files = [f for f in sys.argv[1:] if not f.startswith("--")]
    
    if dry_run:
        print("🔍 DRY-RUN MODE - no changes will be made\n")
    
    scan_and_watermark(dry_run=dry_run, target_files=target_files if target_files else None)
