import os
import argparse
import time
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import re

from utils.files import get_nickname

def analyze_image_with_gemini(image_path, model):
    try:
        img = Image.open(image_path)
        
        prompt = """
        Analyze this image and identify the DATE of the run or activity shown.
        Focus on text like "29 Jan 2026", "2026/01/29", "21 ม.ค. 69", etc.
        If you find a date, return it strictly in the format: DD-MM-YYYY.
        If you find multiple dates, prefer the one that looks like the activity date.
        If no date is clearly visible, return: NOT_FOUND.
        Do not explain or add extra text. Just the date or NOT_FOUND.
        """
        
        response = model.generate_content([prompt, img])
        text = response.text.strip()
        
        # specific cleanup for common hallucinations or formatting
        text = text.replace("Date: ", "").strip()
        
        if "NOT_FOUND" in text:
            return None
            
        # Try to parse the returned date to ensure validity
        try:
            # Expected DD-MM-YYYY
            return datetime.strptime(text, "%d-%m-%Y")
        except ValueError:
            print(f"  [Gemini] Returned invalid date format: {text}")
            return None

    except Exception as e:
        print(f"  [Error] Gemini analysis failed: {e}")
        return None

def process_files(base_dir, target_folder=None, dry_run=False, api_key=None):
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
        
    if not api_key:
        print("Error: GEMINI_API_KEY not found. Please provide it via --api-key or environment variable.")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    print(f"Scanning directory: {base_dir}")
    if dry_run:
        print(">> DRY RUN MODE: No files will be renamed. <<")

    for root, dirs, files in os.walk(base_dir):
        if root == base_dir:
            continue
            
        folder_name = os.path.basename(root)
        
        if target_folder and folder_name != target_folder:
            continue

        nickname = get_nickname(folder_name)
        if not nickname:
            continue
            
        nickname = nickname.lower().replace(" ", "")
        print(f"Processing folder: {folder_name} (Nickname: {nickname})")
        
        for filename in files:
            if filename.startswith('.'): continue
            _, ext = os.path.splitext(filename)
            if ext.lower() not in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
                continue
                
            filepath = os.path.join(root, filename)
            
            # Rate limiting or nice logging
            print(f"  Analyzing {filename}...")
            
            date_obj = analyze_image_with_gemini(filepath, model)
            
            if date_obj:
                print(f"    [Gemini] Found date: {date_obj.strftime('%d-%b-%Y')}")
                
                months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
                month_str = months[date_obj.month - 1]
                
                new_filename_base = f"{nickname}-{date_obj.year}-{month_str}-{date_obj.day:02d}"
                new_filename = f"{new_filename_base}{ext}"
                new_filepath = os.path.join(root, new_filename)
                
                if filename == new_filename:
                    print(f"    [Skip] Filename already correct.")
                    continue
                
                # Check if file exists, handle collision
                counter = 1
                while os.path.exists(new_filepath):
                    new_filename = f"{new_filename_base}_{counter}{ext}"
                    new_filepath = os.path.join(root, new_filename)
                    counter += 1
                
                if not dry_run:
                    os.rename(filepath, new_filepath)
                    print(f"    [Renamed] {filename} -> {new_filename}")
                else:
                    print(f"    [DryRun] Would rename: {filename} -> {new_filename}")
                
                # Sleep briefly to avoid aggressive rate limiting? 
                # Flash is fast but still check limits.
                time.sleep(1) 
            else:
                print(f"    [Gemini] No date found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze and rename files using Gemini Vision.")
    parser.add_argument("--dir", default="/Users/giornoadd/my-macos/running-comp/member_results", help="Base directory")
    parser.add_argument("--folder", default=None, help="Specific folder name")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes")
    parser.add_argument("--api-key", default=None, help="Gemini API Key")
    
    args = parser.parse_args()
    
    process_files(args.dir, args.folder, args.dry_run, args.api_key)
