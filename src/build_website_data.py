#!/usr/bin/env python3
import csv
import glob
import json
import os
import re
from collections import defaultdict
from datetime import datetime

# --- Config ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
MEMBER_RESULTS_DIR = os.path.join(PROJECT_ROOT, "member_results")
HTML_DIR = os.path.join(PROJECT_ROOT, "docs", "html")

# Folder name -> (nickname_display, thai_name, team)
FOLDER_MAP = {
    "Manda-1_โจ (GIO)":        ("Gio", "โจ", "Mandalorian"),
    "Manda-2_โบ๊ท (Boat)":      ("Boat", "โบ๊ท", "Mandalorian"),
    "Manda-3_ต้อ (TORO)":       ("Toro", "ต้อ", "Mandalorian"),
    "Manda-4_เอ็ม (EM)":        ("Em", "เอ็ม", "Mandalorian"),
    "Manda-5_แซนด์ (SAND)":     ("Sand", "แซนด์", "Mandalorian"),
    "Manda-6_เป๊ก (peck)":      ("Peck", "เป๊ก", "Mandalorian"),
    "Manda-7_หนึ่ง (Neung)":    ("Neung", "หนึ่ง", "Mandalorian"),
    "Manda-8_ฟิวส์ (fuse)":     ("Fuse", "ฟิวส์", "Mandalorian"),
    "Manda-9_พี่ฉันท์ (Chan)":  ("Chan", "พี่ฉันท์", "Mandalorian"),
    "Manda-10_มอส (Mos)":      ("Mos", "มอส", "Mandalorian"),
    "ITSystem-1_Oat (โอ๊ต)":    ("Oat", "โอ๊ต", "IT System"),
    "ITSystem-2_Game (เกมส์)":   ("Game", "เกมส์", "IT System"),
    "ITSystem-3_O (โอ)":        ("O", "โอ", "IT System"),
    "ITSystem-4_Palm (ปาล์ม)":  ("Palm", "ปาล์ม", "IT System"),
    "ITSystem-5_Oum (อุ้ม)":    ("Oum", "อุ้ม", "IT System"),
    "ITSystem-6_Jojo (โจโจ้)":  ("Jojo", "โจโจ้", "IT System"),
    "ITSystem-7_Tae (เต)":      ("Tae", "เต", "IT System"),
    "ITSystem-8_Boy (บอย)":     ("Boy", "บอย", "IT System"),
    "ITSystem-9_Ton (ต้น)":     ("Ton", "ต้น", "IT System"),
    "ITSystem-10_PAN (แพน)":    ("PAN", "แพน", "IT System"),
}

# --- Shared Parsing logic from generate_member_readmes.py ---
def parse_runners(runners_str):
    if not runners_str or not runners_str.strip():
        return []
    results = []
    for part in runners_str.split(","):
        part = part.strip()
        m = re.match(r'([^:]+):\s*([\d.]+)\s*km', part, re.IGNORECASE)
        if m:
            results.append((m.group(1).strip(), float(m.group(2))))
    return results

def sort_csv_key(filepath):
    basename = os.path.splitext(os.path.basename(filepath))[0]
    months = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    parts = basename.split('-')
    year = int(parts[0])
    month = months.get(parts[1], 0)
    return (year, month)

def count_images_and_get_dates(folder_path, nickname_lower):
    pics_dir = os.path.join(folder_path, "running-pics")
    count = 0
    recent_images = []
    if not os.path.isdir(pics_dir):
        return 0, recent_images
    
    files = []
    for f in os.listdir(pics_dir):
        if re.match(r'^[a-z]+-\d{4}-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)-\d{2}', f, re.IGNORECASE):
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                count += 1
                files.append(f)
    
    # Simple sort to get recent ones at the end, then flip
    files.sort(reverse=True)
    # Give back the top 5 most recent image paths
    recent_images = [f"../member_results/{os.path.basename(folder_path)}/running-pics/{img}" for img in files[:5]]
    return count, recent_images

