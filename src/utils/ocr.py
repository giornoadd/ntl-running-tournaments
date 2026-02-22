
import os
import subprocess
import re
import time
from PIL import Image, ImageEnhance

def preprocess_image(image_path, debug=False):
    try:
        img = Image.open(image_path)
        img = img.convert('L') # Grayscale
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        
        temp_path = f"temp_ocr_{os.getpid()}_{int(time.time()*1000)}.png"
        dir_path = os.path.dirname(image_path)
        full_temp_path = os.path.join(dir_path, temp_path)
        
        img.save(full_temp_path)
        return full_temp_path
    except Exception as e:
        if debug: print(f"Preprocessing error: {e}")
        return None

def extract_text(image_path, psm='3', debug=False):
    temp_path = preprocess_image(image_path, debug)
    target_path = temp_path if temp_path else image_path
    
    text = ""
    try:
        # psm 11 (Sparse) is often better for screenshots
        cmd = ['tesseract', target_path, 'stdout']
        if psm:
            cmd.extend(['--psm', psm])
            
        result = subprocess.run(cmd, capture_output=True, text=True)
        text = result.stdout
    except Exception as e:
        if debug: print(f"OCR Error: {e}")
    finally:
        if temp_path and os.path.exists(temp_path) and not debug:
            os.remove(temp_path)
    return text

def extract_distance_duration(text):
    distance = 0.0
    duration_str = ""
    
    # Distance
    dist_match = re.search(r'(\d+\.\d+)\s*(?:km|mi|KM)', text)
    if dist_match:
        distance = float(dist_match.group(1))
    
    # Duration: HH:MM:SS or MM:SS
    dur_match = re.search(r'(\d{1,2}:\d{2}(?::\d{2})?)', text)
    if dur_match:
        duration_str = dur_match.group(1)
    else:
        # 30m 10s
        dur_match_2 = re.search(r'(\d{1,2})m\s*(\d{1,2})s', text)
        if dur_match_2:
            duration_str = f"00:{dur_match_2.group(1)}:{dur_match_2.group(2)}"

    return distance, duration_str
