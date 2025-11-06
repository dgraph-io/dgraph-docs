#!/usr/bin/env python3
"""
Script to fix GraphQL pages for Docusaurus:
- Fix frontmatter syntax
- Convert relref to proper links
- Convert tabs to Docusaurus tabs
- Convert load-img to images
- Convert figure to images
- Fix broken links
"""

import os
import re
from pathlib import Path

def fix_frontmatter(content):
    """Fix Hugo frontmatter syntax to YAML"""
    # Fix title = "..." to title: "..."
    content = re.sub(r'^title\s*=\s*"([^"]+)"', r'title: "\1"', content, flags=re.MULTILINE)
    content = re.sub(r'^description\s*=\s*"([^"]+)"', r'description: "\1"', content, flags=re.MULTILINE)
    content = re.sub(r'^identifier\s*=\s*"([^"]+)"', r'id: "\1"', content, flags=re.MULTILINE)
    
    # Remove parent and other Hugo-specific fields
    content = re.sub(r'^\s*parent\s*=\s*"[^"]*"\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*identifier\s*=\s*"[^"]*"\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*name\s*=\s*"[^"]*"\s*$', '', content, flags=re.MULTILINE)
    
    # Clean up extra blank lines in frontmatter
    content = re.sub(r'---\n\n+---', '---\n---', content)
    
    return content

def fix_relref(content, file_path):
    """Convert Hugo relref to Docusaurus links"""
    def replace_relref(match):
        identifier = match.group(1).strip('"\'')
        # Convert identifier to proper path
        # For now, just convert to a relative link
        if identifier == "gqlschema":
            return "[GraphQL schema](/graphql/schema/dgraph-schema)"
        # Default: try to create a link
        return f"[{identifier}](/graphql/{identifier})"
    
    content = re.sub(r'\{\{<\s*relref\s+identifier\s*=\s*"([^"]+)"\s*>\}\}', replace_relref, content)
    content = re.sub(r'\{\{<\s*relref\s+"([^"]+)"\s*>\}\}', replace_relref, content)
    
    return content

def fix_tabs(content):
    """Convert Hugo tabs to Docusaurus tabs"""
    # Add imports at the top if tabs are found
    if '{{% tabs %}}' in content or '{{< tab' in content or '{{% /tab %}}' in content:
        if 'import Tabs' not in content:
            # Find the first --- after frontmatter
            frontmatter_end = content.find('---', content.find('---') + 3)
            if frontmatter_end != -1:
                insert_pos = frontmatter_end + 3
                imports = '\nimport Tabs from \'@theme/Tabs\';\nimport TabItem from \'@theme/TabItem\';\n\n'
                content = content[:insert_pos] + imports + content[insert_pos:]
    
    # Convert tabs
    content = re.sub(r'\{\{%\s*tabs\s*%\}\}', '<Tabs>', content)
    content = re.sub(r'\{\{%\s*/tabs\s*%\}\}', '</Tabs>', content)
    
    # Convert tab items
    def replace_tab(match):
        label = match.group(1).strip('"\'')
        value = label.lower().replace(' ', '-')
        return f'<TabItem value="{value}" label="{label}">'
    
    content = re.sub(r'\{\{<\s*tab\s+"([^"]+)"\s*>\}\}', replace_tab, content)
    content = re.sub(r'\{\{<\s*/tab\s*>\}\}', '</TabItem>', content)
    # Fix leftover Hugo closing tags
    content = re.sub(r'\{\{%\s*/tab\s*%\}\}', '</TabItem>', content)
    
    return content

def fix_load_img(content):
    """Convert load-img to markdown images"""
    def replace_load_img(match):
        img_path = match.group(1).strip('"\'')
        alt_text = match.group(2).strip('"\'') if match.group(2) else ""
        # Ensure path starts with /
        if not img_path.startswith('/'):
            img_path = '/' + img_path
        return f'![{alt_text}]({img_path})'
    
    content = re.sub(r'\{\{%\s*load-img\s+"([^"]+)"\s+"([^"]+)"\s*%\}\}', replace_load_img, content)
    
    return content

def fix_figure(content):
    """Convert figure to markdown images"""
    def replace_figure_with_title(match):
        src = match.group(1).strip('"\'')
        alt = match.group(2).strip('"\'') if len(match.groups()) > 1 and match.group(2) else ""
        title = match.group(3).strip('"\'') if len(match.groups()) > 2 and match.group(3) else ""
        # Ensure path starts with /
        if not src.startswith('/'):
            src = '/' + src
        if title:
            return f'![{alt}]({src} "{title}")'
        return f'![{alt}]({src})'
    
    def replace_figure_simple(match):
        src = match.group(1).strip('"\'')
        alt = match.group(2).strip('"\'') if len(match.groups()) > 1 and match.group(2) else ""
        # Ensure path starts with /
        if not src.startswith('/'):
            src = '/' + src
        return f'![{alt}]({src})'
    
    # Pattern: {{<figure ... src="..." alt="..." title="...">}}
    content = re.sub(r'\{\{<figure[^>]*src\s*=\s*"([^"]+)"[^>]*alt\s*=\s*"([^"]+)"[^>]*title\s*=\s*"([^"]+)"[^>]*>\}\}', replace_figure_with_title, content)
    # Pattern: {{<figure ... src="..." alt="...">}}
    content = re.sub(r'\{\{<figure[^>]*src\s*=\s*"([^"]+)"[^>]*alt\s*=\s*"([^"]+)"[^>]*>\}\}', replace_figure_simple, content)
    # Pattern: {{<figure ... src="...">}}
    content = re.sub(r'\{\{<figure[^>]*src\s*=\s*"([^"]+)"[^>]*>\}\}', replace_figure_simple, content)
    
    return content

def fix_broken_links(content):
    """Fix broken markdown links"""
    # Fix nested links like [/graphql/[text](url)] to just /graphql/url
    content = re.sub(r'\[/graphql/\[([^\]]+)\]\(([^)]+)\)\]', r'[/graphql/\2]', content)
    
    def replace_link(match):
        text = match.group(1)
        url = match.group(2)
        if url.startswith(('http', '/', '#')):
            return f'[{text}]({url})'
        # Fix patterns like [lambda-overview](lambda-overview)
        if url == text and not url.startswith('/'):
            return f'[{text}](/graphql/{url})'
        return f'[{text}](/graphql/{url})'
    
    # Fix [text](text) patterns that don't start with http, /, or #
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, content)
    
    return content

def fix_file(file_path):
    """Fix a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False
    
    original_content = content
    
    # Apply all fixes
    content = fix_frontmatter(content)
    content = fix_relref(content, file_path)
    content = fix_tabs(content)
    content = fix_load_img(content)
    content = fix_figure(content)
    content = fix_broken_links(content)
    
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {file_path}")
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return False
    
    return False

def main():
    graphql_dir = Path('docusaurus-docs/docs-graphql')
    
    fixed = 0
    total = 0
    
    for md_file in graphql_dir.rglob('*.md'):
        total += 1
        if fix_file(md_file):
            fixed += 1
    
    print(f"\nFixed {fixed} out of {total} files")

if __name__ == '__main__':
    main()

