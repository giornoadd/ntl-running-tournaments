import csv
import os
import glob

def csv_to_md(csv_file, md_file):
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
        md_lines = []
        md_lines.append(f"# {os.path.basename(csv_file).replace('.csv', '')} Detailed Results\n")
        
        # Format headers
        header_row = "| " + " | ".join(headers) + " |"
        separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"
        
        md_lines.append(header_row)
        md_lines.append(separator_row)
        
        for row in reader:
            md_lines.append("| " + " | ".join(row) + " |")
            
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_lines) + "\n")
    print(f"Created {md_file}")

for csv_path in glob.glob("results/*.csv"):
    md_path = csv_path.replace(".csv", ".md")
    csv_to_md(csv_path, md_path)
