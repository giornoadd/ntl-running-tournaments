
import os
import argparse
import shutil
from datetime import datetime
from utils import files, dates, ocr

def reformat_files(base_dir, target_folder=None, dry_run=False, use_ocr=False, fallback_mtime=False):
    if not os.path.exists(base_dir):
        print(f"Error: {base_dir} not found.")
        return

    print(f"Scanning {base_dir}...")
    
    for root, dirs, _ in os.walk(base_dir):
        if root == base_dir: continue
        
        folder_name = os.path.basename(root)
        if target_folder and folder_name != target_folder:
            continue
            
        nickname = files.get_nickname(folder_name)
        
        if not nickname:
            # print(f"Skipping {folder_name} (no nickname)")
            continue
            
        print(f"Processing {folder_name} (Nickname: {nickname})")
        
        # Get files
        img_files = [f for f in os.listdir(root) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        # Sort to ensure consistent processing? No, we process one by one.
        # But for incrementing suffix, we might need order? No, suffix logic handles it.
        
        for filename in img_files:
            filepath = os.path.join(root, filename)
            
            # 1. Try Filename Date
            dt = dates.parse_date_from_filename(filename)
            
            # 2. Try OCR if requested or filename failed (and forced?)
            if not dt and use_ocr:
                print(f"  [OCR] Scanning {filename}...")
                text = ocr.extract_text(filepath)
                dt = dates.parse_date_generic(text)
                if dt: print(f"    Found date: {dt}")
            
            # 3. Fallback: Modification time?
            if not dt and fallback_mtime:
                mtime = os.path.getmtime(filepath)
                dt = datetime.fromtimestamp(mtime)
                print(f"    [Fallback] Using modification time: {dt}")

            if not dt:
                # print(f"  [Skip] No date found for {filename}")
                continue
                
            # Rename
            # nickname-yyyy-mon-dd.ext
            months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
            mon_str = months[dt.month - 1]
            
            new_base = f"{nickname}-{dt.year}-{mon_str}-{dt.day:02d}"
            _, ext = os.path.splitext(filename)
            new_filename = f"{new_base}{ext}"
            new_filepath = os.path.join(root, new_filename)
            
            if filename == new_filename:
                continue
                
            # Collision handling
            counter = 1
            while os.path.exists(new_filepath):
                # If content is identical? We assume unique filenames for now or handle stats duplicates later.
                # Just rename to _1, _2
                if new_filepath == filepath: break # Should have proved equality above, but just in case
                
                new_filename = f"{new_base}_{counter}{ext}"
                new_filepath = os.path.join(root, new_filename)
                counter += 1
                
            if dry_run:
                print(f"  [DryRun] {filename} -> {new_filename}")
            else:
                try:
                    os.rename(filepath, new_filepath)
                    print(f"  [Renamed] {filename} -> {new_filename}")
                except Exception as e:
                    print(f"  [Error] {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="/Users/giornoadd/my-macos/running-comp/member_results")
    parser.add_argument("--folder", help="Specific folder to process")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--ocr", action="store_true", help="Enable OCR fallback")
    parser.add_argument("--fallback-mtime", action="store_true", help="Fallback to file modification time if no date found")
    args = parser.parse_args()
    
    reformat_files(args.dir, args.folder, args.dry_run, args.ocr, args.fallback_mtime)
