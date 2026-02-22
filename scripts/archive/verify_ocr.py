import os
import shutil
import time
from datetime import datetime
from unittest.mock import MagicMock, patch
import sys

# Add script folder to sys.path to import rename_files
script_path = "/Users/giornoadd/my-macos/running-comp/script"
sys.path.append(script_path)

try:
    import rename_files
except ImportError:
    print(f"Error: Could not import 'rename_files' from {script_path}")
    sys.exit(1)

# Setup test environment
test_base = "/Users/giornoadd/my-macos/running-comp/test_ocr_results"
if os.path.exists(test_base):
    shutil.rmtree(test_base)
os.makedirs(test_base)

# Create a test folder
test_folder_name = "ITSystem-9_Ton (ต้น)"
folder_path = os.path.join(test_base, test_folder_name)
os.makedirs(folder_path)

# Create dummy file named as image for script to pick up
filepath = os.path.join(folder_path, "ocr_evidence.png")
with open(filepath, 'w') as f:
    f.write("dummy content")

# Set mtime to something irrelevant (e.g. 2025-01-01)
timestamp = datetime(2025, 1, 1, 12, 0, 0).timestamp()
os.utime(filepath, (timestamp, timestamp))

print(f"Created test file at: {filepath}")
print(f"File mtime is set to 2025-01-01, but OCR should extract 25 Dec 2025")

# Mock subprocess.run to return specific text
mock_result = MagicMock()
mock_result.stdout = "Evidence of running\nTotal time: 45:00\nDate: 25 Dec 2025\nDistance: 5km"
mock_result.returncode = 0

# Need to mock subprocess.run inside the rename_files module
with patch('subprocess.run', return_value=mock_result) as mock_subprocess:
    # Run the rename function directly
    print("Running rename_files with mocked OCR...")
    rename_files.rename_files(test_base)

# Verify
expected_name = "ton-25-dec-2025.png"
expected_path = os.path.join(folder_path, expected_name)

if os.path.exists(expected_path):
    print("SUCCESS: File renamed correctly using OCR date!")
else:
    print("FAILURE: File not renamed correctly.")
    print("Files in directory:")
    print(os.listdir(folder_path))

# Cleanup
shutil.rmtree(test_base)
