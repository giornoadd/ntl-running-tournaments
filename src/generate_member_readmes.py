#!/usr/bin/env python3
"""Generate individual README.md for each member under member_results/."""

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

# Load OCR-verified activity types
ACTIVITY_TYPES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "activity_types.json")
try:
    with open(ACTIVITY_TYPES_PATH, 'r', encoding='utf-8') as _f:
        ACTIVITY_DATA = json.load(_f)
except (FileNotFoundError, json.JSONDecodeError):
    ACTIVITY_DATA = {}

MONTH_ABBR = {
    'jan': 'January', 'feb': 'February', 'mar': 'March', 'apr': 'April',
    'may': 'May', 'jun': 'June', 'jul': 'July', 'aug': 'August',
    'sep': 'September', 'oct': 'October', 'nov': 'November', 'dec': 'December'
}


def parse_runners(runners_str):
    """Parse 'GIO: 4.53km, Sand: 2.55km' into list of (name, distance)."""
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
    """Sort CSV files chronologically."""
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


def count_images(folder_path):
    """Count renamed image files in a member folder's running-pics/ subfolder."""
    pics_dir = os.path.join(folder_path, "running-pics")
    count = 0
    if not os.path.isdir(pics_dir):
        return 0
    for f in os.listdir(pics_dir):
        if re.match(r'^[a-z]+-\d{4}-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)-\d{2}', f, re.IGNORECASE):
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                count += 1
    return count


def get_image_dates(folder_path, nickname_lower):
    """Get set of dates that have image evidence in running-pics/ subfolder."""
    pics_dir = os.path.join(folder_path, "running-pics")
    dates = set()
    if not os.path.isdir(pics_dir):
        return dates
    pattern = re.compile(
        rf'^{re.escape(nickname_lower)}-(\d{{4}})-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)-(\d{{2}})',
        re.IGNORECASE
    )
    for f in os.listdir(pics_dir):
        m = pattern.match(f)
        if m and f.lower().endswith(('.jpg', '.jpeg', '.png')):
            year, mon, day = m.group(1), m.group(2).lower(), m.group(3)
            dates.add(f"{year}-{mon}-{day}")
    return dates


