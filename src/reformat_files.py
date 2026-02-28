
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
    
    for entry in os.listdir(base_dir):
        member_dir = os.path.join(base_dir, entry)
        if not os.path.isdir(member_dir):
            continue
        
        folder_name = entry
        if target_folder and folder_name != target_folder:
            continue
            
        nickname = files.get_nickname(folder_name)
        
        if not nickname:
            continue
            
        # Look for images in running-pics/ subfolder
        pics_dir = os.path.join(member_dir, "running-pics")
        if not os.path.isdir(pics_dir):
            os.makedirs(pics_dir, exist_ok=True)
            
        print(f"Processing {folder_name} (Nickname: {nickname})")
        
        # Get image files from running-pics/
        img_files = [f for f in os.listdir(pics_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        for filename in img_files:
            filepath = os.path.join(pics_dir, filename)
            
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
                continue
                
            # Rename
            # nickname-yyyy-mon-dd.ext
            months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
            mon_str = months[dt.month - 1]
            
            new_base = f"{nickname}-{dt.year}-{mon_str}-{dt.day:02d}"
            _, ext = os.path.splitext(filename)
            new_filename = f"{new_base}{ext}"
            new_filepath = os.path.join(pics_dir, new_filename)
            
            if filename == new_filename:
                continue
                
            # Collision handling
            counter = 1
            while os.path.exists(new_filepath):
                if new_filepath == filepath: break
                
                new_filename = f"{new_base}_{counter}{ext}"
                new_filepath = os.path.join(pics_dir, new_filename)
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
