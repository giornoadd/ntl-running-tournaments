
import os
import argparse
import hashlib
from utils import files, ocr, dates

def get_file_hash(filepath):
    """
    Calculate MD5 hash of a file.
    """
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(65536)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def deduplicate_binary(base_dir, dry_run=False):
    print(f"Scanning {base_dir} for BINARY duplicates (MD5)...")
    
    hashes = {} # hash -> list of filepaths
    
    for root, dirs, files in os.walk(base_dir):
        files.sort()
        for filename in files:
            if filename.startswith('.'): continue
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png')): continue
            
            filepath = os.path.join(root, filename)
            file_hash = get_file_hash(filepath)
            
            if file_hash:
                if file_hash not in hashes: hashes[file_hash] = []
                hashes[file_hash].append(filepath)

    count = 0
    for file_hash, file_list in hashes.items():
        if len(file_list) > 1:
            # Sort: shortest name first
            file_list.sort(key=lambda x: (len(os.path.basename(x)), os.path.basename(x)))
            
            keep = file_list[0]
            remove = file_list[1:]
            
            print(f"  [Binary Duplicate] Hash: {file_hash[:8]}...")
            print(f"    > KEEP: {os.path.basename(keep)}")
            
            for f in remove:
                if dry_run:
                    print(f"    > REMOVE (DryRun): {os.path.basename(f)}")
                else:
                    try:
                        os.remove(f)
                        print(f"    > REMOVED: {os.path.basename(f)}")
                        count += 1
                    except Exception as e:
                        print(f"    > ERROR: {e}")
                        
    print(f"Binary deduplication complete. Removed {count} files.")

def deduplicate_semantic(base_dir, dry_run=False):
    print(f"Scanning {base_dir} for SEMANTIC duplicates (OCR)...")
    
    for root, dirs, _ in os.walk(base_dir):
        if root == base_dir: continue 
        
        # Filter for known member folders if needed, or just run on everything
        # if "ITSystem-" not in os.path.basename(root) and "Manda-" not in os.path.basename(root): continue
             
        files_by_date = {}
        img_files = [f for f in os.listdir(root) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if not img_files: continue
        
        # print(f"Checking {os.path.basename(root)} ({len(img_files)} files)...")

        for filename in img_files:
            filepath = os.path.join(root, filename)
            if not os.path.exists(filepath): continue # Might have been deleted by binary check
            
            dt = dates.parse_date_from_filename(filename)
            if not dt: continue
            
            date_key = dt.strftime("%Y-%m-%d")
            
            # Extract semantic stats
            text = ocr.extract_text(filepath)
            dist, dur = ocr.extract_distance_duration(text)
            
            if date_key not in files_by_date: files_by_date[date_key] = []
            files_by_date[date_key].append({
                "filename": filename,
                "filepath": filepath,
                "dist": dist,
                "dur": dur
            })
            
        deletion_candidates = []
        
        for d_key, runs in files_by_date.items():
            if len(runs) < 2: continue
            
            buckets = {}
            for r in runs:
                if r['dist'] == 0: continue 
                
                key = (r['dist'], r['dur'])
                if key not in buckets: buckets[key] = []
                buckets[key].append(r)
                
            for stats, duplicates in buckets.items():
                if len(duplicates) > 1:
                    print(f"  [Semantic Duplicate] {d_key} | Stats: {stats}")
                    duplicates.sort(key=lambda x: (len(x['filename']), x['filename']))
                    
                    keep = duplicates[0]
                    remove = duplicates[1:]
                    
                    print(f"    > KEEP: {keep['filename']}")
                    for rem in remove:
                        print(f"    > REMOVE: {rem['filename']}")
                        deletion_candidates.append(rem['filepath'])
                        
        if deletion_candidates:
            if dry_run:
                print(f"  [DryRun] Would delete {len(deletion_candidates)} semantic duplicates.")
            else:
                for fpath in deletion_candidates:
                    try:
                        os.remove(fpath)
                        print(f"  [Deleted] {os.path.basename(fpath)}")
                    except Exception as e:
                        print(f"  [Error] {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="/Users/giornoadd/my-macos/running-comp/member_results")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--mode", choices=["binary", "semantic", "all"], default="all")
    args = parser.parse_args()
    
    if args.mode in ["binary", "all"]:
        deduplicate_binary(args.dir, args.dry_run)
        
    if args.mode in ["semantic", "all"]:
        deduplicate_semantic(args.dir, args.dry_run)
