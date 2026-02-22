import os
import csv
import re
import glob

# Ensure we can import utils
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from utils.files import get_nickname

def parse_csv(filepath):
    """Read CSV into a list of dictionaries with headers."""
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def extract_personal_distance(runners_str, target_name):
    """
    Given 'Oat: 4.06km, Jojo: 2.35km', find 'Jojo' and return 2.35. 
    Return 0 if not found.
    """
    if not runners_str:
        return 0.0
    
    parts = [p.strip() for p in runners_str.split(',')]
    for part in parts:
        if not part: continue
        match = re.search(r'([A-Za-z]+):\s*([\d\.]+)km', part)
        if match:
            name = match.group(1).lower()
            if name == target_name.lower():
                return float(match.group(2))
    return 0.0

def generate_personal_readme(member_folder, csv_files):
    folder_name = os.path.basename(member_folder)
    nickname = get_nickname(folder_name)
    
    if not nickname:
        print(f"Skipping {folder_name} - cannot extract nickname.")
        return

    # To calculate Total statistics
    total_km = 0.0
    total_days = 0
    
    md_lines = []
    md_lines.append(f"# 🏃‍♂️ Personal Stats: {folder_name.split('_')[1]}")
    md_lines.append("")
    md_lines.append(f"This is the automated detailed running log for **{nickname.capitalize()}**.")
    md_lines.append("")
    
    for csv_file in csv_files:
        month_name = os.path.basename(csv_file).replace('.csv', '')
        rows = parse_csv(csv_file)
        
        # Filter rows where this user ran
        user_runs = []
        for row in rows:
            dist = extract_personal_distance(row.get('Runners', ''), nickname)
            if dist > 0:
                user_runs.append({
                    'Date': row['Date'],
                    'Distance': f"{dist:.2f} km",
                    'Team Score Input': row.get('Runners', '')  # Context of who else ran
                })
                total_km += dist
                total_days += 1
                
        if user_runs:
            md_lines.append(f"## 📅 {month_name}")
            md_lines.append("| Date | Distance | Full Team Daily Context |")
            md_lines.append("| :--- | :--- | :--- |")
            for run in user_runs:
                md_lines.append(f"| {run['Date']} | **{run['Distance']}** | {run['Team Score Input']} |")
            md_lines.append("")
    
    # If no runs found across all CSVs
    if total_days == 0:
         md_lines.append("> ⚠️ No valid running data found for this period.")
         md_lines.append("")
    
    # Prepend summary overview right under the title
    summary_lines = [
        "## 📊 Accumulative Summary",
        f"- **Total Distance Ran:** `{total_km:.2f} km`",
        f"- **Active Days:** `{total_days} days`",
        "---"
    ]
    
    md_lines.insert(4, "\n".join(summary_lines))
    
    # Save the file
    readme_path = os.path.join(member_folder, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_lines) + "\n")
    print(f"Generated {readme_path} ({total_km:.2f} km)")

def main():
    base_dir = "member_results"
    # Find all CSV files and sort chronologically
    csv_files = sorted(glob.glob("results/2026-*.csv"))
    
    # Find all member folders
    member_folders = [f.path for f in os.scandir(base_dir) if f.is_dir()]
    
    for folder in member_folders:
        generate_personal_readme(folder, csv_files)

if __name__ == '__main__':
    main()
