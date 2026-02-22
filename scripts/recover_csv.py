import os, glob

for md_file in glob.glob('results/2026-*.md'):
    csv_file = md_file.replace('.md', '.csv')
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    csv_rows = []
    for line in lines:
        if line.startswith('| '):
            if '| ---' in line:
                continue
            # Parse md row
            parts = [p.strip() for p in line.strip().split('|')[1:-1]]
            # Add quotes back to runners if comma exists
            if ',' in parts[1]:
                parts[1] = f'"{parts[1]}"'
            if len(parts) > 2 and ',' in parts[2]:
                 parts[2] = f'"{parts[2]}"'
            csv_rows.append(','.join(parts))
            
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(csv_rows) + '\n')
    print(f"Recovered {csv_file}")
