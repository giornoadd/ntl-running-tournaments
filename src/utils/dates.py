
import re
from datetime import datetime

def adjust_year(dt):
    """
    Convert Buddhist Era year to AD if necessary.
    Assumes years > 2400 are BE.
    """
    if dt.year > 2400:
        return dt.replace(year=dt.year - 543)
    return dt

def parse_date_from_filename(filename):
    """
    Standard format: nickname-yyyy-mon-dd.ext
    e.g., oat-2026-jan-15.jpg
    Also handle _1, _2 suffixes
    """
    match = re.search(r'-(\d{4})-([a-z]{3})-(\d{2})', filename.lower())
    if match:
        y, m, d = match.groups()
        try:
            dt = datetime.strptime(f"{y}-{m}-{d}", "%Y-%b-%d")
            return dt
        except ValueError:
            pass

    # Support Runna filename format: "Runna ... on Feb 9, 2026 ..."
    match = re.search(r'on\s+([a-zA-Z]+)\s+(\d{1,2}),\s+(\d{4})', filename, re.IGNORECASE)
    if match:
        m, d, y = match.groups()
        try:
            valid_dt = datetime.strptime(f"{d} {m} {y}", "%d %b %Y")
            return valid_dt
        except ValueError:
            try: return datetime.strptime(f"{d} {m} {y}", "%d %B %Y")
            except ValueError: pass

    return None

def parse_date_generic(text):
    """
    Try to parse date from OCR text using various patterns.
    """
    text = text.strip()
    
    # 1. Standard Date/Time: 1/25/2026, 6:07 PM (Chan style)
    match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4}),\s*(\d{1,2}:\d{2}\s*(?:AM|PM))', text, re.IGNORECASE)
    if match:
        m, d, y, t_str = match.groups()
        try:
            dt_str = f"{m}/{d}/{y} {t_str}"
            dt = datetime.strptime(dt_str, "%m/%d/%Y %H:%M %p") # %I for 12-hour clock
            return adjust_year(dt)
        except ValueError: pass

    # 2. dd-Mon-yyyy (29 Jan 2026)
    match = re.search(r'(\d{1,2})[\s\/-]+([a-zA-Z]{3,9})[\s\/-]+(\d{4})', text, re.IGNORECASE)
    if match:
        d, m, y = match.groups()
        try:
            return adjust_year(datetime.strptime(f"{d} {m} {y}", "%d %b %Y"))
        except ValueError:
            try: return adjust_year(datetime.strptime(f"{d} {m} {y}", "%d %B %Y"))
            except ValueError: pass

    # 3. Month dd, yyyy (January 29, 2026)
    match = re.search(r'([a-zA-Z]{3,9})[\s]+(\d{1,2})[,\s]+(\d{4})', text, re.IGNORECASE)
    if match:
        m, d, y = match.groups()
        try:
            return adjust_year(datetime.strptime(f"{d} {m} {y}", "%d %b %Y"))
        except ValueError:
            try: return adjust_year(datetime.strptime(f"{d} {m} {y}", "%d %B %Y"))
            except ValueError: pass

    # 4. Numeric (d/m/y or y-m-d)
    match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', text)
    if match:
        v1, v2, v3 = map(int, match.groups())
        v1, v2, v3 = map(int, match.groups())
        
        dt_dmy = None
        dt_mdy = None
        
        # Try d/m/y
        try: dt_dmy = adjust_year(datetime(v3, v2, v1))
        except ValueError: pass
        
        # Try m/d/y
        try: dt_mdy = adjust_year(datetime(v3, v1, v2))
        except ValueError: pass
        
        if dt_dmy and dt_mdy:
             # Both valid. Check against today.
             now = datetime.now()
             if dt_dmy > now and dt_mdy <= now:
                 return dt_mdy
             return dt_dmy
        
        if dt_dmy: return dt_dmy
        if dt_mdy: return dt_mdy
        
    return None
