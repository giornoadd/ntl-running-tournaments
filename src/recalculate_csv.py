import csv
import glob
import json
import os
import re
from datetime import datetime

def parse_runners_string(runners_str):
    runners = []
    if not runners_str:
        return runners
        
    parts = [p.strip() for p in runners_str.split(',')]
    for part in parts:
        if not part: continue
        match = re.search(r'([A-Za-z]+):\s*([\d\.]+)km', part)
        if match:
            runners.append({
                'name': match.group(1),
                'dist': float(match.group(2)),
                'original': part
            })
    return runners

from utils.config import determine_team, RUN_MIN_DISTANCE, WALK_MIN_DISTANCE, TEAM_SIZE

# Load activity types for walk detection
_ACTIVITY_TYPES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "activity_types.json")
try:
    with open(_ACTIVITY_TYPES_PATH, 'r', encoding='utf-8') as _f:
        _ACTIVITY_DATA = json.load(_f)
except FileNotFoundError:
    _ACTIVITY_DATA = {}

def is_walk_activity(name, date_str=None):
    """Check if a runner's activity is a walk (uses activity_types.json)."""
    key = name.lower()
    if key not in _ACTIVITY_DATA:
        return False
    data = _ACTIVITY_DATA[key]
    # Check per-date override first
    if date_str and date_str in data.get('overrides', {}):
        activity = data['overrides'][date_str].get('activity', '')
    else:
        activity = data.get('default_activity', '')
    return 'walk' in activity.lower()

MONTH_ORDER = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

def sort_key(filepath):
    """Sort results files chronologically by yyyy-Month."""
    basename = os.path.basename(filepath).replace('.csv', '')
    parts = basename.split('-')
    year = int(parts[0])
    month = MONTH_ORDER.index(parts[1]) if parts[1] in MONTH_ORDER else 0
    return (year, month)

def csv_to_md(csv_file):
    """Convert a CSV results file to its corresponding Markdown table."""
    md_file = csv_file.replace('.csv', '.md')
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
        md_lines = []
        title = os.path.basename(csv_file).replace('.csv', '')
        md_lines.append(f"# {title} Detailed Results\n")
        
        header_row = "| " + " | ".join(headers) + " |"
        separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"
        
        md_lines.append(header_row)
        md_lines.append(separator_row)
        
        for row in reader:
            md_lines.append("| " + " | ".join(row) + " |")
            
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_lines) + "\n")
    print(f"  -> Generated {md_file}")

QUARTER_MAP = {
    1: 'Q1', 2: 'Q1', 3: 'Q1',
    4: 'Q2', 5: 'Q2', 6: 'Q2',
    7: 'Q3', 8: 'Q3', 9: 'Q3',
    10: 'Q4', 11: 'Q4', 12: 'Q4',
}

def get_year_from_filepath(filepath):
    """Extract year from CSV filename like '2026-January.csv'."""
    basename = os.path.basename(filepath).replace('.csv', '')
    return int(basename.split('-')[0])

