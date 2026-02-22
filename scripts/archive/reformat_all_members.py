
import os
import re
import argparse
from datetime import datetime
import subprocess

def get_nickname(folder_name):
    """
    Extract nickname from folder name.
    e.g. "Manda-1_โจ (GIO)" -> "gio"
    e.g. "ITSystem-1_Oat (โอ๊ต)" -> "oat"
    """
    try:
        parts = folder_name.split('_')
        if len(parts) >= 2:
            name_part = "_".join(parts[1:]) # "โจ (GIO)" or "Oat (โอ๊ต)"
            
            # Strategy 1: Look for parens
            if '(' in name_part and ')' in name_part:
                in_paren = name_part.split('(')[1].split(')')[0].strip()
                if re.search(r'[a-zA-Z]', in_paren):
                    return in_paren.lower()
            
            # Strategy 2: Pre-paren English
            pre_paren = name_part.split('(')[0].strip()
            if re.search(r'[a-zA-Z]', pre_paren):
                return pre_paren.lower()
                
    except Exception:
        pass
    return None

def parse_runna_filename(filename):
    match = re.search(r'Runna .*? on (.*?) -', filename)
    if match:
        date_str = match.group(1).strip()
        is_be = 'BE' in date_str
        date_str = date_str.replace(' BE', '').strip()
        formats = ["%b %d, %Y", "%d %b %Y"]
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                if is_be: dt = dt.replace(year=dt.year - 543)
                return dt
            except ValueError: continue
    return None

def parse_existing_nickname_format(filename, nickname):
    """
    Parses nickname-dd-mon-yyyy.ext
    e.g. oat-15-jan-2026.jpg
    """
    # Create regex based on nickname to avoid false positives?
    # Actually, the file might adhere to format but have wrong nickname if moved?
    # Let's assume the file starts with the nickname or just parse the date pattern at the end.
    
    # Pattern: .*-dd-mon-yyyy.ext OR .*-yyyy-mon-dd.ext (if already done)
    
    # Try dd-mon-yyyy
    match = re.search(r'-(\d{2})-([a-z]{3})-(\d{4})(_\d+)?\.', filename.lower())
    if match:
        d, m, y, _ = match.groups()
        try: return datetime.strptime(f"{d}-{m}-{y}", "%d-%b-%Y")
        except ValueError: pass

    # Try yyyy-mon-dd (to not double rename or break if mixed)
    match = re.search(r'-(\d{4})-([a-z]{3})-(\d{2})(_\d+)?\.', filename.lower())
    if match:
         # It's already in the target format.
         # But we might need to verify the nickname prefix matches the current folder?
         # For now, just return valid date.
         y, m, d, _ = match.groups()
         try: return datetime.strptime(f"{d}-{m}-{y}", "%d-%b-%Y")
         except ValueError: pass
         
    return None

def get_creation_date(filepath):
    try:
        result = subprocess.run(
            ['mdls', '-name', 'kMDItemContentCreationDate', '-raw', filepath], 
            capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout and result.stdout != '(null)':
            dt_str = result.stdout.strip()
            return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S %z")
    except Exception: pass
    return datetime.fromtimestamp(os.path.getmtime(filepath))

def reformat_files(base_dir, dry_run=False):
    if not os.path.exists(base_dir):
        print(f"Error: Directory not found: {base_dir}")
        return

    # Iterate over all subdirectories
    processed_count = 0
    
    # walk is recursive, but we only want immediate children of member_results usually
    # But user structure is member_results/FOLDER/file
    
    for root, dirs, files in os.walk(base_dir):
        if root == base_dir: continue # Skip root itself
        
        folder_name = os.path.basename(root)
        nickname = get_nickname(folder_name)
        
        if not nickname:
            print(f"Skipping folder {folder_name} (No nickname found)")
            continue
            
        print(f"Processing {folder_name} (Nickname: {nickname}) ...")
        
        files.sort()
        for filename in files:
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png')): continue
            
            filepath = os.path.join(root, filename)
            
            # 1. Parse Date
            date_obj = parse_runna_filename(filename)
            source = "Runna"
            
            if not date_obj:
                date_obj = parse_existing_nickname_format(filename, nickname)
                source = "ExistingFormat"
            
            if not date_obj:
                date_obj = get_creation_date(filepath)
                source = "Metadata"
            
            if not date_obj:
                print(f"  [Skip] No date for {filename}")
                continue
                
            # 2. Form new name
            months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
            month_str = months[date_obj.month - 1]
            year = date_obj.year
            
            # Target: nickname-yyyy-mon-dd
            new_base = f"{nickname}-{year}-{month_str}-{date_obj.day:02d}"
            _, ext = os.path.splitext(filename)
            new_filename = f"{new_base}{ext}"
            new_filepath = os.path.join(root, new_filename)
            
            if filename == new_filename: continue # Already correct
            
            # Collision
            counter = 1
            while os.path.exists(new_filepath):
                if os.path.abspath(filepath) == os.path.abspath(new_filepath): break
                new_filename = f"{new_base}_{counter}{ext}"
                new_filepath = os.path.join(root, new_filename)
                counter += 1
            
            if filename == new_filename: continue

            if dry_run:
                print(f"[DryRun] {filename} -> {new_filename} ({source})")
            else:
                try:
                    os.rename(filepath, new_filepath)
                    print(f"[Renamed] {filename} -> {new_filename} ({source})")
                    processed_count += 1
                except Exception as e:
                    print(f"[Error] {filename}: {e}")

    print(f"Finished. Renamed {processed_count} files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    # Default to base member_results
    parser.add_argument("--dir", default="/Users/giornoadd/my-macos/running-comp/member_results")
    args = parser.parse_args()
    
    reformat_files(args.dir, args.dry_run)
