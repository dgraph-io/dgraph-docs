#!/usr/bin/env python3
"""
Fix YAML frontmatter - quote values that contain colons or special characters
"""

import re
from pathlib import Path

def fix_frontmatter(content):
    """Fix frontmatter - quote values with colons"""
    lines = content.split('\n')
    fixed_lines = []
    in_frontmatter = False
    
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
                fixed_lines.append(line)
                continue
            else:
                in_frontmatter = False
                fixed_lines.append(line)
                continue
        
        if in_frontmatter:
            # Match title: value or description: value
            match = re.match(r'^(\s*)(title|description):\s*(.+)$', line)
            if match:
                indent, key, value = match.groups()
                value = value.strip()
                # If value contains colon and isn't already quoted, quote it
                if ':' in value and not (value.startswith('"') or value.startswith("'")):
                    value = f'"{value}"'
                fixed_lines.append(f"{indent}{key}: {value}")
            else:
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
        
        if fixed != content:
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
    
    print(f"\nFixed YAML quotes in {fixed} files")

if __name__ == '__main__':
    main()

