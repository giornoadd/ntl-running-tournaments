import os
import re
import json
import shutil
from pathlib import Path

def sanitize_name(name):
    """
    Remove any Thai characters and special symbols, keeping only A-Z, a-z, 0-9, -, _, and .
    """
    sanitized = re.sub(r'[^A-Za-z0-9_\-\.]', '', name)
    if not sanitized:
        sanitized = "asset"
    return sanitized

def main():
    base_dir = Path(__file__).parent.parent.absolute()
    html_data_js = base_dir / 'docs' / 'html' / 'data.js'
    
    react_public = base_dir / 'webapp-react' / 'public'
    assets_out_dir = react_public / 'assets_data'
    rosters_out_dir = react_public / 'rosters'
    
    # 1. Clear out the old directories
    if assets_out_dir.exists(): shutil.rmtree(assets_out_dir)
    if rosters_out_dir.exists(): shutil.rmtree(rosters_out_dir)
    assets_out_dir.mkdir(parents=True, exist_ok=True)
    rosters_out_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. Read existing data.js and parse as JSON
    print("Reading docs/html/data.js...")
    with open(html_data_js, 'r', encoding='utf-8') as f:
        content = f.read()

    json_start = content.find('{')
    json_end = content.rfind('}')
    
    if json_start == -1 or json_end == -1:
        print("Error: Could not find valid JSON object in data.js")
        return
        
    json_str = content[json_start:json_end+1]
    
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from data.js: {e}")
        return

    def copy_file_to_assets(src_str):
        if not src_str: return ""
        src_path = (base_dir / 'html' / src_str).resolve()
        if not src_path.exists(): return src_str
        
        parts = src_path.parts[-4:]
        sanitized_parts = [sanitize_name(p) for p in parts]
        dest_rel = Path(*sanitized_parts)
        dest_full = assets_out_dir / dest_rel
        
        dest_full.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dest_full)
        return str(Path('assets_data') / dest_rel).replace('\\', '/')

    print("Sanitizing, separating JSON, and copying markdown assets...")

    for member in data.get('roster', []):
        nickname_safe = sanitize_name(member['nickname'].lower())
        
        # Update image paths
        member['recent_images'] = [copy_file_to_assets(img) for img in member.get('recent_images', [])]

        # Extract member_results directory by searching the base folder
        mem_dir = None
        for d in (base_dir / 'member_results').iterdir():
            if d.is_dir() and member['nickname'].lower() in d.name.lower():
                mem_dir = d
                break
                
        # Create a static markdown directory for this member
        member_assets_dir = assets_out_dir / 'members' / nickname_safe
        member_assets_dir.mkdir(parents=True, exist_ok=True)

        # Process markdown strings and rewrite static MD files
        def replace_md_links(match):
            original_path = "../" + match.group(1)
            new_path = copy_file_to_assets(original_path)
            return f"]({new_path})"

        md_dict = member.get('markdown', {})
        for key in md_dict:
            # The old regex [^)]+ fails when paths contain parentheses like (Boat).
            # Instead, match links ending with known file extensions (jpg, jpeg, png, gif, webp, md).
            # This handles nested parens in folder names.
            md_dict[key] = re.sub(
                r'\]\(\.\./(.+?\.(?:jpg|jpeg|png|gif|webp|JPEG|JPG|PNG|md))\)',
                replace_md_links,
                md_dict[key]
            )
            
            # Save the physical static markdown
            md_filename = 'README.md' if key == 'readme' else ('personal-statistics.md' if key == 'statistics' else 'running-plan.md')
            md_filepath = member_assets_dir / md_filename
            with open(md_filepath, 'w', encoding='utf-8') as mf:
                mf.write(md_dict[key])

        # Export this member to an independent roster JSON
        roster_json_path = rosters_out_dir / f"{nickname_safe}.json"
        with open(roster_json_path, 'w', encoding='utf-8') as rf:
            json.dump(member, rf, ensure_ascii=False, indent=2)
            
        # Shrink the main member object to optimize Dashboard payloads
        if 'markdown' in member:
            del member['markdown']

    # Handle global activities images
    for act in data.get('activities', []):
        for runner in act.get('runners_list', []):
            runner['images'] = [copy_file_to_assets(img) for img in runner.get('images', [])]

    # Save lightweight data.json
    out_json = react_public / 'data.json'
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Successfully wrote lightweight data.json to {out_json}")
    
    # Global README and results
    readme_src = base_dir / 'README.md'
    if readme_src.exists(): shutil.copy2(readme_src, assets_out_dir / 'README.md')
    results_dir_src = base_dir / 'results'
    if results_dir_src.exists():
        for f in results_dir_src.glob('*.md'):
            shutil.copy2(f, assets_out_dir / sanitize_name(f.name))
    
    print("Asset build complete.")

if __name__ == "__main__":
    main()
