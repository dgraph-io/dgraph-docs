#!/usr/bin/env python3
"""
Fix tab formatting - ensure proper line breaks
"""

import re
from pathlib import Path

def fix_tabs_formatting(content):
    """Fix tab formatting"""
    # Fix <Tabs> <TabItem on same line -> separate lines
    content = re.sub(r'<Tabs> <TabItem', '<Tabs>\n<TabItem', content)
    
    # Fix </TabItem><TabItem on same line -> separate lines
    content = re.sub(r'</TabItem><TabItem', '</TabItem>\n<TabItem', content)
    
    # Fix </TabItem></Tabs> on same line -> separate lines
    content = re.sub(r'</TabItem></Tabs>', '</TabItem>\n</Tabs>', content)
    
    return content

def fix_file(filepath):
    """Fix a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        fixed = fix_tabs_formatting(content)
        
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
    
    print(f"\nFixed tab formatting in {fixed} files")

if __name__ == '__main__':
    main()

