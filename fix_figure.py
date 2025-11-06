#!/usr/bin/env python3
"""
Replace Hugo {{< figure >}} shortcodes with Docusaurus image syntax
"""

import re
from pathlib import Path

def convert_figure(content):
    """Convert Hugo figure shortcodes to Docusaurus images"""
    
    # Pattern: {{< figure src="/path/to/image.png" alt="Alt text" >}}
    # Convert to: ![Alt text](/path/to/image.png)
    
    def replace_figure(match):
        src = match.group(1)
        alt = match.group(2) if match.group(2) else ''
        
        # Ensure path starts with / for absolute paths
        if not src.startswith('/'):
            src = '/' + src
        
        return f'![{alt}]({src})'
    
    # Match {{< figure src="..." alt="..." >}} with various spacing
    # Handle both {{<figure and {{< figure
    content = re.sub(
        r'\{\{<\s*figure\s+src\s*=\s*"([^"]+)"\s+alt\s*=\s*"([^"]*)"\s*>\}\}',
        replace_figure,
        content,
        flags=re.IGNORECASE
    )
    
    # Also handle case where alt might come first
    content = re.sub(
        r'\{\{<\s*figure\s+alt\s*=\s*"([^"]*)"\s+src\s*=\s*"([^"]+)"\s*>\}\}',
        lambda m: f'![{m.group(1)}]({m.group(2) if m.group(2).startswith("/") else "/" + m.group(2)})',
        content,
        flags=re.IGNORECASE
    )
    
    return content

def fix_file(filepath):
    """Fix a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Match {{< figure src="..." alt="..." >}} with various spacing
        def replace_figure(match):
            src = match.group(1)
            alt = match.group(2) if match.group(2) else ''
            
            # Ensure path starts with / for absolute paths
            if not src.startswith('/'):
                src = '/' + src
            
            return f'![{alt}]({src})'
        
        # Handle both {{<figure and {{< figure (case insensitive)
        content = re.sub(
            r'\{\{<\s*figure\s+src\s*=\s*"([^"]+)"\s+alt\s*=\s*"([^"]*)"\s*>\}\}',
            replace_figure,
            content,
            flags=re.IGNORECASE
        )
        
        # Also handle case where alt might come first
        content = re.sub(
            r'\{\{<\s*figure\s+alt\s*=\s*"([^"]*)"\s+src\s*=\s*"([^"]+)"\s*>\}\}',
            lambda m: f'![{m.group(1)}]({m.group(2) if m.group(2).startswith("/") else "/" + m.group(2)})',
            content,
            flags=re.IGNORECASE
        )
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    docs_dir = Path('docusaurus-docs/docs')
    
    fixed = 0
    for md_file in docs_dir.rglob('*.md'):
        if fix_file(md_file):
            fixed += 1
            print(f"Fixed: {md_file}")
    
    print(f"\nFixed figure shortcodes in {fixed} files")

if __name__ == '__main__':
    main()

