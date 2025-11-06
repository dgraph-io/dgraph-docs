#!/usr/bin/env python3
"""
Convert Hugo {{% load-img "path" "alt" %}} to Docusaurus image syntax
"""

import re
from pathlib import Path

def convert_load_img(content):
    """Convert Hugo load-img shortcodes to Docusaurus images"""
    
    # Pattern: {{% load-img "path/to/image.png" "alt text" %}}
    # Convert to: ![alt text](/path/to/image.png)
    
    def replace_load_img(match):
        image_path = match.group(1)
        alt_text = match.group(2)
        
        # Ensure path starts with / for absolute paths in Docusaurus
        if not image_path.startswith('/'):
            image_path = '/' + image_path
        
        return f'![{alt_text}]({image_path})'
    
    # Match {{% load-img "path" "alt" %}}
    content = re.sub(
        r'\{\{%\s*load-img\s+"([^"]+)"\s+"([^"]+)"\s*%\}\}',
        replace_load_img,
        content
    )
    
    return content

def fix_file(filepath):
    """Fix a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        fixed = convert_load_img(content)
        
        if fixed != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed)
            return True
        return False
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    docs_dir = Path('docusaurus-docs/docs')
    
    fixed = 0
    for md_file in docs_dir.rglob('*.md'):
        if fix_file(md_file):
            fixed += 1
            print(f"Fixed: {md_file}")
    
    print(f"\nFixed load-img in {fixed} files")

if __name__ == '__main__':
    main()

