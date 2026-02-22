import os
import argparse
import time
from datetime import datetime, timedelta
import subprocess
import re
import shutil
from PIL import Image, ImageEnhance

def get_nickname(folder_name):
    try:
         parts = folder_name.split('_')
         if len(parts) >= 2:
             name_part = "_".join(parts[1:])
             
             pre_paren = name_part.split('(')[0].strip()
             in_paren = ""
             if '(' in name_part and ')' in name_part:
                in_paren = name_part.split('(')[1].split(')')[0].strip()
             
             def is_english(s):
                 return bool(re.search(r'[a-zA-Z]', s))
             
             if is_english(pre_paren):
                 return pre_paren
             elif is_english(in_paren):
                 return in_paren
                 
    except Exception as e:
        pass
    return None

def preprocess_image(image_path, debug=False, debug_dir=None):
    """
    Preprocess image for better OCR:
    - Convert to grayscale
    - Increase contrast
    - Upscale if too small (optional, skipped for now to keep it fast)
    """
    try:
        img = Image.open(image_path)
        
        # Convert to grayscale
        img = img.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0) # Double the contrast
        
        # Save to a file
        if debug and debug_dir:
             if not os.path.exists(debug_dir):
                 os.makedirs(debug_dir)
             temp_filename = f"debug_{os.path.basename(image_path)}.png"
             temp_path = os.path.join(debug_dir, temp_filename)
        else:
             temp_filename = f"temp_ocr_{os.getpid()}_{int(time.time()*1000)}.png"
             temp_path = os.path.join(os.path.dirname(image_path), temp_filename)
             
        img.save(temp_path)
        return temp_path
    except Exception as e:
        print(f"  [Warn] Image preprocessing failed: {e}")
        return None

def adjust_year(dt):
    """
    Convert Buddhist Era year to AD if necessary.
    Assumes years > 2400 are BE.
    """
    if dt.year > 2400:
        return dt.replace(year=dt.year - 543)
    return dt

