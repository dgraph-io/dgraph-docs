#!/usr/bin/env python3
"""
Replace Hugo {{< highlight >}} shortcodes with Highlight component
"""

import re
from pathlib import Path

def convert_highlight(content):
    """Convert Hugo highlight shortcodes to Highlight component"""
    
    # Pattern: {{< highlight language "params" >}}code{{< / highlight >}}
    # Example: {{< highlight json "linenos=false,hl_lines=7 " >}}code{{< / highlight >}}
    
    def replace_highlight(match):
        full_match = match.group(0)
        language = match.group(1) if match.group(1) else 'text'
        params = match.group(2) if match.group(2) else ''
        code = match.group(3)
        
        # Parse parameters
        linenos = 'false'
        hl_lines = None
        
        # Extract linenos
        linenos_match = re.search(r'linenos=([^,\s"]+)', params)
        if linenos_match:
            linenos = linenos_match.group(1)
        
        # Extract hl_lines
        hl_lines_match = re.search(r'hl_lines=([^"\s]+)', params)
        if hl_lines_match:
            hl_lines = hl_lines_match.group(1).strip()
        
        # Build component props
        props = []
        if language:
            props.append(f'language="{language}"')
        if linenos and linenos.lower() != 'false':
            props.append(f'linenos="{linenos}"')
        if hl_lines:
            props.append(f'hl_lines="{hl_lines}"')
        
        props_str = ' '.join(props) if props else ''
        
        return f'<Highlight {props_str}>\n\n```{language}\n{code.strip()}\n```\n\n</Highlight>'
    
    # Match {{< highlight lang "params" >}}code{{< / highlight >}}
    content = re.sub(
        r'\{\{<\s*highlight\s+(\w+)?\s*"([^"]*)"\s*>\}\}(.*?)\{\{<\s*/\s*highlight\s*>\}\}',
        replace_highlight,
        content,
        flags=re.DOTALL
    )
    
    return content

def fix_file(filepath):
    """Fix a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Match {{< highlight lang "params" >}}code{{< / highlight >}}
        def replace_highlight(match):
            language = match.group(1) if match.group(1) else 'text'
            params = match.group(2) if match.group(2) else ''
            code = match.group(3).strip()
            
            # Parse parameters
            linenos = 'false'
            hl_lines = None
            
            # Extract linenos
            linenos_match = re.search(r'linenos=([^,\s"]+)', params)
            if linenos_match:
                linenos = linenos_match.group(1)
            
            # Extract hl_lines
            hl_lines_match = re.search(r'hl_lines=([^"\s]+)', params)
            if hl_lines_match:
                hl_lines = hl_lines_match.group(1).strip()
            
            # Build component props
            props = []
            if language:
                props.append(f'language="{language}"')
            if linenos and linenos.lower() != 'false':
                props.append(f'linenos="{linenos}"')
            if hl_lines:
                props.append(f'hl_lines="{hl_lines}"')
            
            props_str = ' '.join(props) if props else ''
            
            return f'<Highlight {props_str}>\n\n```{language}\n{code}\n```\n\n</Highlight>'
        
        content = re.sub(
            r'\{\{<\s*highlight\s+(\w+)?\s*"([^"]*)"\s*>\}\}(.*?)\{\{<\s*/\s*highlight\s*>\}\}',
            replace_highlight,
            content,
            flags=re.DOTALL
        )
        
        if content != original:
            # Add import at the top if not present
            if 'import Highlight' not in content:
                if content.startswith('---'):
                    # Has frontmatter
                    frontmatter_end = content.find('---', 3)
                    if frontmatter_end != -1:
                        imports = '\nimport Highlight from \'@site/src/components/Highlight\';\n\n'
                        content = content[:frontmatter_end + 3] + imports + content[frontmatter_end + 3:]
                else:
                    # No frontmatter
                    imports = 'import Highlight from \'@site/src/components/Highlight\';\n\n'
                    content = imports + content
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
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
    
    print(f"\nFixed highlight shortcodes in {fixed} files")

if __name__ == '__main__':
    main()

