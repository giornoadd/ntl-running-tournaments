import os

base_dir = "member_results/ITSystem-9_Ton (ต้น)"

# Current state:
# - ton-27-jan-2026.jpg exists (Target for file 1, but likely holds content of file 2)
# - ton-27-jan-2026.JPEG exists (File 1)

# Goal:
# 1. Rename ton-27-jan-2026.jpg -> ton-27-jan-2026_2.jpg
# 2. Rename ton-27-jan-2026.JPEG -> ton-27-jan-2026.jpg

file_jpg = os.path.join(base_dir, "ton-27-jan-2026.jpg")
file_jpeg = os.path.join(base_dir, "ton-27-jan-2026.JPEG")
target_2 = os.path.join(base_dir, "ton-27-jan-2026_2.jpg")

if os.path.exists(file_jpg):
    print(f"Renaming collision: {file_jpg} -> {target_2}")
    os.rename(file_jpg, target_2)
else:
    print(f"Warning: {file_jpg} not found!")

if os.path.exists(file_jpeg):
    print(f"Renaming source: {file_jpeg} -> {file_jpg}")
    os.rename(file_jpeg, file_jpg)
else:
    print(f"Warning: {file_jpeg} not found!")
