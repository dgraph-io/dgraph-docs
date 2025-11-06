#!/usr/bin/env python3
"""
Convert Hugo tabs to Docusaurus tabs
"""

import re
from pathlib import Path

def convert_tabs(content):
    """Convert Hugo tabs to Docusaurus tabs"""
    
    # Check if file needs tab imports
    needs_import = '{{% tabs %}}' in content or '{{< tab ' in content
    
    # Convert Hugo tabs to Docusaurus tabs
    # Pattern: {{% tabs %}} ... {{% /tabs %}}
    # Or: {{% tabs %}} {{< tab "Name" >}} ... {{< /tab >}} {{% /tabs %}}
    
    # Step 1: Replace {{% tabs %}} with <Tabs>
    content = re.sub(r'\{\{%\s*tabs\s*%\}\}', '<Tabs>', content)
    content = re.sub(r'\{\{%\s*/tabs\s*%\}\}', '</Tabs>', content)
    
    # Step 2: Replace {{< tab "Name" >}} with <TabItem value="name" label="Name">
    def replace_tab_open(match):
        tab_name = match.group(1)
        # Convert to lowercase for value, keep original for label
        value = tab_name.lower().replace(' ', '-')
        return f'<TabItem value="{value}" label="{tab_name}">'
    
    content = re.sub(r'\{\{<\s*tab\s+"([^"]+)"\s*>\}\}', replace_tab_open, content)
    content = re.sub(r'\{\{%\s*tab\s+"([^"]+)"\s*%\}\}', replace_tab_open, content)
    
    # Step 3: Replace {{< /tab >}} or {{% /tab %}} with </TabItem>
    content = re.sub(r'\{\{<\s*/tab\s*>\}\}', '</TabItem>', content)
    content = re.sub(r'\{\{%\s*/tab\s*%\}\}', '</TabItem>', content)
    
    # Step 4: Fix escaped angle brackets
    content = re.sub(r'&lt;', '<', content)
    content = re.sub(r'&gt;', '>', content)
    
    # Step 5: Add imports at the top if needed
    if needs_import and 'import Tabs' not in content:
        # Check if file has frontmatter
        if content.startswith('---'):
            # Find end of frontmatter
            frontmatter_end = content.find('---', 3)
            if frontmatter_end != -1:
                # Insert imports after frontmatter
                imports = '\nimport Tabs from \'@theme/Tabs\';\nimport TabItem from \'@theme/TabItem\';\n\n'
                content = content[:frontmatter_end + 3] + imports + content[frontmatter_end + 3:]
        else:
            # No frontmatter, add imports at the beginning
            imports = 'import Tabs from \'@theme/Tabs\';\nimport TabItem from \'@theme/TabItem\';\n\n'
            content = imports + content
    
    return content

def fix_file(filepath):
    """Fix a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        fixed = convert_tabs(content)
        
        if fixed != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed)
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
    
    print(f"\nFixed tabs in {fixed} files")

if __name__ == '__main__':
    main()

