import os
import re
import argparse
import subprocess
import json
from datetime import datetime
from PIL import Image, ImageEnhance
import time

# Regex patterns
DISTANCE_PATTERNS = [
    r'(\d+\.\d+)\s*km',       # 5.02 km
    r'(\d+\.\d+)\s*mi',       # 3.12 mi
    r'(\d+\.\d+)',            # Just a number (fallback, risky)
]

DURATION_PATTERNS = [
    r'(\d{1,2}):(\d{2}):(\d{2})',   # 00:30:00
    r'(\d{1,2})m\s*(\d{1,2})s',     # 30m 12s
    r'(\d{1,2})\'(\d{1,2})\"',      # 30'12"
]

def preprocess_image(image_path):
    try:
        img = Image.open(image_path)
        img = img.convert('L') # Grayscale
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        
        temp_path = f"temp_stats_{os.getpid()}_{int(time.time()*1000)}.png"
        img.save(temp_path)
        return temp_path
    except:
        return None

def extract_text(image_path):
    temp_path = preprocess_image(image_path)
    target_path = temp_path if temp_path else image_path
    
    try:
        # psm 6 Assume a single uniform block of text? Or 3 (default)?
        # 11: Sparse text. Good for HUDs.
        result = subprocess.run(['tesseract', target_path, 'stdout', '--psm', '11'], capture_output=True, text=True)
        text = result.stdout
    except Exception as e:
        print(f"OCR Error: {e}")
        text = ""
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            
    return text

def parse_stats(text):
    distance = 0.0
    duration_seconds = 0
    
    # Distance
    # We look for lines with "km" specifically to be safe
    # Or just largest number with decimal?
    # Runners usually have "Distance" label.
    
    # Simple logic: Find pattern (\d+\.\d+) km
    km_match = re.search(r'(\d+\.\d+)\s*(?:km|KM|Km)', text)
    if km_match:
        distance = float(km_match.group(1))
    else:
        # Fallback: look for just X.XX
        # This is noisy. Let's stick to explicit units for now or common labels.
        pass

    # Duration
    # 00:00:00
    dur_match = re.search(r'(\d{1,2}):(\d{2}):(\d{2})', text)
    if dur_match:
        h, m, s = map(int, dur_match.groups())
        duration_seconds = h*3600 + m*60 + s
    else:
        # 30m 12s
        dur_match_2 = re.search(r'(\d{1,2})m\s*(\d{1,2})s', text)
        if dur_match_2:
            m, s = map(int, dur_match_2.groups())
            duration_seconds = m*60 + s
            
    return distance, duration_seconds

def get_team_and_member(folder_name):
    # ITSystem-1_Oat (โอ๊ต) -> Team: ITSystem, Member: Oat (โอ๊ต)
    # Manda-1_โจ (GIO) -> Team: Manda, Member: โจ (GIO)
    parts = folder_name.split('-')
    if len(parts) >= 2:
        team_prefix = parts[0] # ITSystem or Manda
        # The rest is member ID and name, need to split carefully
        # Actually just "ITSystem" or "Manda" is enough for team.
        return team_prefix, folder_name
    return "Unknown", folder_name

