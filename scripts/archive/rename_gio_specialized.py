
import os
import re
import argparse
from datetime import datetime
import subprocess
import shutil

def parse_runna_filename(filename):
    """
    Parses 'Runna' filenames to extract date.
    Examples:
    - Runna 5km Easy Run on Jan 26, 2026 - ...
    - Runna Rolling 400s on 15 Sep 2568 BE - ...
    """
    match = re.search(r'Runna .*? on (.*?) -', filename)
    if match:
        date_str = match.group(1).strip()
        is_be = 'BE' in date_str
        date_str = date_str.replace(' BE', '').strip()
        
        # Formats to try
        formats = [
            "%b %d, %Y", # Jan 26, 2026
            "%d %b %Y",  # 15 Sep 2568
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                if is_be:
                    dt = dt.replace(year=dt.year - 543)
                return dt
            except ValueError:
                continue
    return None

def parse_gio_previous_format(filename):
    """
    Parses the format from the previous step: gio-04-feb-2026.jpg
    """
    # gio-04-feb-2026.jpg or gio-04-feb-2026_1.jpg
    match = re.search(r'gio-(\d{2})-([a-z]{3})-(\d{4})', filename)
    if match:
        d, m, y = match.groups()
        try:
            return datetime.strptime(f"{d}-{m}-{y}", "%d-%b-%Y")
        except ValueError:
            pass
    return None

def get_creation_date(filepath):
    """
    Get creation date using macOS metadata (mdls) or fallback to mtime.
    """
    try:
        result = subprocess.run(
            ['mdls', '-name', 'kMDItemContentCreationDate', '-raw', filepath], 
            capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout and result.stdout != '(null)':
            # Output format: 2026-02-08 13:35:43 +0000
            dt_str = result.stdout.strip()
            return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S %z")
    except Exception as e:
        print(f"  [Warn] Metadata extraction failed: {e}")
    
    # Fallback to mtime
    return datetime.fromtimestamp(os.path.getmtime(filepath))

def rename_gio_files(base_dir, dry_run=False):
    if not os.path.exists(base_dir):
        print(f"Error: Directory not found: {base_dir}")
        return

    print(f"Scanning: {base_dir}")
    files = [f for f in os.listdir(base_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    # Sort files to ensure deterministic order (e.g. process IMG_001 before IMG_002)
    files.sort()

    count = 0
    for filename in files:
        filepath = os.path.join(base_dir, filename)
        
        source = "Unknown"
        date_obj = None
        
        # 1. Try Filename Parsing (Runna)
        date_obj = parse_runna_filename(filename)
        if date_obj: source = "Filename(Runna)"
            
        # 2. Try Previous Format Parsing
        if not date_obj:
            date_obj = parse_gio_previous_format(filename)
            if date_obj: source = "Filename(Gio)"
        
        # 3. Fallback to Metadata
        if not date_obj:
            date_obj = get_creation_date(filepath)
            source = "Metadata"
        
        if not date_obj:
            print(f"  [Skip] Could not determine date for: {filename}")
            continue
            
        # Format: gio-yyyy-mon-dd
        months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
        month_str = months[date_obj.month - 1]
        year = date_obj.year
        
        # Sanity check for year
        if year < 2020:
             print(f"  [Warn] Detected old year ({year}) for {filename}. Using metadata might be wrong.")
        
        _, ext = os.path.splitext(filename)
        # NEW FORMAT HERE
        new_base = f"gio-{year}-{month_str}-{date_obj.day:02d}"
        new_filename = f"{new_base}{ext}"
        new_filepath = os.path.join(base_dir, new_filename)
        
        # Validation: Don't rename if already correct
        if filename == new_filename:
            continue
            
        # Collision handling
        counter = 1
        while os.path.exists(new_filepath):
            # Check if it's the SAME file 
            if os.path.abspath(filepath) == os.path.abspath(new_filepath):
                break
            
            new_filename = f"{new_base}_{counter}{ext}"
            new_filepath = os.path.join(base_dir, new_filename)
            counter += 1
            
        if filename == new_filename:
            continue

        if dry_run:
            print(f"[DryRun] {filename} -> {new_filename} ({source})")
        else:
            try:
                os.rename(filepath, new_filepath)
                print(f"[Renamed] {filename} -> {new_filename} ({source})")
                count += 1
            except Exception as e:
                print(f"[Error] Failed to rename {filename}: {e}")

    print(f"Finished. Total renamed: {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--dir", default="/Users/giornoadd/my-macos/running-comp/member_results/Manda-1_โจ (GIO)")
    args = parser.parse_args()
    
    rename_gio_files(args.dir, args.dry_run)
