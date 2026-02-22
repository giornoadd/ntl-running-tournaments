
import os
import argparse
import time
from datetime import datetime
from utils import files, ocr, dates

# Manual Data Overrides (Filename -> {dist, dur})
# Ideally this should be loaded from a JSON file.
MANUAL_DATA = {
    # Gio
    "gio-2026-feb-07.jpg": {"dist": 9.09, "dur": 0},
    "gio-2026-feb-05.jpg": {"dist": 6.24, "dur": 0},
    "gio-2026-feb-03.jpg": {"dist": 7.71, "dur": 0},
    "gio-2026-feb-02.jpg": {"dist": 6.02, "dur": 0},
    "gio-2026-jan-31.jpg": {"dist": 8.4, "dur": 0},
    "gio-2026-jan-29.jpg": {"dist": 6.1, "dur": 0},
    "gio-2026-jan-26.jpg": {"dist": 5.0, "dur": 0},
    "gio-2026-jan-24.jpg": {"dist": 8.0, "dur": 0},
    "gio-2026-jan-22.jpg": {"dist": 5.5, "dur": 0},
    "gio-2026-jan-16.jpg": {"dist": 3.1, "dur": 0},
    "gio-2026-jan-11.jpg": {"dist": 6.1, "dur": 0},
    "gio-2026-jan-06.jpg": {"dist": 2.3, "dur": 0},
    # Sand (Duration only provided, roughly)
    "sand-2026-feb-07.jpg": {"dist": 0, "dur": 541}, # 9m 1s
    "sand-2026-feb-07_1.jpg": {"dist": 0, "dur": 1880}, # 31m 20s
    # Add more as needed based on old script but updated filenames
}

def analyze_directory(base_dir, use_ocr=False):
    stats = [] # List of dicts
    
    print(f"Scanning {base_dir} for report generation...")
    
    for root, dirs, _ in os.walk(base_dir):
        if root == base_dir: continue
        
        folder_name = os.path.basename(root)
        # Assuming folder format: Team-MemberID_Name (Nick)
        # e.g. Manda-1_Jo (Gio)
        
        parts = folder_name.split('-')
        team = parts[0] if len(parts) > 0 else "Unknown"
        nickname = files.get_nickname(folder_name)
        if not nickname: nickname = folder_name
        
        img_files = [f for f in os.listdir(root) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        for filename in img_files:
            filepath = os.path.join(root, filename)
            
            # Parse Date
            dt = dates.parse_date_from_filename(filename)
            date_str = dt.strftime("%Y-%m-%d") if dt else "Unknown"
            
            # Get Stats
            dist = 0.0
            dur = 0
            
            # Check Manual
            if filename.lower() in MANUAL_DATA:
                m = MANUAL_DATA[filename.lower()]
                dist = m.get("dist", 0)
                dur = m.get("dur", 0)
                # print(f"  [Manual] {filename}: {dist} km")
            elif use_ocr:
                # OCR
                text = ocr.extract_text(filepath)
                dist, dur_str = ocr.extract_distance_duration(text)
                # Convert dur_str to seconds if needed, but report just needs display
                # Let's keep distinct seconds logic if we want to sum duration.
                # For now, OCR returns str.
                pass
            
            stats.append({
                "Team": team,
                "Member": nickname,
                "Date": date_str,
                "Distance": dist,
                "Duration": dur, # Seconds or str? Let's assume numeric for manual, ignore str for now
                "File": filename
            })
            
    return stats

def generate_markdown_report(stats, output_file="report.md"):
    # Aggregate by Date -> Team -> Stats
    data = {}
    
    for s in stats:
        d = s["Date"]
        t = s["Team"]
        if d not in data: data[d] = {}
        if t not in data[d]: data[d][t] = {"dist": 0.0, "count": 0}
        
        data[d][t]["dist"] += s["Distance"]
        data[d][t]["count"] += 1
        
    sorted_dates = sorted(data.keys())
    
    with open(output_file, "w") as f:
        f.write("# Daily Running Report\n\n")
        f.write("| Date | Team | Total Distance (km) | Avg Distance (km) | Activity Count |\n")
        f.write("|---|---|---|---|---|\n")
        
        for d in sorted_dates:
            for t in ["Manda", "ITSystem"]:
                if t in data[d]:
                    row = data[d][t]
                    avg = row["dist"] / row["count"] if row["count"] > 0 else 0
                    f.write(f"| {d} | {t} | {row['dist']:.2f} | {avg:.2f} | {row['count']} |\n")
                    
    print(f"Report generated: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="/Users/giornoadd/my-macos/running-comp/member_results")
    parser.add_argument("--ocr", action="store_true", help="Enable OCR for stats (slow)")
    parser.add_argument("--output", default="report.md")
    args = parser.parse_args()
    
    stats = analyze_directory(args.dir, args.ocr)
    generate_markdown_report(stats, args.output)
