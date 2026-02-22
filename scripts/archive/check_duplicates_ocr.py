
import os
import re
import argparse
import subprocess
import time
from datetime import datetime
try:
    from PIL import Image, ImageEnhance
except ImportError:
    print("PIL not installed. Please install pillow.")
    exit(1)

def preprocess_image(image_path):
    try:
        img = Image.open(image_path)
        img = img.convert('L') # Grayscale
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        
        # Resize if too small? Tesseract likes ~300 DPI.
        # Let's just save temp.
        temp_path = f"temp_{os.getpid()}_{int(time.time()*1000)}.png"
        img.save(temp_path)
        return temp_path
    except:
        return None

def extract_text(image_path):
    temp_path = preprocess_image(image_path)
    target_path = temp_path if temp_path else image_path
    
    text = ""
    try:
        # psm 11: Sparse text
        result = subprocess.run(['tesseract', target_path, 'stdout', '--psm', '11'], capture_output=True, text=True)
        text = result.stdout
    except Exception as e:
        print(f"OCR Error for {image_path}: {e}")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
    return text

def parse_stats(text):
    distance = 0.0
    duration_str = ""
    
    # Distance: Look for N.NN km or N.NN mi
    # Regex: (\d+\.\d+) \s* (km|mi)
    dist_match = re.search(r'(\d+\.\d+)\s*(?:km|mi|KM)', text)
    if dist_match:
        distance = float(dist_match.group(1))
    
    # Duration: HH:MM:SS or MM:SS
    # 0:00:00 or 45:00
    dur_match = re.search(r'(\d{1,2}:\d{2}(?::\d{2})?)', text)
    if dur_match:
        duration_str = dur_match.group(1)
    else:
        # 30m 10s
        dur_match_2 = re.search(r'(\d{1,2})m\s*(\d{1,2})s', text)
        if dur_match_2:
            duration_str = f"00:{dur_match_2.group(1)}:{dur_match_2.group(2)}"

    return distance, duration_str

def get_filename_date(filename):
    # gio-yyyy-mon-dd.jpg
    match = re.search(r'(\d{4})-([a-z]{3})-(\d{2})', filename.lower())
    if match:
        y, m, d = match.groups()
        return f"{y}-{m}-{d}"
    return "Unknown"

def check_duplicates(base_dir, dry_run=False):
    if not os.path.exists(base_dir):
        print(f"Error: {base_dir} not found.")
        return

    print(f"Scanning {base_dir} for semantic duplicates...")
    
    # Data structure:
    # Date -> List of {file, dist, dur}
    runs_by_date = {}
    
    files = sorted([f for f in os.listdir(base_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    
    print(f"Found {len(files)} images.")
    
    for filename in files:
        filepath = os.path.join(base_dir, filename)
        f_date = get_filename_date(filename)
        
        # OCR
        text = extract_text(filepath)
        dist, dur = parse_stats(text)
        
        if f_date not in runs_by_date: runs_by_date[f_date] = []
        
        runs_by_date[f_date].append({
            "filename": filename,
            "filepath": filepath,
            "dist": dist,
            "dur": dur
        })
        
        # Progress log
        # print(f"  {filename}: {dist} km, {dur}")

    # Analyze
    deletion_candidates = []
    
    for date_key, run_list in runs_by_date.items():
        if len(run_list) < 2: continue
        
        # Group by (Dist, Dur) to find duplicates
        # We need a tolerant comparison for float, but exact for string duration usually ok from regex
        
        # bucket: (dist, dur) -> list of files
        buckets = {}
        
        for run in run_list:
            # If OCR failed (dist=0), treat as unique to be safe? 
            # Or if buckets has (0.0, "") it groups failures.
            # Let's only group if Dist > 0
            if run['dist'] == 0.0:
                 continue
                 
            key = (run['dist'], run['dur'])
            if key not in buckets: buckets[key] = []
            buckets[key].append(run)
            
        for stats, duplicates in buckets.items():
            if len(duplicates) > 1:
                # We have semantic duplicates!
                print(f"\n[Duplicate Set] Date: {date_key}, Stats: {stats[0]}km, {stats[1]}")
                
                # Sort: shortest filename length first (e.g. gio.jpg vs gio_1.jpg)
                duplicates.sort(key=lambda x: (len(x['filename']), x['filename']))
                
                keep = duplicates[0]
                remove_list = duplicates[1:]
                
                print(f"  > KEEP: {keep['filename']}")
                for rem in remove_list:
                    print(f"  > REMOVE: {rem['filename']}")
                    deletion_candidates.append(rem['filepath'])

    print(f"\nTotal semantic duplicates found: {len(deletion_candidates)}")
    
    if not dry_run and deletion_candidates:
        print("Deleting files...")
        for fpath in deletion_candidates:
            try:
                os.remove(fpath)
                print(f"Deleted {os.path.basename(fpath)}")
            except Exception as e:
                print(f"Error deleting {fpath}: {e}")
    elif dry_run and deletion_candidates:
        print("Dry run complete. No files deleted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    check_duplicates(args.dir, args.dry_run)
