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
    """Count renamed image files in a member folder."""
    count = 0
    if not os.path.isdir(folder_path):
        return 0
    for f in os.listdir(folder_path):
        if re.match(r'^[a-z]+-\d{4}-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)-\d{2}', f, re.IGNORECASE):
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                count += 1
    return count


def get_image_dates(folder_path, nickname_lower):
    """Get set of dates that have image evidence."""
    dates = set()
    if not os.path.isdir(folder_path):
        return dates
    pattern = re.compile(
        rf'^{re.escape(nickname_lower)}-(\d{{4}})-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)-(\d{{2}})',
        re.IGNORECASE
    )
    for f in os.listdir(folder_path):
        m = pattern.match(f)
        if m and f.lower().endswith(('.jpg', '.jpeg', '.png')):
            year, mon, day = m.group(1), m.group(2).lower(), m.group(3)
            dates.add(f"{year}-{mon}-{day}")
    return dates


def find_image_files(folder_path, nickname_lower, date_str):
    """Find image files matching a date_str like '2026-01-15' for a member.
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
    matches = []
    if not os.path.isdir(folder_path):
        return matches
    for f in os.listdir(folder_path):
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
    """Create markdown links for image files."""
    if not image_files:
        return ""
    if len(image_files) == 1:
        return f"[📸]({image_files[0].replace(' ', '%20')})"
    return " ".join(f"[📸{i}]({f.replace(' ', '%20')})" for i, f in enumerate(image_files, 1))


def get_activity_info(nickname_lower, date_str=None):
    """Get OCR-verified activity type for a member, with optional per-date override."""
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

    # Use default
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
        activity_label, default_activity = get_activity_info(nickname_lower)
        member_info = ACTIVITY_DATA.get(nickname_lower, {})
        app_used = member_info.get('app', 'Unknown')

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
        lines.append(f"| **Team** | {'⚔️' if team == 'Mandalorian' else '💻'} {team} |")
        lines.append(f"| **Primary Activity** | {activity_label} |")
        lines.append(f"| **Tracking App** | 📱 {app_used} |")
        lines.append(f"| **Member Since** | {first_date} |")
        lines.append("")

        # All-time summary
        lines.append("## 📊 All-Time Summary")
        lines.append("")
        lines.append(f"| Metric | Value |")
        lines.append(f"| :--- | :--- |")
        lines.append(f"| **Total Distance** | 🔥 **{total_distance:.2f} km** |")
        lines.append(f"| **Active Days** | 📅 {active_days} days |")
        lines.append(f"| **Average / Session** | 📏 {avg_distance:.2f} km |")
        lines.append(f"| **Best Session** | 🏆 {max_distance:.2f} km ({max_date}) |")
        lines.append(f"| **Evidence Files** | 📸 {image_count} screenshots |")
        lines.append(f"| **First Active** | {first_date} |")
        lines.append(f"| **Last Active** | {last_date} |")
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
                activity_display, _ = get_activity_info(nickname_lower, date_str)
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
