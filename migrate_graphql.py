#!/usr/bin/env python3
"""
Script to migrate Hugo GraphQL pages to Docusaurus format.
Converts frontmatter and shortcodes.
"""

import os
import re
import sys
from pathlib import Path

def convert_frontmatter(content):
    """Convert Hugo frontmatter (+++) to Docusaurus frontmatter (---)"""
    # Replace +++ with ---
    content = re.sub(r'^\+\+\+', '---', content, flags=re.MULTILINE)
    content = re.sub(r'^\+\+\+', '---', content, flags=re.MULTILINE)
    
    # Remove Hugo-specific menu entries
    content = re.sub(r'\[menu\.\w+\].*?\n', '', content, flags=re.DOTALL)
    
    # Remove weight and type fields (not needed in Docusaurus)
    content = re.sub(r'^\s*type\s*=\s*"[^"]*"\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*weight\s*=\s*\d+\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*date\s*=\s*"[^"]*"\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*aliases\s*=\s*\[[^\]]*\]\s*$', '', content, flags=re.MULTILINE)
    
    # Clean up extra blank lines in frontmatter
    content = re.sub(r'---\n\n+---', '---\n---', content)
    
    return content

def convert_shortcodes(content):
    """Convert Hugo shortcodes to Docusaurus equivalents"""
    # Convert {{% notice "note" %}} to :::note
    content = re.sub(r'\{\{%\s*notice\s+"note"\s*%\}\}', ':::note', content)
    content = re.sub(r'\{\{%\s*/\s*notice\s*%\}\}', ':::', content)
    
    # Convert {{% notice "tip" %}} to :::tip
    content = re.sub(r'\{\{%\s*notice\s+"tip"\s*%\}\}', ':::tip', content)
    
    # Convert {{% notice "warning" %}} to :::warning
    content = re.sub(r'\{\{%\s*notice\s+"warning"\s*%\}\}', ':::warning', content)
    
    # Convert {{% notice "danger" %}} to :::danger
    content = re.sub(r'\{\{%\s*notice\s+"danger"\s*%\}\}', ':::danger', content)
    
    # Convert {{< relref >}} to relative links (simplified - will need manual review)
    def replace_relref(match):
        path = match.group(1).strip('"\'')
        # Remove .md extension if present
        path = path.replace('.md', '')
        # Convert to relative path
        return f'[{path}]({path})'
    
    content = re.sub(r'\{\{<\s*relref\s+"([^"]+)"\s*>\}\}', replace_relref, content)
    
    return content

def migrate_file(hugo_path, docusaurus_dir):
    """Migrate a single file from Hugo to Docusaurus format"""
    try:
        with open(hugo_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {hugo_path}: {e}")
        return False
    
    # Convert content
    content = convert_frontmatter(content)
    content = convert_shortcodes(content)
    
    # Determine output path
    rel_path = hugo_path.relative_to(Path('content'))
    if rel_path.name == '_index.md':
        output_path = docusaurus_dir / rel_path.parent / 'index.md'
    else:
        output_path = docusaurus_dir / rel_path
    
    # Create directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Migrated: {rel_path}")
        return True
    except Exception as e:
        print(f"Error writing {output_path}: {e}")
        return False

def main():
    # Migrate GraphQL pages
    content_dir = Path('content/graphql')
    docusaurus_dir = Path('docusaurus-docs/docs-graphql')
    
    migrated = 0
    skipped = 0
    
    if content_dir.exists():
        for hugo_file in content_dir.rglob('*.md'):
            if migrate_file(hugo_file, docusaurus_dir):
                migrated += 1
            else:
                skipped += 1
    
    # Migrate GraphQL-DQL pages
    content_dql_dir = Path('content/graphql-dql')
    docusaurus_dql_dir = Path('docusaurus-docs/docs-graphql-dql')
    
    if content_dql_dir.exists():
        for hugo_file in content_dql_dir.rglob('*.md'):
            if migrate_file(hugo_file, docusaurus_dql_dir):
                migrated += 1
            else:
                skipped += 1
    
    print(f"\nMigration complete!")
    print(f"Migrated: {migrated} files")
    print(f"Skipped: {skipped} files")

if __name__ == '__main__':
    main()

