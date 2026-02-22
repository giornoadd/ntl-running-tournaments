import os
import re

source_file = '/Users/giornoadd/my-macos/running-comp/Team member list.md'
base_dir = '/Users/giornoadd/my-macos/running-comp/member_results'

if not os.path.exists(base_dir):
    os.makedirs(base_dir)

with open(source_file, 'r') as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()
    if '|' in line:
        parts = line.split('|')
        id_part = parts[0].strip()
        name_part = parts[1].strip()
        
        # Clean name part to be filesystem friendlier
        # ID is usually safe (Manda-1), Name might have parenthesis
        # Let's format as ID_Name
        # Remove special chars from name if needed, but keeping it simple is usually fine on macOS
        # actually let's just use the ID as the key part, but include the name for readability
        # Extract English name from parenthesis if available, or just use the whole thing?
        # User said "Result of each person".
        # Let's try to extract the English name inside parenthesis if possible for shorter folder names, 
        # but the full string "Manda-1_โจ (GIO)" is also fine and descriptive.
        # Let's simple sanitize the name part.
        safe_name = name_part.replace('/', '_').replace(':', '')
        folder_name = f"{id_part}_{safe_name}"
        
        full_path = os.path.join(base_dir, folder_name)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            print(f"Created: {folder_name}")
        else:
            print(f"Exists: {folder_name}")