def find_image_files(folder_path, nickname_lower, date_str):
    """Find image files matching a date_str like '2026-01-15' for a member.
    Searches in running-pics/ subfolder.
    Returns list of filenames sorted (base first, then _1, _2, etc)."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        mon_abbr = dt.strftime("%b").lower()  # 'jan', 'feb', etc.
        day = dt.strftime("%d")
        year = dt.strftime("%Y")
    except ValueError:
        return []

    # Pattern: nickname-YYYY-mon-DD[_N].(jpg|jpeg|png)
    prefix = f"{nickname_lower}-{year}-{mon_abbr}-{day}"
    pics_dir = os.path.join(folder_path, "running-pics")
    matches = []
    if not os.path.isdir(pics_dir):
        return matches
    for f in os.listdir(pics_dir):
        f_lower = f.lower()
        if f_lower.endswith(('.jpg', '.jpeg', '.png')):
            # Match exact prefix (with or without _N suffix before extension)
            name_part = os.path.splitext(f)[0].lower()
            if name_part == prefix or name_part.startswith(prefix + '_'):
                matches.append(f)
    # Sort: base file first, then _1, _2, etc.
    matches.sort(key=lambda x: (os.path.splitext(x)[0].lower().replace(prefix, ''), x))
    return matches


def format_evidence_links(image_files):
    """Create markdown links for image files in running-pics/ subfolder."""
    if not image_files:
        return ""
    if len(image_files) == 1:
        path = f"running-pics/{image_files[0]}".replace(' ', '%20')
        return f"[📸]({path})"
    links = []
    for i, f in enumerate(image_files, 1):
        path = f"running-pics/{f}".replace(' ', '%20')
        links.append(f"[📸{i}]({path})")
    return " ".join(links)


def load_personal_stats_activities(folder_path):
    """Load activity names from personal-statistics.md for each date.
    Returns dict: {date_str: [activity_name, ...]} (multiple per date possible)."""
    stats_path = os.path.join(folder_path, "personal-statistics.md")
    activities = defaultdict(list)
    if not os.path.isfile(stats_path):
        return activities
    try:
        with open(stats_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line.startswith('|'):
                    continue
                cols = [c.strip() for c in line.split('|')]
                # cols[0] is empty (before first |), cols[1]=date, cols[2]=activity, ...
                if len(cols) < 4:
                    continue
                date_val = cols[1]
                activity_val = cols[2]
                # Skip header rows
                if date_val in ('วันที่', ':---', ''):
                    continue
                if not re.match(r'\d{4}-\d{2}-\d{2}', date_val):
                    continue
                if activity_val:
                    activities[date_val].append(activity_val)
    except (IOError, UnicodeDecodeError):
        pass
    return activities


def load_personal_stats_details(folder_path):
    """Parse personal-statistics.md for detailed metrics.
    Returns dict with: run_dist, walk_dist, run_count, walk_count, total_sessions,
    best_pace, best_pace_activity, best_pace_date, cadence_values,
    longest_long_run, longest_long_run_activity, longest_long_run_date."""
    stats_path = os.path.join(folder_path, "personal-statistics.md")
    details = {
        'run_dist': 0.0, 'walk_dist': 0.0,
        'run_count': 0, 'walk_count': 0, 'total_sessions': 0,
        'best_pace': None, 'best_pace_activity': '', 'best_pace_date': '',
        'cadence_values': [],
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
                cadence_val = cols[8] if len(cols) > 8 else ''

                if not re.match(r'\d{4}-\d{2}-\d{2}', date_val):
                    continue

                # Parse distance
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

                    # Track longest run (exclude walks)
                    if dist > details['longest_run_dist']:
                        details['longest_run_dist'] = dist
                        details['longest_run_activity'] = activity_val
                        details['longest_run_date'] = date_val

                    # Parse pace (format: "8:17/km" or "7:27/km")
                    pace_match = re.search(r'(\d+):(\d+)/km', pace_val)
                    if pace_match:
                        pace_mins = int(pace_match.group(1))
                        pace_secs = int(pace_match.group(2))
                        pace_total = pace_mins * 60 + pace_secs
                        if details['best_pace'] is None or pace_total < details['best_pace']:
                            details['best_pace'] = pace_total
                            details['best_pace_activity'] = activity_val
                            details['best_pace_date'] = date_val

                    # Parse cadence
                    cad_match = re.search(r'(\d+)\s*spm', cadence_val)
                    if cad_match:
                        cad = int(cad_match.group(1))
                        if not is_walk and cad > 80:  # filter out walk cadences
                            details['cadence_values'].append(cad)
    except (IOError, UnicodeDecodeError):
        pass
    return details


def get_activity_info(nickname_lower, date_str=None, stats_activities=None):
    """Get activity type for a member. Priority:
    1. personal-statistics.md (specific session names from running plan)
    2. activity_types.json overrides (per-date)
    3. activity_types.json default
    """
    # 1. Check personal-statistics.md first
    if date_str and stats_activities:
        names = stats_activities.get(date_str, [])
        if names:
            # Combine all activities for this date with ' + '
            combined = ' + '.join(names)
            emoji = "🚶" if all('walk' in n.lower() for n in names) else "🏃"
            if len(names) > 1 and any('walk' in n.lower() for n in names):
                # Mixed run+walk: use run emoji
                emoji = "🏃"
            label = f"{emoji} {combined}"
            return label, names[0]

    # 2. Check activity_types.json
    member_info = ACTIVITY_DATA.get(nickname_lower, {})
    if not member_info:
        return "🏃 Run", "Run"

    # Check for per-date override
    if date_str and 'overrides' in member_info:
        override = member_info['overrides'].get(date_str)
        if override:
            activity = override.get('activity', member_info.get('default_activity', 'Run'))
            activity_thai = override.get('activity_thai', '')
            emoji = "🚶" if 'walk' in activity.lower() else "🏃"
            label = f"{emoji} {activity}"
            if activity_thai:
                label += f" ({activity_thai})"
            return label, activity

    # 3. Use default
    activity = member_info.get('default_activity', 'Run')
    activity_thai = member_info.get('default_activity_thai', '')
    emoji = "🚶" if 'walk' in activity.lower() else "🏃"
    label = f"{emoji} {activity}"
    if activity_thai:
        label += f" ({activity_thai})"
    return label, activity


def format_date_display(date_str):
    """Convert 2026-01-15 to a nicer display like 'Wed, Jan 15'."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%a, %b %d")
    except ValueError:
        return date_str


