
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
        
        temp_path = f"temp_chan_{os.getpid()}_{int(time.time()*1000)}.png"
        img.save(temp_path)
        return temp_path
    except:
        return None

def extract_text(image_path):
    temp_path = preprocess_image(image_path)
    target_path = temp_path if temp_path else image_path
    
    text = ""
    try:
        # psm 11: Sparse text for HUDs/Screenshots
        result = subprocess.run(['tesseract', target_path, 'stdout', '--psm', '11'], capture_output=True, text=True)
        text = result.stdout
    except Exception as e:
        print(f"OCR Error for {image_path}: {e}")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
    return text

def parse_datetime(text):
    # Pattern: 1/25/2026, 6:07 PM
    # Regex for date and optional time
    # Try specific format first
    
    # Match: 1/25/2026, 6:07 PM
    match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4}),\s*(\d{1,2}:\d{2}\s*(?:AM|PM))', text)
    if match:
        m, d, y, t_str = match.groups()
        dt_str = f"{m}/{d}/{y} {t_str}"
        try:
            return datetime.strptime(dt_str, "%m/%d/%Y %I:%M %p")
        except ValueError:
            pass

    # Fallback: Just date?
    match_d = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', text)
    if match_d:
        m, d, y = match_d.groups()
        try:
            return datetime.strptime(f"{m}/{d}/{y}", "%m/%d/%Y")
        except ValueError:
            pass
            
    return None

def rename_chan_files(base_dir, dry_run=False):
    if not os.path.exists(base_dir):
        print(f"Error: {base_dir} not found.")
        return

    print(f"Scanning {base_dir}...")
    files = [f for f in os.listdir(base_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    # Store tuples of (datetime, original_filename)
    results = []
    
    for filename in files:
        filepath = os.path.join(base_dir, filename)
        text = extract_text(filepath)
        dt = parse_datetime(text)
        
        if dt:
            results.append((dt, filename))
            print(f"  [OCR] {filename} -> {dt}")
        else:
            print(f"  [OCR] {filename} -> No date found")
            
    # Sort by datetime to ensure correct order (_1, _2...)
    results.sort(key=lambda x: x[0])
    
    # Rename
    # Target: chan-yyyy-mon-dd.jpg
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    
    # Track usage of filenames to handle collisions across buckets if needed?
    # Actually, if dates are same, we just increment counter.
    # But since we sorted, we can just process sequentially and check existence?
    # Better: grouping by date string to manage counters locally for that date.
    
    processed_counts = {} # date_str -> count
    
    for dt, filename in results:
        y = dt.year
        mo_str = months[dt.month - 1]
        d = dt.day
        
        base_name = f"chan-{y}-{mo_str}-{d:02d}"
        
        if base_name not in processed_counts:
            processed_counts[base_name] = 0
            
        count = processed_counts[base_name]
        suffix = "" if count == 0 else f"_{count}"
        processed_counts[base_name] += 1
        
        _, ext = os.path.splitext(filename)
        new_filename = f"{base_name}{suffix}{ext}"
        
        old_path = os.path.join(base_dir, filename)
        new_path = os.path.join(base_dir, new_filename)
        
        if filename == new_filename:
            print(f"  [Skip] {filename} already correct.")
            continue
            
        if dry_run:
            print(f"  [DryRun] {filename} -> {new_filename}")
        else:
            try:
                os.rename(old_path, new_path)
                print(f"  [Renamed] {filename} -> {new_filename}")
            except Exception as e:
                print(f"  [Error] {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="/Users/giornoadd/my-macos/running-comp/member_results/Manda-9_พี่ฉันท์ (Chan)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    rename_chan_files(args.dir, args.dry_run)