def find_image_files_for_date(folder_path, nickname_lower, date_str):
    """Find specific image paths for a given nickname and date."""
    pics_dir = os.path.join(folder_path, "running-pics")
    matches = []
    if not os.path.isdir(pics_dir):
        return matches
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        mon_abbr = dt.strftime("%b").lower()  # 'jan', 'feb', etc.
        day = dt.strftime("%d")
        year = dt.strftime("%Y")
    except ValueError:
        return []
    prefix = f"{nickname_lower}-{year}-{mon_abbr}-{day}"
    for f in os.listdir(pics_dir):
        f_lower = f.lower()
        if f_lower.endswith(('.jpg', '.jpeg', '.png')):
            name_part = os.path.splitext(f)[0].lower()
            if name_part == prefix or name_part.startswith(prefix + '_'):
                matches.append(f"../member_results/{os.path.basename(folder_path)}/running-pics/{f}")
    matches.sort()
    return matches

def load_personal_stats_details(folder_path):
    stats_path = os.path.join(folder_path, "personal-statistics.md")
    details = {
        'run_dist': 0.0, 'walk_dist': 0.0,
        'run_count': 0, 'walk_count': 0, 'total_sessions': 0,
        'best_pace': None, 'best_pace_activity': '', 'best_pace_date': '',
        'longest_run_dist': 0.0, 'longest_run_activity': '', 'longest_run_date': '',
    }
    if not os.path.isfile(stats_path):
        return details
    try:
        with open(stats_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line.startswith('|'):
                    continue
                cols = [c.strip() for c in line.split('|')]
                if len(cols) < 6:
                    continue
                date_val = cols[1]
                activity_val = cols[2]
                dist_val = cols[3]
                pace_val = cols[5] if len(cols) > 5 else ''

                if not re.match(r'\d{4}-\d{2}-\d{2}', date_val):
                    continue

                dist_match = re.search(r'([\d.]+)\s*km', dist_val)
                dist = float(dist_match.group(1)) if dist_match else 0.0

                details['total_sessions'] += 1
                is_walk = 'walk' in activity_val.lower()

                if is_walk:
                    details['walk_dist'] += dist
                    details['walk_count'] += 1
                else:
                    details['run_dist'] += dist
                    details['run_count'] += 1

                    if dist > details['longest_run_dist']:
                        details['longest_run_dist'] = dist
                        details['longest_run_activity'] = activity_val
                        details['longest_run_date'] = date_val

                    pace_match = re.search(r'(\d+):(\d+)/km', pace_val)
                    if pace_match:
                        pace_mins = int(pace_match.group(1))
                        pace_secs = int(pace_match.group(2))
                        pace_total = pace_mins * 60 + pace_secs
                        if details['best_pace'] is None or pace_total < details['best_pace']:
                            details['best_pace'] = pace_total
                            details['best_pace_activity'] = activity_val
                            details['best_pace_date'] = date_val

    except Exception:
        pass
    return details

def build_data():
    os.makedirs(HTML_DIR, exist_ok=True)
    
    # Gather CSV data
    csv_files = sorted(glob.glob(os.path.join(RESULTS_DIR, "*.csv")), key=sort_csv_key)
    
    # {nickname_lower: {month_label: [(date_str, distance)]}}
    member_data = defaultdict(lambda: defaultdict(list))
    
    # Also collect formatted history data mapped by date, resembling results/*.md
    # schema: { 
    #   "date": "2026-03-01", 
    #   "month": "2026-March", 
    #   "runners_list": [...],
    #   "mando_daily": 0, "it_daily": 0
    # }
    grouped_activities = {}

    for csv_path in csv_files:
        basename = os.path.splitext(os.path.basename(csv_path))[0]
        if not basename.startswith("2026"):
            continue
            
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if not row or not row[0].strip():
                    continue
                date_str = row[0].strip()
                runners_str = row[1] if len(row) > 1 else ""
                runners = parse_runners(runners_str)
                
                if date_str not in grouped_activities:
                    grouped_activities[date_str] = {
                        "date": date_str,
                        "month": basename,
                        "runners_list": [],
                        "mando_daily": 0.0,
                        "it_daily": 0.0,
                    }

                for name, dist in runners:
                    member_data[name.lower()][basename].append((date_str, dist))
                    
                    user_folder = ""
                    team_name = ""
                    for raw_f, (d_name, t_name, team) in FOLDER_MAP.items():
                        if d_name.lower() == name.lower():
                            user_folder = os.path.join(MEMBER_RESULTS_DIR, raw_f)
                            team_name = team
                            break
                            
                    images = find_image_files_for_date(user_folder, name.lower(), date_str) if user_folder else []
                    
                    grouped_activities[date_str]["runners_list"].append({
                        "name": name,
                        "distance": dist,
                        "team": team_name,
                        "images": images
                    })
                    
                    if team_name == "Mandalorian":
                        grouped_activities[date_str]["mando_daily"] += dist
                    elif team_name == "IT System":
                        grouped_activities[date_str]["it_daily"] += dist
    
    # Sort grouped activities by date
    sorted_dates = sorted(grouped_activities.keys())
    
    # Calculate Accumulates
    mando_accum = 0.0
    it_accum = 0.0
    history_array = []
    
    for d in sorted_dates:
        act = grouped_activities[d]
        mando_accum += act["mando_daily"]
        it_accum += act["it_daily"]
        
        act["mando_accum"] = round(mando_accum, 2)
        act["it_accum"] = round(it_accum, 2)
        act["mando_avg"] = round(mando_accum / 10, 2) # Div by 10 members
        act["it_avg"] = round(it_accum / 10, 2)
        
        # Format daily totals nicely
        act["mando_daily"] = round(act["mando_daily"], 2)
        act["it_daily"] = round(act["it_daily"], 2)
        
        history_array.append(act)

    # Reverse to show newest first for the history view
    history_array.reverse()
    
    # Build complete rosters
    roster = []
    
    # Calculate Team Stats
    teams = {
        "Mandalorian": { "total_distance": 0.0, "members": 0, "active_members": 0, "name": "Mandalorian", "avg_distance": 0.0 },
        "IT System": { "total_distance": 0.0, "members": 0, "active_members": 0, "name": "IT System", "avg_distance": 0.0 }
    }
    
    for folder_name, (display_name, thai_name, team) in FOLDER_MAP.items():
        nickname_lower = display_name.lower()
        folder_path = os.path.join(MEMBER_RESULTS_DIR, folder_name)
        
        m_data = member_data.get(nickname_lower, {})
        
        total_distance = 0.0
        active_days = 0
        
        for month_label, entries in m_data.items():
            for date_str, dist in entries:
                total_distance += dist
                active_days += 1
                
        teams[team]["total_distance"] += total_distance
        teams[team]["members"] += 1
        if total_distance > 0:
            teams[team]["active_members"] += 1
            
        # Get extra details
        stats_details = load_personal_stats_details(folder_path) if os.path.isdir(folder_path) else None
        image_count, recent_images = count_images_and_get_dates(folder_path, nickname_lower) if os.path.isdir(folder_path) else (0, [])
        
        md_readme = ""
        md_stats = ""
        md_plan = ""
        md_coach = ""

        if os.path.isdir(folder_path):
            def get_fixed_md(filename):
                file_path = os.path.join(folder_path, filename)
                if not os.path.isfile(file_path):
                    return ""
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Replace relative (running-pics/...) to (../member_results/<folder>/running-pics/...)
                fix_path = f"../member_results/{folder_name}/running-pics/"
                content = content.replace("(running-pics/", f"({fix_path}")
                return content
                
            md_readme = get_fixed_md("README.md")
            md_stats = get_fixed_md("personal-statistics.md")
            md_plan = get_fixed_md("running-plan.md")
            md_coach = get_fixed_md("coach-analysis.md")
        
        member_obj = {
            "nickname": display_name,
            "thai_name": thai_name,
            "team": team,
            "total_distance": round(total_distance, 2),
            "active_days": active_days,
            "image_count": image_count,
            "recent_images": recent_images,
            "stats_details": stats_details,
            "markdown": {
                "readme": md_readme,
                "statistics": md_stats,
                "plan": md_plan,
                "coach_analysis": md_coach
            }
        }
        roster.append(member_obj)
        
    for team_name, t in teams.items():
        if t["members"] > 0:
            # According to rules, average is divided by 10 members (total members)
            t["avg_distance"] = round(t["total_distance"] / 10, 2)
        t["total_distance"] = round(t["total_distance"], 2)

    roster.sort(key=lambda x: x["total_distance"], reverse=True)
    
    # Update timestamp
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    final_data = {
        "last_updated": last_updated,
        "teams": teams,
        "roster": roster,
        "activities": history_array
    }
    
    js_content = f"// Auto-generated by build_website_data.py\nwindow.COMPETITION_DATA = {json.dumps(final_data, indent=2, ensure_ascii=False)};\n"
    
    output_path = os.path.join(HTML_DIR, "data.js")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"✅ Generated {output_path} successfully.")

if __name__ == '__main__':
    build_data()