def extract_preserved_sections(readme_path):
    """Extract manually-added sections between All-Time Summary and monthly data.
    These sections (HR Zones, Goals, Coaching Methods, etc.) should be preserved
    when regenerating the README."""
    if not os.path.isfile(readme_path):
        return []
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (IOError, UnicodeDecodeError):
        return []

    lines = content.split('\n')
    # Find the end of All-Time Summary (last line of the summary table)
    summary_end = -1
    monthly_start = -1
    auto_gen_marker = -1

    for i, line in enumerate(lines):
        # The All-Time Summary table ends after the last row starting with |
        if '## 📊 All-Time Summary' in line:
            # Find end of this table
            for j in range(i + 1, len(lines)):
                if lines[j].strip().startswith('|'):
                    summary_end = j
                elif summary_end > 0 and not lines[j].strip().startswith('|'):
                    summary_end = j
                    break

        # Monthly sections start with ## 📅
        if line.strip().startswith('## 📅') and monthly_start == -1 and summary_end > 0:
            monthly_start = i
            break

        # Or the separator before monthly data
        if line.strip() == '---' and summary_end > 0 and monthly_start == -1:
            # Check if next non-empty line is a monthly header
            for j in range(i + 1, min(i + 3, len(lines))):
                if lines[j].strip().startswith('## 📅'):
                    monthly_start = i
                    break
            if monthly_start > 0:
                break

    if summary_end > 0 and monthly_start > summary_end:
        preserved = lines[summary_end:monthly_start]
        # Strip leading/trailing empty lines but keep content
        while preserved and not preserved[0].strip():
            preserved.pop(0)
        while preserved and not preserved[-1].strip():
            preserved.pop()
        # Only return if there's actual content (not just ---)
        content_lines = [l for l in preserved if l.strip() and l.strip() != '---']
        if content_lines:
            return preserved

    return []


