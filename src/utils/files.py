
import os
import re

def get_nickname(folder_name):
    """
    Extract nickname from folder name.
    e.g. "Manda-1_โจ (GIO)" -> "gio"
    e.g. "ITSystem-1_Oat (โอ๊ต)" -> "oat"
    """
    try:
        parts = folder_name.split('_')
        if len(parts) >= 2:
            # part[1] is "โจ (GIO)" or "Oat (โอ๊ต)"
            name_part = "_".join(parts[1:])
            
            # Logic: Look for English text inside or outside parens
            
            # Check inside parens first: (GIO), (Oat), (Chan)
            paren_match = re.search(r'\((.*?)\)', name_part)
            if paren_match:
                content = paren_match.group(1)
                if re.search(r'[a-zA-Z]', content):
                    return content.strip().lower() # "gio", "oat"
            
            # Check outside parens: Oat (โอ๊ต) -> Oat
            pre_paren = name_part.split('(')[0].strip()
            if re.search(r'[a-zA-Z]', pre_paren):
                 return pre_paren.lower()

    except Exception as e:
        print(f"Error parsing nickname for {folder_name}: {e}")
        pass
    
    return None

def list_image_files(base_dir):
    """Recursively list all image files."""
    image_files = []
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_files.append(os.path.join(root, f))
    return image_files
