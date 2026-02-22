import os
from PIL import Image, ImageDraw, ImageFont

def get_best_font(font_size):
    """Attempt to find a robust font on macOS/Linux. Fallback to default."""
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSText.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, font_size)
            except Exception:
                continue
    return ImageFont.load_default()

def add_text_watermark(image_path, text, position="bottom-right", dry_run=False):
    """
    Core function for applying a semi-transparent text watermark.
    
    Args:
        image_path: Path to the image.
        text: String of text to render on the image.
        position: 'bottom-right' (default) or 'bottom-center'
        dry_run: bool indicating whether to bypass writing
    """
    if dry_run:
        print(f"  [DRY-RUN] Would add watermark '{text}' to {os.path.basename(image_path)}")
        return True
    
    try:
        img = Image.open(image_path)
        width, height = img.size
        
        # Convert to RGBA for transparency compositing
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create blank transparency overlay
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Scale Font based on role
        if position == 'bottom-center':
            font_size = max(int(width * 0.04), 24)
        else:
            font_size = max(int(width * 0.035), 20)
            
        font = get_best_font(font_size)
        
        # Determine bounding box
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        padding = int(width * 0.02)
        bg_padding = int(font_size * 0.3)
        
        # Calculate X/Y Positioning Coordinates
        if position == 'bottom-center':
            x = (width - text_width) // 2
        else: # bottom-right
            x = width - text_width - padding - bg_padding
            
        y = height - text_height - padding - bg_padding
        
        # Render a readable dark shadow behind the white text
        bg_rect = [
            x - bg_padding,
            y - bg_padding,
            x + text_width + bg_padding,
            y + text_height + bg_padding
        ]
        draw.rounded_rectangle(bg_rect, radius=8, fill=(0, 0, 0, 160))
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 240))
        
        # Composite and Flatten
        result = Image.alpha_composite(img, overlay)
        
        ext = os.path.splitext(image_path)[1].lower()
        if ext in ('.jpg', '.jpeg'):
            result = result.convert('RGB')
            result.save(image_path, 'JPEG', quality=95)
        else:
            result.save(image_path)
        
        print(f"  ✅ Added {position} watermark '{text}' to {os.path.basename(image_path)}")
        return True
    except Exception as e:
        print(f"  ❌ Error adding watermark to {os.path.basename(image_path)}: {e}")
        return False
