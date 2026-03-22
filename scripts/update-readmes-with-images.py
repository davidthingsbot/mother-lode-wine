#!/usr/bin/env python3
"""
Update all winery README.md files to include inline images for photo.jpg and map.png.
Adds image links after the H1 title and tagline.
"""

import os
import re
from pathlib import Path

def update_readme(readme_path):
    """Update a README.md to include image references."""
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Check if images already added
    if '![Photo]' in content or '![Map]' in content:
        return False, "already has images"
    
    # Check if photo.jpg and map.png exist
    readme_dir = readme_path.parent
    has_photo = (readme_dir / 'photo.jpg').exists()
    has_map = (readme_dir / 'map.png').exists()
    
    if not has_photo and not has_map:
        return False, "no images found"
    
    # Find the insertion point - after H1 and tagline (if present)
    # Pattern: # Title\n\n> *tagline*\n\n (or just # Title\n\n)
    
    lines = content.split('\n')
    insert_line = 0
    
    # Find end of H1 + tagline block
    for i, line in enumerate(lines):
        if line.startswith('# '):
            insert_line = i + 1
            # Skip blank lines
            while insert_line < len(lines) and lines[insert_line].strip() == '':
                insert_line += 1
            # Check for tagline (> *)
            if insert_line < len(lines) and lines[insert_line].startswith('> *'):
                insert_line += 1
                # Skip blank lines after tagline
                while insert_line < len(lines) and lines[insert_line].strip() == '':
                    insert_line += 1
            break
    
    # Build image block
    image_block = []
    if has_photo:
        image_block.append('![Photo](photo.jpg)')
        image_block.append('')
    
    if has_map:
        image_block.append('## Location')
        image_block.append('')
        image_block.append('![Map](map.png)')
        image_block.append('')
    
    # Insert the image block
    new_lines = lines[:insert_line] + image_block + lines[insert_line:]
    new_content = '\n'.join(new_lines)
    
    with open(readme_path, 'w') as f:
        f.write(new_content)
    
    return True, "updated"

def main():
    script_dir = Path(__file__).parent
    repo_dir = script_dir.parent
    regions_dir = repo_dir / 'regions'
    
    print("Updating winery READMEs with image links...")
    print("=" * 60)
    
    updated = 0
    skipped = 0
    
    for county_dir in sorted(regions_dir.iterdir()):
        if not county_dir.is_dir():
            continue
        
        county = county_dir.name
        print(f"\n{county.upper()}")
        print("-" * 40)
        
        for winery_dir in sorted(county_dir.iterdir()):
            if not winery_dir.is_dir():
                continue
            
            readme_path = winery_dir / 'README.md'
            if not readme_path.exists():
                continue
            
            winery_slug = winery_dir.name
            success, msg = update_readme(readme_path)
            
            if success:
                print(f"  ✓ {winery_slug}")
                updated += 1
            else:
                print(f"  - {winery_slug} ({msg})")
                skipped += 1
    
    print("\n" + "=" * 60)
    print(f"COMPLETE: {updated} READMEs updated, {skipped} skipped")

if __name__ == '__main__':
    main()