def recalculate_all():
    # Auto-discover all results CSV files and sort chronologically
    files = sorted(glob.glob('results/*.csv'), key=sort_key)
    
    if not files:
        print("No CSV files found in results/")
        return
    
    # State variables — reset per year
    manda_accum = 0.0
    itsys_accum = 0.0
    manda_count = TEAM_SIZE
    itsys_count = TEAM_SIZE
    current_year = None
    
    # Collect quarterly stats for README generation
    quarterly_stats = {}  # {(year, quarter): {manda_total, itsys_total}}
    monthly_stats = {}    # {filepath_basename: {manda_total, itsys_total}}
    runner_yearly_stats = {} # {year: {name: {'team': team, 'distance': 0.0}}}
    
    for filepath in files:
        file_year = get_year_from_filepath(filepath)
        
        # Reset accumulation when year changes
        if file_year != current_year:
            manda_accum = 0.0
            itsys_accum = 0.0
            current_year = file_year
        
        print(f"Processing {filepath}...")
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            rows = list(reader)
            
        output_rows = []
        manda_month_total = 0.0
        itsys_month_total = 0.0
        
        for row in rows:
            if not row or not row[0]: continue
            
            date_str = row[0]
            runners_str = row[1]
            runners = parse_runners_string(runners_str)
            
            valid_manda = []
            valid_itsys = []
            invalid_list = []
            
            for r in runners:
                is_valid = True
                walk = is_walk_activity(r['name'], date_str)
                if walk and r['dist'] < WALK_MIN_DISTANCE:
                    is_valid = False
                elif not walk and r['dist'] < RUN_MIN_DISTANCE:
                    is_valid = False
                
                if is_valid:
                    team = determine_team(r['name'])
                    if team == 'Mandalorian':
                        valid_manda.append(r)
                    elif team == 'IT System':
                        valid_itsys.append(r)
                else:
                    invalid_list.append(r)
                    
            manda_daily = sum(r['dist'] for r in valid_manda)
            itsys_daily = sum(r['dist'] for r in valid_itsys)
            
            if file_year not in runner_yearly_stats:
                runner_yearly_stats[file_year] = {}
            for r in valid_manda:
                name = r['name'].capitalize()
                if name not in runner_yearly_stats[file_year]:
                    runner_yearly_stats[file_year][name] = {'team': 'Mandalorian', 'distance': 0.0}
                runner_yearly_stats[file_year][name]['distance'] += r['dist']
            for r in valid_itsys:
                name = r['name'].capitalize()
                if name not in runner_yearly_stats[file_year]:
                    runner_yearly_stats[file_year][name] = {'team': 'IT System', 'distance': 0.0}
                runner_yearly_stats[file_year][name]['distance'] += r['dist']
            
            manda_accum += manda_daily
            itsys_accum += itsys_daily
            manda_month_total += manda_daily
            itsys_month_total += itsys_daily
            
            manda_avg = manda_accum / manda_count
            itsys_avg = itsys_accum / itsys_count
            
            valid_all_str = ", ".join([r['original'] for r in (valid_manda + valid_itsys)])
            
            invalid_str_parts = []
            for ir in invalid_list:
                walk = is_walk_activity(ir['name'], date_str)
                reason = "เดินไม่ถึง 2km" if walk else "น้อยกว่า 1km"
                base_str = re.sub(r'\(.*?\)', '', ir['original']).strip()
                invalid_str_parts.append(f"{base_str} ({reason})")
                
            invalid_str = ", ".join(invalid_str_parts)
            
            new_row = [
                date_str,
                valid_all_str,
                invalid_str,
                f"{manda_daily:.2f}" if manda_daily > 0 else "0",
                f"{manda_accum:.2f}",
                f"{manda_avg:.2f}",
                f"{itsys_daily:.2f}" if itsys_daily > 0 else "0",
                f"{itsys_accum:.2f}",
                f"{itsys_avg:.2f}"
            ]
            output_rows.append(new_row)
            
            # Track quarterly stats
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                qkey = (dt.year, QUARTER_MAP[dt.month])
                if qkey not in quarterly_stats:
                    quarterly_stats[qkey] = {'manda': 0.0, 'itsys': 0.0}
                quarterly_stats[qkey]['manda'] += manda_daily
                quarterly_stats[qkey]['itsys'] += itsys_daily
            except ValueError:
                pass
            
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(headers)
            writer.writerows(output_rows)
            print(f"  -> Saved {filepath}")
        
        # Generate corresponding MD file
        csv_to_md(filepath)
        
        # Track monthly stats
        month_key = os.path.basename(filepath).replace('.csv', '')
        monthly_stats[month_key] = {
            'manda': manda_month_total,
            'itsys': itsys_month_total,
            'year': file_year
        }
    
    # Generate results/README.md
    generate_results_readme(quarterly_stats, monthly_stats, runner_yearly_stats)


