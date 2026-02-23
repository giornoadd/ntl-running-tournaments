import os
import glob
import hashlib
from collections import defaultdict

def md5(fname):
    hash_md5 = hashlib.md5()
    try:
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    except FileNotFoundError:
        return None
    return hash_md5.hexdigest()

def main():
    # Find all images in member_results
    search_pattern = 'member_results/**/*.*'
    files = glob.glob(search_pattern, recursive=True)
    
    # Filter for image extensions typically used
    image_exts = {'.jpg', '.jpeg', '.png', '.HEIC', '.heic'}
    images = [f for f in files if os.path.splitext(f)[1].lower() in image_exts]
    
    # hash -> list of file paths
    hash_map = defaultdict(list)
    
    for img in images:
        h = md5(img)
        if h:
            hash_map[h].append(img)
            
    print("=== IDENTICAL FILES (BY MD5) ===")
    found_dup = False
    for h, paths in hash_map.items():
        if len(paths) > 1:
            print(f"Hash {h[:8]} shared by:")
            for p in paths:
                print(f"  - {p}")
            found_dup = True
            
    if not found_dup:
        print("No identical files found.")

if __name__ == '__main__':
    main()
