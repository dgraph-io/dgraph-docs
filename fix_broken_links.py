#!/usr/bin/env python3
"""
Fix broken document references that weren't properly converted
"""

import re
from pathlib import Path

# Mapping of identifiers to document paths
DOC_MAP = {
    'learning-environment': '/learn/',
    'monitoring': '/dgraph-overview/admin/observability/monitoring',
    'admin': '/dgraph-overview/admin/',
    'production-checklist': '/dgraph-overview/installation/production-checklist',
    'clients': '/dgraph-overview/clients/',
    'ports-usage': '/dgraph-overview/admin/security/ports-usage',
    'dgraph-zero': '/dgraph-overview/admin/dgraph-zero',
    'binary-backups': '/dgraph-overview/admin/enterprise-features/binary-backups',
    'dgraph-administration': '/dgraph-overview/admin/dgraph-administration',
    'single-host-setup': '/dgraph-overview/installation/single-host-setup',
    'encryption-at-rest': '/dgraph-overview/admin/enterprise-features/encryption-at-rest',
    'multitenancy': '/dgraph-overview/admin/enterprise-features/multitenancy',
    'data-compression': '/dgraph-overview/admin/data-compression',
    'download': '/dgraph-overview/installation/download',
    'bulk-loader': '/dgraph-overview/migration/bulk-loader',
    'live-loader': '/dgraph-overview/migration/live-loader',
    'import-data': '/dgraph-overview/migration/import-data',
    'export-data': '/dgraph-overview/migration/export-data',
    'dql-rdf': '/dgraph-overview/dql/dql-rdf',
    'json-mutation-format': '/dgraph-overview/dql/json-mutation-format',
    'graphql-dql': '/graphql-dql/',
    'dgraph-architecture': '/dgraph-overview/installation/dgraph-architecture',
    'functions': '/dgraph-overview/dql/query/functions',
    'facets': '/dgraph-overview/dql/query/facets',
    'variables': '/dgraph-overview/dql/query/variables',
    'cascade-directive': '/dgraph-overview/dql/query/directive/cascade-directive',
    'dql-query': '/dgraph-overview/dql/query/dql-query',
    'cli/config': '/dgraph-overview/cli/config',
    'cli/superflags': '/dgraph-overview/cli/superflags',
    'cli/live': '/dgraph-overview/cli/live',
}

def fix_links(content):
    """Fix broken document references"""
    # Pattern to match [text](identifier) where identifier is not a full path
    def replace_link(match):
        text = match.group(1)
        identifier = match.group(2)
        
        # Skip if already a full path (starts with /)
        if identifier.startswith('/'):
            return match.group(0)
        
        # Skip if it's a URL (starts with http)
        if identifier.startswith('http'):
            return match.group(0)
        
        # Skip if it's an anchor link (starts with #)
        if identifier.startswith('#'):
            return match.group(0)
        
        # Skip if it's a relative path (contains /)
        if '/' in identifier and not identifier.startswith('/'):
            # Check if it's in our map
            if identifier in DOC_MAP:
                return f'[{text}]({DOC_MAP[identifier]})'
            return match.group(0)
        
        # Check if identifier is in our map
        if identifier in DOC_MAP:
            return f'[{text}]({DOC_MAP[identifier]})'
        
        # If not found, try to find the document
        docs_dir = Path('docusaurus-docs/docs')
        possible_paths = [
            docs_dir / identifier / 'index.md',
            docs_dir / f'{identifier}.md',
        ]
        
        # Search in subdirectories
        for subdir in docs_dir.rglob('*'):
            if subdir.is_dir():
                possible_paths.extend([
                    subdir / f'{identifier}.md',
                    subdir / identifier / 'index.md',
                ])
        
        # Check if file exists
        for path in possible_paths:
            if path.exists() and path.is_file():
                try:
                    rel_path = path.relative_to(docs_dir)
                    doc_id = str(rel_path).replace('.md', '')
                    if doc_id.endswith('/index'):
                        doc_id = doc_id[:-6]
                    if doc_id:
                        return f'[{text}](/dgraph-overview/{doc_id})'
                except:
                    pass
        
        # Fallback: assume it's a document ID in the same section
        return f'[{text}](/dgraph-overview/{identifier})'
    
    # Match [text](identifier) where identifier doesn't start with /, http, or #
    content = re.sub(r'\[([^\]]+)\]\(([^/)][^)]*)\)', replace_link, content)
    
    return content

def fix_file(filepath):
    """Fix a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        fixed = fix_links(content)
        
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
    
    print(f"\nFixed broken links in {fixed} files")

if __name__ == '__main__':
    main()