def analyze_directory(base_dir):
    stats = [] # List of dicts
    
    # Manual Data Overrides (Filename -> {dist, dur})
    MANUAL_DATA = {
        # Gio
        "gio-07-feb-2026.jpg": {"dist": 9.09, "dur": 0},
        "gio-05-feb-2026.jpg": {"dist": 6.24, "dur": 0},
        "gio-03-feb-2026.jpg": {"dist": 7.71, "dur": 0},
        "gio-02-feb-2026.jpg": {"dist": 6.02, "dur": 0},
        "gio-31-jan-2026.jpg": {"dist": 8.4, "dur": 0},
        "gio-29-jan-2026.jpg": {"dist": 6.1, "dur": 0},
        "gio-26-jan-2026.jpg": {"dist": 5.0, "dur": 0},
        "gio-24-jan-2026.jpg": {"dist": 8.0, "dur": 0},
        "gio-22-jan-2026.jpg": {"dist": 5.5, "dur": 0},
        "gio-16-jan-2026.jpg": {"dist": 3.1, "dur": 0},
        "gio-11-jan-2026.jpg": {"dist": 6.1, "dur": 0},
        "gio-06-jan-2026.jpg": {"dist": 2.3, "dur": 0},
        # Sand (Duration only provided, roughly)
        "sand-07-feb-2026.jpg": {"dist": 0, "dur": 541}, # 9m 1s
        "sand-07-feb-2026_2.jpg": {"dist": 0, "dur": 1880}, # 31m 20s
        "sand-07-feb-2026_3.jpg": {"dist": 0, "dur": 2048}, # 34m 8s
        "sand-07-feb-2026_4.jpg": {"dist": 0, "dur": 2123}, # 35m 23s
        "sand-07-feb-2026_5.jpg": {"dist": 0, "dur": 1196}, # 19m 56s
        "sand-07-feb-2026_6.jpg": {"dist": 0, "dur": 2181}, # 36m 21s
        "sand-07-feb-2026_7.jpg": {"dist": 0, "dur": 2181}, # 36m 21s
        "sand-07-feb-2026_8.jpg": {"dist": 0, "dur": 2356}, # 39m 16s
        "sand-07-feb-2026_9.jpg": {"dist": 0, "dur": 2448}, # 40m 48s
        "sand-07-feb-2026_10.jpg": {"dist": 0, "dur": 2742}, # 45m 42s
        "sand-07-feb-2026_11.jpg": {"dist": 0, "dur": 2820}, # 47m 0s
        "sand-07-feb-2026_12.jpg": {"dist": 0, "dur": 2834}, # 47m 14s
    }

    for root, dirs, files in os.walk(base_dir):
        folder_name = os.path.basename(root)
        if root == base_dir: continue
        
        team, member = get_team_and_member(folder_name)
        
        print(f"Processing {member}... (Found {len(files)} files)")
        
        for filename in files:
            # print(f"  Checking {filename}...")
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                # print(f"  Skipping {filename} (extension mismatch)")
                continue
                
            # Parse Date from Filename (We rely on our renames!)
            # Format: nickname-dd-mon-yyyy.jpg or nickname-dd-mon-yyyy_N.jpg
            # nick-name-07-feb-2026.jpg
            
            # Simple dash split might fail if nickname has dashes.
            # But our renames use dashes.
            # Let's use regex for the date part at the end.
            
            date_match = re.search(r'(\d{2}-[a-zA-Z]{3}-\d{4})', filename)
            date_str = date_match.group(1) if date_match else "Unknown"
            
            if filename.lower() in MANUAL_DATA:
                manual = MANUAL_DATA[filename.lower()]
                dist = manual["dist"]
                dur = manual["dur"]
                print(f"  [Manual Override] {filename} -> {dist} km, {dur} sec")
            else:
                # Fallback to OCR if not in manual list
                filepath = os.path.join(root, filename)
                text = extract_text(filepath)
                dist, dur = parse_stats(text)
                
            stats.append({
                "Team": team,
                "Member": member,
                "Date": date_str,
                "Distance": dist,
                "Duration": dur,
                "File": filename
            })
            if dist > 0 or dur > 0:
                 print(f"  {filename} -> {dist} km, {dur} sec (Date: {date_str})")
            
    return stats

def generate_report(stats):
    # Aggregation
    # Date | Team | Total Distance | Avg Distance | Total Duration
    
    # 1. Group by Date, then Team
    data = {} # date -> team -> {dist_sum, count, dur_sum}
    
    for s in stats:
        d = s["Date"]
        t = s["Team"]
        if d not in data: data[d] = {}
        if t not in data[d]: data[d][t] = {"dist": 0.0, "count": 0, "dur": 0}
        
        data[d][t]["dist"] += s["Distance"]
        data[d][t]["dur"] += s["Duration"]
        # Only count if distance > 0? Or just participation?
        # User asked for AVG. If distance is 0, it drags down avg.
        # Let's count all files as "runs".
        data[d][t]["count"] += 1

    # Sort dates
    try:
        sorted_dates = sorted(data.keys(), key=lambda x: datetime.strptime(x, "%d-%b-%Y") if x != "Unknown" else datetime.min)
    except:
        sorted_dates = sorted(data.keys())

    with open("report.md", "w") as f:
        f.write("\n# Daily Running Report\n\n")
        f.write("| Date | Team | Total Distance (km) | Avg Distance (km) | Total Duration | Activity Count |\n")
        f.write("|---|---|---|---|---|---|\n")
        
        for d in sorted_dates:
            for t in ["Manda", "ITSystem"]: # Force order
                if t in data[d]:
                    row = data[d][t]
                    avg = row["dist"] / row["count"] if row["count"] > 0 else 0
                    dur_fmt = time.strftime('%H:%M:%S', time.gmtime(row["dur"]))
                    f.write(f"| {d} | {t} | {row['dist']:.2f} | {avg:.2f} | {dur_fmt} | {row['count']} |\n")
    print("Report generated in report.md")

if __name__ == "__main__":
    base_dir = "member_results"
    stats = analyze_directory(base_dir)
    generate_report(stats)
