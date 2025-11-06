#!/usr/bin/env python3
"""
Fix MDX compilation issues - escape angle brackets and fix HTML tags
"""

import re
from pathlib import Path

def fix_mdx(content):
    """Fix MDX issues"""
    # Fix unclosed or malformed HTML tags - remove standalone opening tags without closing
    # Remove <object> tags (common issue)
    content = re.sub(r'<object[^>]*>.*?</object>', '', content, flags=re.DOTALL)
    
    # Escape angle brackets in code context but not in HTML tags
    # This is a simplified approach - escape < > that are not part of HTML tags
    # Pattern: <word> should be escaped if not part of HTML tag
    def escape_angles(match):
        text = match.group(0)
        # Don't escape if it looks like an HTML tag
        if re.match(r'</?[a-zA-Z][^>]*>', text):
            return text
        # Escape angle brackets
        return text.replace('<', '&lt;').replace('>', '&gt;')
    
    # Find and escape angle brackets in text (not in code blocks)
    lines = content.split('\n')
    fixed_lines = []
    in_code_block = False
    
    for line in lines:
        # Check if we're entering/leaving a code block
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            fixed_lines.append(line)
            continue
        
        if not in_code_block:
            # Escape angle brackets that aren't part of HTML tags
            # Simple approach: if line contains <something> and doesn't start with <, escape it
            if '<' in line and '>' in line:
                # Check if it's an HTML tag
                if not re.match(r'^\s*<[a-zA-Z]', line):
                    # Escape angle brackets in angle-bracket pairs
                    line = re.sub(r'<([^<>]+)>', r'&lt;\1&gt;', line)
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_file(filepath):
    """Fix a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed = fix_mdx(content)
        
        if fixed != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed)
            return True
        return False
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    # Fix specific files mentioned in errors
    files_to_fix = [
        'docusaurus-docs/docs/admin/enterprise-features/binary-backups.md',
        'docusaurus-docs/docs/admin/enterprise-features/multitenancy.md',
        'docusaurus-docs/docs/admin/observability/tracing.md',
        'docusaurus-docs/docs/design-concepts/badger-concept.md',
        'docusaurus-docs/docs/design-concepts/minimizing-network-calls.md',
        'docusaurus-docs/docs/design-concepts/relationships-concept.md',
        'docusaurus-docs/docs/dql/dql-mutation.md',
        'docusaurus-docs/docs/dql/dql-schema.md',
    ]
    
    fixed = 0
    for filepath_str in files_to_fix:
        filepath = Path(filepath_str)
        if filepath.exists():
            if fix_file(filepath):
                fixed += 1
                print(f"Fixed: {filepath}")
    
    print(f"\nFixed {fixed} files")

if __name__ == '__main__':
    main()