def generate_results_readme(quarterly_stats, monthly_stats, runner_yearly_stats=None):
    if runner_yearly_stats is None:
        runner_yearly_stats = {}
    """Generate results/README.md with yearly-quarterly statistics."""
    lines = []
    lines.append("# 📊 Running Competition: Results Tracker\n")
    lines.append("This directory contains the chronological statistics for the **Mandalorian vs IT System** Running Competition.\n")
    lines.append("---\n")
    
    # Group by year
    years = sorted(set(y for y, q in quarterly_stats.keys()), reverse=True)
    
    for year in years:
        year_quarters = sorted(
            [(q, s) for (y, q), s in quarterly_stats.items() if y == year],
            key=lambda x: ['Q1', 'Q2', 'Q3', 'Q4'].index(x[0])
        )
        
        # Year total
        year_manda = sum(s['manda'] for _, s in year_quarters)
        year_itsys = sum(s['itsys'] for _, s in year_quarters)
        year_manda_avg = year_manda / TEAM_SIZE
        year_itsys_avg = year_itsys / TEAM_SIZE
        leader = "💻 **IT System**" if year_itsys_avg > year_manda_avg else "⚔️ **Mandalorian**"
        lead_by = abs(year_itsys_avg - year_manda_avg)
        
        lines.append(f"## 🏆 {year} Tournament\n")
        lines.append("| Metric | ⚔️ Mandalorian | 💻 IT System | Leader |")
        lines.append("| :--- | ---: | ---: | :--- |")
        lines.append(f"| **Total Distance** | {year_manda:.2f} km | {year_itsys:.2f} km | {leader} |")
        lines.append(f"| **Average / Person** | {year_manda_avg:.2f} km | {year_itsys_avg:.2f} km | {leader} |")
        lines.append(f"\n> {leader} leads by **{lead_by:.2f} km/person**\n")
        
        if year in runner_yearly_stats:
            top_runners = sorted(runner_yearly_stats[year].items(), key=lambda x: x[1]['distance'], reverse=True)[:5]
            if top_runners:
                lines.append("### 🌟 Top 5 Individual Runners\n")
                lines.append("| Rank | Name | Team | Distance |")
                lines.append("| :---: | :--- | :--- | ---: |")
                medals = ["🥇 1", "🥈 2", "🥉 3", "🏅 4", "🏅 5"]
                for idx, (r_name, r_data) in enumerate(top_runners):
                    team_icon = "⚔️ Mandalorian" if r_data['team'] == 'Mandalorian' else "💻 IT System"
                    lines.append(f"| {medals[idx]} | {r_name} | {team_icon} | {r_data['distance']:.2f} km |")
                lines.append("")

        # Quarterly breakdown
        lines.append("### Quarterly Breakdown\n")
        lines.append("| Quarter | ⚔️ Mandalorian | 💻 IT System | Winner |")
        lines.append("| :--- | ---: | ---: | :--- |")
        
        for q, stats in year_quarters:
            q_manda_avg = stats['manda'] / TEAM_SIZE
            q_itsys_avg = stats['itsys'] / TEAM_SIZE
            q_winner = "💻 IT System" if q_itsys_avg > q_manda_avg else "⚔️ Mandalorian"
            if q_itsys_avg == q_manda_avg:
                q_winner = "🤝 Tie"
            lines.append(f"| **{q}** | {stats['manda']:.2f} km ({q_manda_avg:.2f} avg) | {stats['itsys']:.2f} km ({q_itsys_avg:.2f} avg) | {q_winner} |")
        
        lines.append("")
        
        # Monthly details
        lines.append("### Monthly Details\n")
        year_months = sorted(
            [(k, v) for k, v in monthly_stats.items() if v['year'] == year],
            key=lambda x: sort_key(f"results/{x[0]}.csv"),
            reverse=True
        )
        
        for month_key, stats in year_months:
            m_winner = "💻 IT System" if stats['itsys'] > stats['manda'] else "⚔️ Mandalorian"
            if stats['itsys'] == stats['manda']:
                m_winner = "🤝 Tie"
            lines.append(f"- **{month_key}** — Mandalorian: {stats['manda']:.2f} km | IT System: {stats['itsys']:.2f} km | {m_winner}")
            lines.append(f"  - 📋 [{month_key}.md]({month_key}.md) | 📄 [{month_key}.csv]({month_key}.csv)")
        
        lines.append("")
        lines.append("---\n")
    
    lines.append("*Auto-generated by `src/recalculate_csv.py`*\n")
    
    readme_path = os.path.join('results', 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"  -> Generated {readme_path}")


if __name__ == '__main__':
    recalculate_all()

