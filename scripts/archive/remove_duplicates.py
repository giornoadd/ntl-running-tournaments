
import os
import hashlib
import argparse

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

def find_and_remove_duplicates(base_dir, dry_run=False):
    if not os.path.exists(base_dir):
        print(f"Error: Directory not found: {base_dir}")
        return

    print(f"Scanning for duplicates in: {base_dir}")
    
    # map hash -> list of filepaths
    hashes = {}
    
    for root, dirs, files in os.walk(base_dir):
        files.sort()
        for filename in files:
            if filename.startswith('.'): continue
            
            filepath = os.path.join(root, filename)
            file_hash = get_file_hash(filepath)
            
            if file_hash:
                if file_hash not in hashes:
                    hashes[file_hash] = []
                hashes[file_hash].append(filepath)

    duplicates_found = 0
    deleted_count = 0
    
    for file_hash, file_list in hashes.items():
        if len(file_list) > 1:
            duplicates_found += 1
            # Sort to determine which one to keep
            # Criteria: Shortest name first, then alphabetical
            # e.g. gio-2023-apr-10.jpg vs gio-2023-apr-10_1.jpg -> keep first
            file_list.sort(key=lambda x: (len(os.path.basename(x)), os.path.basename(x)))
            
            keep = file_list[0]
            remove = file_list[1:]
            
            print(f"Duplicate Group ({file_hash[:8]}...):")
            print(f"  [Keep] {os.path.basename(keep)}")
            
            for f in remove:
                if dry_run:
                    print(f"  [DryRun Delete] {os.path.basename(f)}")
                else:
                    try:
                        os.remove(f)
                        print(f"  [Deleted] {os.path.basename(f)}")
                        deleted_count += 1
                    except Exception as e:
                        print(f"  [Error Deleting] {os.path.basename(f)}: {e}")
            print("-" * 20)

    if dry_run:
        print(f"Finished scan. Found {duplicates_found} groups of duplicates.")
    else:
        print(f"Finished. Deleted {deleted_count} duplicate files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--dir", required=True)
    args = parser.parse_args()
    
    find_and_remove_duplicates(args.dir, args.dry_run)
