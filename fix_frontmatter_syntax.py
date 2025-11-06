#!/usr/bin/env python3
"""
Fix frontmatter syntax errors - convert = to : in frontmatter
"""

import re
from pathlib import Path

def fix_frontmatter(content):
    """Fix frontmatter syntax - convert = to : and remove invalid fields"""
    lines = content.split('\n')
    fixed_lines = []
    in_frontmatter = False
    frontmatter_end = False
    
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
                fixed_lines.append(line)
                continue
            else:
                # End of frontmatter
                in_frontmatter = False
                frontmatter_end = True
                fixed_lines.append(line)
                continue
        
        if in_frontmatter:
            # Convert keywords = "value" to keywords: value (or remove if not standard)
            if re.match(r'^\s*keywords\s*=', line):
                # Remove keywords field (not standard Docusaurus frontmatter)
                continue
            # Convert any remaining = to :
            if '=' in line and not line.strip().startswith('#'):
                # Check if it's a key = value pattern
                match = re.match(r'^(\s*)(\w+)\s*=\s*(.+)$', line)
                if match:
                    indent, key, value = match.groups()
                    # Remove quotes if present
                    value = value.strip().strip('"').strip("'")
                    fixed_lines.append(f"{indent}{key}: {value}")
                else:
                    fixed_lines.append(line)
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
    
    print(f"Fixed frontmatter syntax in {fixed} files")

if __name__ == '__main__':
    main()

