import csv
import glob
import os
import re
from collections import defaultdict

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

def main():
    files = glob.glob('results/*.csv')
    
    # name -> date -> list of distances
    date_duplicates = defaultdict(lambda: defaultdict(list))
    # name -> distance -> list of dates
    dist_duplicates = defaultdict(lambda: defaultdict(list))
    
    for filepath in files:
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            try:
                headers = next(reader)
            except StopIteration:
                continue
                
            for row in reader:
                if not row or not row[0]: continue
                
                date_str = row[0]
                runners_str = row[1]
                runners = parse_runners_string(runners_str)
                
                for r in runners:
                    name = r['name']
                    dist = r['dist']
                    date_duplicates[name][date_str].append(dist)
                    dist_duplicates[name][dist].append(date_str)
                    
    print("=== MULTIPLE ENTRIES ON SAME DATE ===")
    found_date_dup = False
    for name, date_map in date_duplicates.items():
        for date_str, dists in date_map.items():
            if len(dists) > 1:
                print(f"{name} on {date_str}: {dists}")
                found_date_dup = True
    if not found_date_dup:
        print("None found.")
        
    print("\n=== EXACT SAME DISTANCE ON DIFFERENT DATES ===")
    found_dist_dup = False
    for name, dist_map in dist_duplicates.items():
        for dist, dates in dist_map.items():
            if len(dates) > 1:
                print(f"{name} ran {dist}km on {len(dates)} dates: {', '.join(dates)}")
                found_dist_dup = True
    if not found_dist_dup:
        print("None found.")

if __name__ == '__main__':
    main()
