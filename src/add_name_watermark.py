#!/usr/bin/env python3
"""
Scan all renamed images in member_results/ and add a name watermark
to the bottom-center of the image.

Usage:
    python3 src/add_name_watermark.py [--dry-run]
"""

import os
import sys
from utils.config import RENAMED_PATTERN, MEMBER_RESULTS_DIR
from utils.image import add_text_watermark

def extract_name_from_filename(filename):
    """Extract nickname from filename for watermark display."""
    match = RENAMED_PATTERN.match(filename)
    if not match:
        return None
    nickname = match.group(1).capitalize()
    return nickname

def scan_and_watermark(dry_run=False, target_files=None):
    """Scan all renamed images and add name watermarks."""
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
        name_text = extract_name_from_filename(filename)
        
        if not name_text:
            print(f"  ⏭️  Skipping {filename} (cannot extract name)")
            skipped += 1
            continue
        
        print(f"[{folder}] {filename} → watermark: '{name_text}'")
        
        if add_text_watermark(filepath, name_text, position="bottom-center", dry_run=dry_run):
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
