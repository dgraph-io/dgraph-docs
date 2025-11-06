#!/usr/bin/env python3
"""
Fix frontmatter in migrated Docusaurus files
"""

import os
import re
from pathlib import Path

def fix_frontmatter(content):
    """Fix frontmatter format"""
    # Fix title = "..." to title: ...
    content = re.sub(r'title\s*=\s*"([^"]+)"', r'title: \1', content)
    content = re.sub(r"title\s*=\s*'([^']+)'", r"title: \1", content)
    
    # Fix description = "..." to description: ...
    content = re.sub(r'description\s*=\s*"([^"]+)"', r'description: \1', content)
    content = re.sub(r"description\s*=\s*'([^']+)'", r"description: \1", content)
    
    # Remove any remaining menu entries
    content = re.sub(r'^\s*\[menu\.\w+\].*?$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*name\s*=.*?$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*identifier\s*=.*?$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*parent\s*=.*?$', '', content, flags=re.MULTILINE)
    
    # Clean up extra blank lines in frontmatter
    lines = content.split('\n')
    fixed_lines = []
    in_frontmatter = False
    frontmatter_started = False
    
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
                frontmatter_started = True
                fixed_lines.append(line)
            else:
                # End of frontmatter
                fixed_lines.append(line)
                in_frontmatter = False
            continue
        
        if in_frontmatter:
            # Skip empty lines at start of frontmatter
            if not frontmatter_started and not line.strip():
                continue
            frontmatter_started = True
            # Skip empty lines and orphaned menu entries
            if line.strip() and not re.match(r'^\s*\[menu\.', line):
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_file(filepath):
    """Fix a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed = fix_frontmatter(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed)
        
        return True
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    docs_dir = Path('docusaurus-docs/docs')
    
    fixed = 0
    for md_file in docs_dir.rglob('*.md'):
        if fix_file(md_file):
            fixed += 1
    
    print(f"Fixed frontmatter in {fixed} files")

if __name__ == '__main__':
    main()

