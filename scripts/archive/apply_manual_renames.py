import os

# List of renames. Order matters to avoid collisions.
# (Old Name, New Name)
renames = [
    ("gio-07-feb-2026_5.JPEG", "gio-31-jan-2026.jpg"),
    ("gio-07-feb-2026.JPEG", "gio-29-jan-2026.jpg"),
    ("gio-07-feb-2026_2.JPEG", "gio-26-jan-2026.jpg"),
    ("gio-07-feb-2026_16.JPEG", "gio-24-jan-2026.jpg"),
    ("gio-07-feb-2026_8.JPEG", "gio-22-jan-2026.jpg"),
    ("gio-07-feb-2026_13.JPEG", "gio-16-jan-2026.jpg"),
    ("gio-07-feb-2026_10.JPEG", "gio-11-jan-2026.jpg"),
    ("gio-07-feb-2026_12.JPEG", "gio-06-jan-2026.jpg")
]

base_dir = "member_results"

print(f"Scanning {base_dir} to apply manual renames...")

# Helper to find file recursively
def find_file(filename, search_root):
    for root, dirs, files in os.walk(search_root):
        if filename in files:
            return os.path.join(root, filename)
    return None

success_count = 0
for old_name, new_name in renames:
    old_path = find_file(old_name, base_dir)
    
    if old_path:
        folder = os.path.dirname(old_path)
        new_path = os.path.join(folder, new_name)
        
        # Check if new_path exists
        if os.path.exists(new_path):
            # If it's the same file (case insensitive check on mac/windows potentially), we might just be renaming case/extension
            if os.path.normcase(old_path) == os.path.normcase(new_path):
                # Just rename
                pass
            else:
                # True collision
                print(f"Conflict: Target {new_name} exists. Skipping {old_name}.")
                continue
        
        try:
            os.rename(old_path, new_path)
            print(f"[OK] {old_name} -> {new_name}")
            success_count += 1
        except Exception as e:
            print(f"[Error] Failed to rename {old_name}: {e}")
    else:
        print(f"[Skip] Source file not found: {old_name}")

print(f"Finished. Renamed {success_count}/{len(renames)} files.")
