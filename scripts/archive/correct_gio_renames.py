import os

base_dir = "member_results/Manda-1_โจ (GIO)"

# Renames: (Old Name in Directory, New Target Name)
renames = [
    # 1. gio-07-feb-2026_1.JPEG -> gio-07-feb-2026.jpg
    ("gio-07-feb-2026_1.JPEG", "gio-07-feb-2026.jpg"),
    
    # 2. gio-07-feb-2026_8.JPEG (was renamed to gio-22-jan-2026.jpg) -> gio-05-feb-2026.jpg
    ("gio-22-jan-2026.jpg", "gio-05-feb-2026.jpg"),

    # 3. gio-07-feb-2026_16.JPEG (was renamed to gio-24-jan-2026.jpg) -> gio-03-feb-2026.jpg
    ("gio-24-jan-2026.jpg", "gio-03-feb-2026.jpg"),
    
    # 4. gio-07-feb-2026_14.JPEG -> gio-02-feb-2026.jpg
    ("gio-07-feb-2026_14.JPEG", "gio-02-feb-2026.jpg")
]

print(f"Applying corrections in: {base_dir}")

if not os.path.exists(base_dir):
    print(f"Error: Directory not found: {base_dir}")
    exit(1)

success_count = 0
for old_name, new_name in renames:
    old_path = os.path.join(base_dir, old_name)
    new_path = os.path.join(base_dir, new_name)
    
    # Check if old file exists
    if not os.path.exists(old_path):
        print(f"[Skip] Source file not found: {old_name}")
        # Maybe it was already renamed? Check target.
        if os.path.exists(new_path):
            print(f"       -> Target {new_name} already exists.")
        continue

    # Check collision
    if os.path.exists(new_path):
        print(f"[Collision] Target {new_name} exists. Skipping {old_name}.")
        continue

    try:
        os.rename(old_path, new_path)
        print(f"[OK] {old_name} -> {new_name}")
        success_count += 1
    except Exception as e:
        print(f"[Error] Failed to rename {old_name}: {e}")

print(f"Finished. Renamed {success_count}/{len(renames)} files.")