def extract_date_from_image(image_path, debug=False):
    debug_dir = os.path.join(os.path.dirname(image_path), "debug_ocr") if debug else None
    temp_path = preprocess_image(image_path, debug, debug_dir)
    target_path = temp_path if temp_path else image_path
    
    try:
        # Run tesseract
        # We assume 'eng' is installed. 'osd' (Orientation and Script Detection) might help?
        # subprocess.run(['tesseract', target_path, 'stdout', '-l', 'eng+osd'], ...)
        result = subprocess.run(['tesseract', target_path, 'stdout'], capture_output=True, text=True)
        text = result.stdout
        
        if debug:
            print(f"  [DEBUG] OCR Output for {os.path.basename(image_path)}:\n{'-'*20}\n{text.strip()}\n{'-'*20}")
        
        # Clean up temp file if NOT debugging
        if not debug and temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            
        # Date patterns
        patterns = [
            # 29 Jan 2026, 29 Jan 2569
            (r'(\d{1,2})\s+([a-zA-Z]{3,9})\s+(\d{4})', "%d %B %Y"),
            (r'(\d{1,2})\s+([a-zA-Z]{3,9})\s+(\d{4})', "%d %b %Y"),
            # 29/01/2026, 29/01/2569
            (r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', "dmy"), 
            # 2026-01-29, 2569-01-29
            (r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', "ymd"),
            # January 29, 2026
            (r'([a-zA-Z]{3,9})\s+(\d{1,2}),\s+(\d{4})', "%B %d %Y"),
            (r'([a-zA-Z]{3,9})\s+(\d{1,2}),\s+(\d{4})', "%b %d %Y"),
            # 4-feb-2026
            (r'(\d{1,2})[/-]([a-zA-Z]{3,9})[/-](\d{4})', "%d %b %Y"),
             # Feb 4, 2026
            (r'([a-zA-Z]{3,9})\s+(\d{1,2}),\s+(\d{4})', "%b %d %Y"),
        ]

        found_date = None
        for pattern, fmt in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    if fmt == "dmy":
                        d, m, y = match.groups()
                        found_date = datetime(int(y), int(m), int(d))
                    elif fmt == "ymd":
                        y, m, d = match.groups()
                        found_date = datetime(int(y), int(m), int(d))
                    else:
                        # Reconstruct string for strptime to handle %b/%B automatically
                        # This relies on the regex groups matching the format string order roughly
                        # For the named month ones:
                        # Group 1 is usually day or month depending on pattern.
                        # We can construct the string based on the matched groups and feed to strptime
                        full_str = match.group(0)
                        # Remove commas to simplify if needed, or just strict parse
                        # Actually simpler:
                        # use dateutil if available? No, stick to stdlib.
                        # Let's try to parse the exact matched string with the format
                        # But format might expect "29 Jan 2026" and we have "29 Jan 2026" works.
                        # "Jan 29, 2026" -> "%b %d, %Y" needed. The fmt above was missing comma in pattern or format.
                        
                        # Let's use the groups to reconstruct a standard string "01 Jan 2026"
                        groups = match.groups()
                        if len(groups) == 3:
                            v1, v2, v3 = groups
                            # Guess order?
                            # If pattern starts with digit, digit, digit -> use dmy logic
                            # If pattern starts with digit, alpha, digit -> d b Y
                            # If pattern starts with alpha, digit, digit -> b d Y
                            
                            # Just trust the fmt string associated with pattern?
                            # But fmt was just a string code I made up in previous version (dmy/ymd) or strptime format.
                            # For the strptime formats, I need the string to match.
                            
                            # Let's refine the loop
                            # Special case manual parsing based on index in 'patterns' list is brittle.
                            # Let's just try to parse the full match.group(0) with the format.
                            clean_str = re.sub(r'[,.\-]', ' ', match.group(0)) # Replace separators with space
                            clean_str = re.sub(r'\s+', ' ', clean_str) # Normalize spaces
                            
                            # We need to map the format to space-separated too
                            # e.g. "%B %d %Y"
                            # This is getting complicated. Let's stick to specific handlers per regex.
                            pass

                except ValueError:
                    continue
        
        # Fallback Strict Checks (More reliable)
        
        # 1. dd-Mon-yyyy (29 Jan 2026, 4-feb-2569)
        match = re.search(r'(\d{1,2})[\s\/-]+([a-zA-Z]{3,9})[\s\/-]+(\d{4})', text, re.IGNORECASE)
        if match:
            d, m, y = match.groups()
            try:
                found_date = datetime.strptime(f"{d} {m} {y}", "%d %b %Y")
            except ValueError:
                try: found_date = datetime.strptime(f"{d} {m} {y}", "%d %B %Y")
                except ValueError: pass
        
        if not found_date:
            # 2. Month dd, yyyy (January 29, 2026)
            match = re.search(r'([a-zA-Z]{3,9})[\s]+(\d{1,2})[,\s]+(\d{4})', text, re.IGNORECASE)
            if match:
                m, d, y = match.groups()
                try:
                    found_date = datetime.strptime(f"{d} {m} {y}", "%d %b %Y")
                except ValueError:
                    try: found_date = datetime.strptime(f"{d} {m} {y}", "%d %B %Y")
                    except ValueError: pass

        if not found_date:
             # 3. Numeric (d/m/y or y-m-d)
             # d/m/y
             match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', text)
             if match:
                 d, m, y = match.groups()
                 try: found_date = datetime(int(y), int(m), int(d))
                 except ValueError: pass
             
             if not found_date:
                 # y-m-d
                 match = re.search(r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', text)
                 if match:
                     y, m, d = match.groups()
                     try: found_date = datetime(int(y), int(m), int(d))
                     except ValueError: pass
        
        # Post-process found_date
        if found_date:
            return adjust_year(found_date)

    except Exception as e:
        print(f"Error OCR extraction for {image_path}: {e}")
        if not debug and temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        
    return None

def rename_files(base_dir, target_folder=None, dry_run=False, debug=False):
    if not os.path.exists(base_dir):
        print(f"Directory not found: {base_dir}")
        return

    print(f"Scanning directory: {base_dir}")
    if dry_run:
        print(">> DRY RUN MODE: No files will be renamed. <<")
    if debug:
        print(">> DEBUG MODE: Raw OCR text will be shown and temp images saved. <<")

    for root, dirs, files in os.walk(base_dir):
        if root == base_dir:
            continue
            
        folder_name = os.path.basename(root)
        
        if target_folder and folder_name != target_folder:
            continue

        nickname = get_nickname(folder_name)
        
        if not nickname:
            print(f"Skipping folder (no nickname found): {folder_name}")
            continue
            
        nickname = nickname.lower().replace(" ", "")
        
        print(f"Processing folder: {folder_name} (Nickname: {nickname})")
        
        for filename in files:
            if filename.startswith('.'): 
                continue
            
            _, ext = os.path.splitext(filename)
            if ext.lower() not in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
                continue
                
            filepath = os.path.join(root, filename)
            
            print(f"  Scanning {filename}...")
            date_obj = extract_date_from_image(filepath, debug)
            
            source_type = "OCR"
            if date_obj:
               print(f"    Found date via OCR: {date_obj.strftime('%d-%b-%Y')}")
            else:
               source_type = "MTime"
               print(f"    No date found via OCR, using file modification time.")
               mtime = os.path.getmtime(filepath)
               date_obj = datetime.fromtimestamp(mtime)
            
            months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
            month_str = months[date_obj.month - 1]
            
            new_filename_base = f"{nickname}-{date_obj.day:02d}-{month_str}-{date_obj.year}"
            new_filename = f"{new_filename_base}{ext}"
            new_filepath = os.path.join(root, new_filename)
            
            if filename == new_filename:
                continue

            counter = 1
            while os.path.exists(new_filepath):
                new_filename = f"{new_filename_base}_{counter}{ext}"
                new_filepath = os.path.join(root, new_filename)
                counter += 1
            
            if not dry_run:
                os.rename(filepath, new_filepath)
                print(f"    [Renamed] {filename} -> {new_filename} ({source_type})")
            else:
                print(f"    [DryRun] Would rename: {filename} -> {new_filename} ({source_type})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename evidence files using OCR and modification time.")
    parser.add_argument("--dir", default="/Users/giornoadd/my-macos/running-comp/member_results", help="Base directory containing member folders")
    parser.add_argument("--folder", default=None, help="Specific folder name to process")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without renaming")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging and save temp images")
    args = parser.parse_args()
    
    try:
        subprocess.run(['tesseract', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("Error: 'tesseract' is not installed or not in PATH.")
        exit(1)
        
    rename_files(args.dir, args.folder, args.dry_run, args.debug)
