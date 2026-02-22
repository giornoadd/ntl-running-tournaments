import os
import shutil
import time
from datetime import datetime

# Setup test environment
test_base = "/Users/giornoadd/my-macos/running-comp/test_member_results"
if os.path.exists(test_base):
    shutil.rmtree(test_base)
os.makedirs(test_base)

# Create a test folder mimicking user structure
test_folder_name = "ITSystem-9_Ton (ต้น)"
folder_path = os.path.join(test_base, test_folder_name)
os.makedirs(folder_path)

# Create dummy file with specific time
# Goal: ton-29-jan-2026
# 29 Jan 2026 12:00:00
target_time = datetime(2026, 1, 29, 12, 0, 0)
timestamp = target_time.timestamp()

filepath = os.path.join(folder_path, "evidence.png")
with open(filepath, 'w') as f:
    f.write("dummy content")

# Set mtime
os.utime(filepath, (timestamp, timestamp))

print(f"Created test file at: {filepath}")
print(f"Target timestamp: {target_time}")

# Run the script
import sys
sys.path.append("/Users/giornoadd/my-macos/running-comp/script")
# We need to import the script module to run its function or execute via os.system
# Since the script is not in python path directly and has if name == main block, let's call via os.system
cmd = f"python3 /Users/giornoadd/my-macos/running-comp/script/rename_files.py --dir {test_base}"
print(f"Running command: {cmd}")
os.system(cmd)

# Verify
expected_name = "ton-29-jan-2026.png"
expected_path = os.path.join(folder_path, expected_name)

if os.path.exists(expected_path):
    print("SUCCESS: File renamed correctly!")
else:
    print("FAILURE: File not renamed correctly.")
    print("Files in directory:")
    print(os.listdir(folder_path))

# Cleanup
shutil.rmtree(test_base)
