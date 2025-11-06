#!/usr/bin/env python3
"""
Replace Hugo {{< relref identifier="something">}} with Docusaurus document references
Also fix double-nested links from previous conversion
"""

import re
from pathlib import Path

def find_document_id(identifier, current_file):
    """Find the document ID for a given identifier"""
    docs_dir = Path('docusaurus-docs/docs')
    current_path = Path(current_file)
    
    # Common identifier mappings - map to full paths
    identifier_map = {
        'learning-environment': '/learn/',
        'security': '/dgraph-overview/admin/security/',
        'admin': '/dgraph-overview/admin/',
        'monitoring': '/dgraph-overview/admin/observability/monitoring',
        'production-checklist': '/dgraph-overview/installation/production-checklist',
        'dgraph-architecture': '/dgraph-overview/installation/dgraph-architecture',
        'dql': '/dgraph-overview/dql/',
        'graphql': '/graphql/',
        'ratel': '/ratel/',
        'ports-usage': '/dgraph-overview/admin/security/ports-usage',
        'dgraph-zero': '/dgraph-overview/admin/dgraph-zero',
        'binary-backups': '/dgraph-overview/admin/enterprise-features/binary-backups',
        'dgraph-administration': '/dgraph-overview/admin/dgraph-administration',
        'single-host-setup': '/dgraph-overview/installation/single-host-setup',
        'encryption-at-rest': '/dgraph-overview/admin/enterprise-features/encryption-at-rest',
        'multitenancy': '/dgraph-overview/admin/enterprise-features/multitenancy',
        'data-compression': '/dgraph-overview/admin/data-compression',
        'download': '/dgraph-overview/installation/download',
        'cli/config': '/dgraph-overview/cli/config',
        'cli/superflags': '/dgraph-overview/cli/superflags',
        'cli/live': '/dgraph-overview/cli/live',
        'dql-rdf': '/dgraph-overview/dql/dql-rdf',
        'graphql-dql': '/graphql-dql/',
        'dgraph-architecture': '/dgraph-overview/installation/dgraph-architecture',
    }
    
    # Check mappings first
    if identifier in identifier_map:
        return identifier_map[identifier]
    
    # Try to find the file and return relative path
    possible_paths = [
        docs_dir / identifier / 'index.md',
        docs_dir / f'{identifier}.md',
        current_path.parent / f'{identifier}.md',
    ]
    
    # Search in subdirectories
    for subdir in docs_dir.rglob('*'):
        if subdir.is_dir():
            possible_paths.extend([
                subdir / f'{identifier}.md',
                subdir / identifier / 'index.md',
            ])
    
    # Check if file exists and calculate relative path
    for path in possible_paths:
        if path.exists() and path.is_file():
            try:
                rel_path = path.relative_to(docs_dir)
                # Convert to document ID (remove .md, convert index to parent)
                doc_id = str(rel_path).replace('.md', '')
                if doc_id.endswith('/index'):
                    doc_id = doc_id[:-6]  # Remove /index
                if not doc_id:
                    doc_id = identifier
                # Return as full path with /dgraph-overview/ prefix
                return f'/dgraph-overview/{doc_id}'
            except:
                pass
    
    # Fallback: use identifier as-is (might be a relative path)
    return f'/dgraph-overview/{identifier}'

def convert_relref(content, file_path):
    """Convert Hugo relref shortcodes to Docusaurus document references"""
    
    # First, fix double-nested links: [text]([identifier](identifier)) -> [text](identifier)
    # Pattern: [text]([identifier](path))
    def fix_double_nested(match):
        text = match.group(1)
        identifier = match.group(2)
        path = match.group(3)
        # Use the path if it looks valid, otherwise use identifier
        if path and path != identifier:
            return f'[{text}]({path})'
        doc_id = find_document_id(identifier, file_path)
        return f'[{text}]({doc_id})'
    
    content = re.sub(r'\[([^\]]+)\]\(\[([^\]]+)\]\(([^)]+)\)\)', fix_double_nested, content)
    
    # Pattern to match relref in link context: [text]({{< relref identifier="something">}})
    # This pattern matches: [text]({{< relref identifier="id">}})
    def replace_relref_in_link(match):
        text = match.group(1)
        identifier = match.group(2)
        doc_id = find_document_id(identifier, file_path)
        return f'[{text}]({doc_id})'
    
    # Match [text]({{< relref identifier="something">}})
    content = re.sub(r'\[([^\]]+)\]\(\{\{<\s*relref\s+identifier\s*=\s*"([^"]+)"\s*>\}\}\)', replace_relref_in_link, content)
    content = re.sub(r'\[([^\]]+)\]\(\{\{<\s*relref\s+identifer\s*=\s*"([^"]+)"\s*>\}\}\)', replace_relref_in_link, content)  # typo
    content = re.sub(r'\[([^\]]+)\]\(\{\{<\s*relref\s+"([^"]+)"\s*>\}\}\)', replace_relref_in_link, content)
    
    # Pattern to match standalone relref: {{< relref identifier="something">}}
    def replace_standalone_relref(match):
        identifier = match.group(1)
        doc_id = find_document_id(identifier, file_path)
        return f'[{identifier}]({doc_id})'
    
    # Match standalone {{< relref identifier="something">}}
    content = re.sub(r'\{\{<\s*relref\s+identifier\s*=\s*"([^"]+)"\s*>\}\}', replace_standalone_relref, content)
    content = re.sub(r'\{\{<\s*relref\s+identifer\s*=\s*"([^"]+)"\s*>\}\}', replace_standalone_relref, content)  # typo
    content = re.sub(r'\{\{<\s*relref\s+"([^"]+)"\s*>\}\}', replace_standalone_relref, content)
    
    return content

def fix_file(filepath):
    """Fix a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        fixed = convert_relref(content, filepath)
        
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
    
    print(f"\nFixed relref in {fixed} files")

if __name__ == '__main__':
    main()
