
import os
import re
import argparse
import subprocess
import time
from datetime import datetime

def parse_date_from_filename(filename):
    # Standard format: nickname-yyyy-mon-dd.ext
    # e.g., oat-2026-jan-15.jpg
    # Also handle _1, _2 suffixes
    
    match = re.search(r'-(\d{4})-([a-z]{3})-(\d{2})', filename.lower())
    if match:
        y, m, d = match.groups()
        try:
            dt = datetime.strptime(f"{y}-{m}-{d}", "%Y-%b-%d")
            # Set to 9 AM just to have a fixed time
            dt = dt.replace(hour=9, minute=0, second=0)
            return dt
        except ValueError:
            pass
    return None

def update_metadata(base_dir, dry_run=False):
    if not os.path.exists(base_dir):
        print(f"Error: {base_dir} not found.")
        return

    print(f"Scanning {base_dir}...")
    
    count = 0
    errors = 0
    
    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if filename.startswith('.'): continue
            
            filepath = os.path.join(root, filename)
            
            dt = parse_date_from_filename(filename)
            if not dt:
                # print(f"  [Skip] Could not parse date from {filename}")
                continue
                
            # timestamp for os.utime
            ts = dt.timestamp()
            
            # format for SetFile: "mm/dd/yyyy hh:mm:ss"
            # Note: SetFile expects 24h format or AM/PM? 
            # Man page says: "mm/dd/yyyy hh:mm:ss [AM|PM]"
            # Let's use %m/%d/%Y %H:%M:%S and see if it works (usually fine).
            setfile_date = dt.strftime("%m/%d/%Y %H:%M:%S")
            
            if dry_run:
                print(f"  [DryRun] {filename} -> Set date to {setfile_date}")
            else:
                try:
                    # 1. Update Modification Time / Access Time
                    os.utime(filepath, (ts, ts))
                    
                    # 2. Update Creation Time (macOS specific)
                    # SetFile -d "date" file
                    cmd = ['SetFile', '-d', setfile_date, filepath]
                    subprocess.run(cmd, check=True)
                    
                    # print(f"  [Updated] {filename}")
                    count += 1
                except Exception as e:
                    print(f"  [Error] {filename}: {e}")
                    errors += 1
                    
    if dry_run:
        print("Dry run complete.")
    else:
        print(f"Finished. Updated {count} files. Errors: {errors}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="/Users/giornoadd/my-macos/running-comp/member_results")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    update_metadata(args.dir, args.dry_run)
