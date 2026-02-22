import csv
import re

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

from utils.config import determine_team

def recalculate_all():
    # Process files in chronological order
    files = ['results/2026-January.csv', 'results/2026-February.csv']
    
    # State variables span ACROSS files
    manda_accum = 0.0
    itsys_accum = 0.0
    manda_count = 10
    itsys_count = 10
    
    for filepath in files:
        print(f"Processing {filepath}...")
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            rows = list(reader)
            
        output_rows = []
        
        for row in rows:
            if not row or not row[0]: continue
            
            date_str = row[0]
            # Ignore anything before 2026-01-01
            if date_str < '2026-01-01':
                continue
                
            runners_str = row[1]
            runners = parse_runners_string(runners_str)
            
            valid_manda = []
            valid_itsys = []
            invalid_list = []
            
            for r in runners:
                is_valid = True
                if r['dist'] < 1.0:
                    is_valid = False
                elif r['name'].lower() == 'sand' and r['dist'] < 2.0:
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
            
            manda_accum += manda_daily
            itsys_accum += itsys_daily
            
            manda_avg = manda_accum / manda_count
            itsys_avg = itsys_accum / itsys_count
            
            valid_all_str = ", ".join([r['original'] for r in (valid_manda + valid_itsys)])
            
            invalid_str_parts = []
            for ir in invalid_list:
                reason = "น้อยกว่า 1km"
                if ir['name'].lower() == 'sand': reason = "เดินไม่ถึง 2km"
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
            
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(headers)
            writer.writerows(output_rows)
            print(f"  -> Saved {filepath}")

if __name__ == '__main__':
    recalculate_all()