def generate_all_readmes():
    # 1. Discover and sort all CSV files
    csv_files = sorted(glob.glob(os.path.join(RESULTS_DIR, "*.csv")), key=sort_csv_key)

    if not csv_files:
        print("No CSV files found in results/")
        return

    # 2. Build per-member data
    # {nickname_lower: {month_label: [(date_str, distance)]}}
    member_data = defaultdict(lambda: defaultdict(list))

    for csv_path in csv_files:
        basename = os.path.splitext(os.path.basename(csv_path))[0]

        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip headers
            for row in reader:
                if not row or not row[0].strip():
                    continue
                date_str = row[0].strip()
                runners_str = row[1] if len(row) > 1 else ""
                runners = parse_runners(runners_str)

                for name, dist in runners:
                    member_data[name.lower()][basename].append((date_str, dist))

    # 3. Generate README for each folder
    generated = 0
    for folder_name, (display_name, thai_name, team) in FOLDER_MAP.items():
        folder_path = os.path.join(MEMBER_RESULTS_DIR, folder_name)
        if not os.path.isdir(folder_path):
            continue

        nickname_lower = display_name.lower()
        m_data = member_data.get(nickname_lower, {})

        # Calculate all-time stats
        total_distance = 0.0
        active_days = 0
        max_distance = 0.0
        max_date = ""
        all_distances = []

        for month_label, entries in m_data.items():
            for date_str, dist in entries:
                total_distance += dist
                active_days += 1
                all_distances.append(dist)
                if dist > max_distance:
                    max_distance = dist
                    max_date = date_str

        image_count = count_images(folder_path)
        avg_distance = total_distance / active_days if active_days > 0 else 0.0
        # Load per-date activities from personal-statistics.md
        stats_activities = load_personal_stats_activities(folder_path)
        # Load detailed stats (run/walk breakdown, pace, cadence)
        stats_details = load_personal_stats_details(folder_path)
        activity_label, default_activity = get_activity_info(nickname_lower)
        member_info = ACTIVITY_DATA.get(nickname_lower, {})
        app_used = member_info.get('app', 'Unknown')
        has_running_plan = os.path.isfile(os.path.join(folder_path, 'running-plan.md'))

        # Determine first and last active dates
        all_dates = []
        for entries in m_data.values():
            for date_str, _ in entries:
                all_dates.append(date_str)
        all_dates.sort()
        first_date = all_dates[0] if all_dates else "N/A"
        last_date = all_dates[-1] if all_dates else "N/A"

        # --- Build README ---
        lines = []
        lines.append(f"# 🏃 {display_name} ({thai_name})")
        lines.append("")
        lines.append(f"> Personal running statistics for the **Running Competition 2026**")
        lines.append("")

        # Profile card
        lines.append("## 👤 Profile")
        lines.append("")
        lines.append(f"| | |")
        lines.append(f"| :--- | :--- |")
        lines.append(f"| **Name** | {display_name} ({thai_name}) |")
        team_emoji = '🪖' if team == 'Mandalorian' else '💻'
        lines.append(f"| **Team** | {team_emoji} {team} |")
        # Determine activity label based on stats
        if stats_details['walk_count'] > 0 and stats_details['run_count'] > 0:
            profile_activity = "🏃 Hybrid (Running + Morning Walk)"
        else:
            profile_activity = activity_label
        lines.append(f"| **Primary Activity** | {profile_activity} |")
        if has_running_plan:
            lines.append(f"| **Training Plan** | 📝 Running Plan (running-plan.md) |")
        lines.append(f"| **Tracking App** | 📱 {app_used} |")
        lines.append(f"| **Member Since** | {first_date} |")
        lines.append("")

        # All-time summary (enhanced with personal-statistics.md data)
        lines.append("## 📊 All-Time Summary")
        lines.append("")
        lines.append(f"| Metric | Value |")
        lines.append(f"| :--- | :--- |")
        # Total distance with breakdown if stats available
        if stats_details['total_sessions'] > 0 and stats_details['walk_count'] > 0:
            lines.append(f"| **Total Distance** | 🔥 **{total_distance:.2f} km** (Running {stats_details['run_dist']:.2f} km + Walk {stats_details['walk_dist']:.2f} km) |")
        else:
            lines.append(f"| **Total Distance** | 🔥 **{total_distance:.2f} km** |")
        lines.append(f"| **Active Days** | 📅 {active_days} days |")
        if stats_details['total_sessions'] > 0 and stats_details['walk_count'] > 0:
            lines.append(f"| **Total Sessions** | 📋 {stats_details['total_sessions']} sessions (Running {stats_details['run_count']} + Walk {stats_details['walk_count']}) |")
        lines.append(f"| **Average / Session** | 📏 {avg_distance:.2f} km |")
        lines.append(f"| **Best Session** | 🏆 {max_distance:.2f} km ({max_date}) |")
        # Best pace from personal-statistics.md
        if stats_details['best_pace'] is not None:
            bp_mins = stats_details['best_pace'] // 60
            bp_secs = stats_details['best_pace'] % 60
            lines.append(f"| **Best Pace** | ⚡ {bp_mins}:{bp_secs:02d}/km \u2014 {stats_details['best_pace_activity']} ({stats_details['best_pace_date']}) |")
        # Longest Long Run
        if stats_details['longest_run_dist'] > 0:
            lines.append(f"| **Longest Run** | 🏅 {stats_details['longest_run_dist']:.2f} km \u2014 {stats_details['longest_run_activity']} ({stats_details['longest_run_date']}) |")
        # Avg cadence
        if stats_details['cadence_values']:
            avg_cad = sum(stats_details['cadence_values']) // len(stats_details['cadence_values'])
            lines.append(f"| **Avg Running Cadence** | 🦶 {avg_cad} spm |")
        lines.append(f"| **Evidence Files** | 📸 {image_count} screenshots |")
        lines.append(f"| **First Active** | {first_date} |")
        lines.append(f"| **Last Active** | {last_date} |")
        lines.append("")

        # Preserve manually-added sections (HR Zones, Goals, Coaching Methods, etc.)
        readme_path = os.path.join(folder_path, "README.md")
        preserved = extract_preserved_sections(readme_path)
        if preserved:
            for pline in preserved:
                lines.append(pline)
            lines.append("")

        # Monthly sections (reverse chronological)
        sorted_months = sorted(m_data.keys(), key=lambda x: sort_csv_key(os.path.join(RESULTS_DIR, x + ".csv")), reverse=True)

        lines.append("---")
        lines.append("")

        for month_label in sorted_months:
            entries = m_data[month_label]
            if not entries:
                continue

            month_total = sum(dist for _, dist in entries)
            month_days = len(entries)
            month_avg = month_total / month_days if month_days > 0 else 0.0
            month_best = max(dist for _, dist in entries)

            lines.append(f"## 📅 {month_label}")
            lines.append(f"> {month_days} sessions · {month_total:.2f} km total · {month_avg:.2f} km avg · best {month_best:.2f} km")
            lines.append("")
            lines.append("| # | Date | Day | Distance | Activity | Evidence |")
            lines.append("| :---: | :--- | :--- | :--- | :--- | :---: |")

            for i, (date_str, dist) in enumerate(entries, 1):
                day_name = format_date_display(date_str)
                activity_display, _ = get_activity_info(nickname_lower, date_str, stats_activities)
                image_files = find_image_files(folder_path, nickname_lower, date_str)
                evidence_links = format_evidence_links(image_files)
                lines.append(f"| {i} | {date_str} | {day_name} | **{dist:.2f} km** | {activity_display} | {evidence_links} |")

            lines.append("")

        # If no data
        if not m_data:
            lines.append("")
            lines.append("*No running data recorded yet.* 🏁")
            lines.append("")

        lines.append("---")
        lines.append(f"*Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
        lines.append("")

        readme_path = os.path.join(folder_path, "README.md")
        with open(readme_path, 'w') as f:
            f.write("\n".join(lines))

        print(f"  ✅ {display_name:6s} | {total_distance:7.2f} km | {active_days:2d} days | {image_count:2d} images | {readme_path}")
        generated += 1

    print(f"\n🎉 Generated {generated} individual README files.")


if __name__ == "__main__":
    generate_all_readmes()
