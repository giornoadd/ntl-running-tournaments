
import os
import argparse
import subprocess
from utils import dates

def sync_metadata(base_dir, dry_run=False):
    if not os.path.exists(base_dir):
        print(f"Error: {base_dir} not found.")
        return

    print(f"Scanning {base_dir}...")
    count = 0
    
    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if filename.startswith('.'): continue
            
            filepath = os.path.join(root, filename)
            
            # Parse date from filename
            dt = dates.parse_date_from_filename(filename)
            if not dt: continue
            
            # Set to 9 AM
            dt = dt.replace(hour=9, minute=0, second=0)
            
            # Format for SetFile
            setfile_date = dt.strftime("%m/%d/%Y %H:%M:%S")
            ts = dt.timestamp()
            
            if dry_run:
                print(f"  [DryRun] {filename} -> Set date to {setfile_date}")
            else:
                try:
                    os.utime(filepath, (ts, ts))
                    subprocess.run(['SetFile', '-d', setfile_date, filepath], check=True)
                    count += 1
                except Exception as e:
                    print(f"  [Error] {filename}: {e}")
                    
    if not dry_run:
        print(f"Updated metadata for {count} files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="/Users/giornoadd/my-macos/running-comp/member_results")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    sync_metadata(args.dir, args.dry_run)
