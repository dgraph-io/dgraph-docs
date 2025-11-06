#!/usr/bin/env python3
"""
Replace <!-- runnable code block --> comments with RunnableCodeBlock component
"""

import re
from pathlib import Path

def convert_runnable_blocks(content):
    """Convert runnable code block comments to RunnableCodeBlock component"""
    
    # Pattern to match:
    # <!-- runnable code block -->
    # {code}
    # <!-- end runnable -->
    
    # Or just:
    # <!-- runnable code block -->
    # {code}
    # (without end comment)
    
    # First, handle blocks with end comments
    def replace_with_end_comment(match):
        code = match.group(1)
        # Remove leading/trailing newlines but preserve indentation
        code = code.strip()
        return f'<RunnableCodeBlock>\n\n```dql\n{code}\n```\n\n</RunnableCodeBlock>'
    
    # Match <!-- runnable code block --> ... code ... <!-- end runnable -->
    content = re.sub(
        r'<!--\s*runnable code block\s*-->\s*\n(.*?)\n<!--\s*end runnable\s*-->',
        replace_with_end_comment,
        content,
        flags=re.DOTALL
    )
    
    # Now handle blocks without end comments
    # This is trickier - we need to find the code block that follows
    # Pattern: <!-- runnable code block --> followed by a code block (```...```)
    def replace_without_end_comment(match):
        code = match.group(1)
        code = code.strip()
        return f'<RunnableCodeBlock>\n\n```dql\n{code}\n```\n\n</RunnableCodeBlock>'
    
    # Match <!-- runnable code block --> followed by code block
    # This pattern looks for the comment, then captures everything until the next ``` or blank line + ```
    content = re.sub(
        r'<!--\s*runnable code block\s*-->\s*\n```(?:dql|dgraph|graphql)?\s*\n(.*?)\n```',
        replace_without_end_comment,
        content,
        flags=re.DOTALL
    )
    
    # Handle case where code is not in a code block (just plain text after comment)
    # Match <!-- runnable code block --> followed by code (not in ```)
    def replace_plain_code(match):
        code = match.group(1)
        # Remove the code block markers if they exist
        code = re.sub(r'^```.*?\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'\n```$', '', code, flags=re.MULTILINE)
        code = code.strip()
        return f'<RunnableCodeBlock>\n\n```dql\n{code}\n```\n\n</RunnableCodeBlock>'
    
    # Match <!-- runnable code block --> followed by code until <!-- end runnable --> or next heading or blank line
    content = re.sub(
        r'<!--\s*runnable code block\s*-->\s*\n((?:[^{]|{(?!{))*(?:\{[^{]|\{[^{]*\}[^}])*[^}]*?)(?=\n\n|\n#|\n<!--|$)',
        replace_plain_code,
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
        
        # First, handle blocks with explicit end comments
        def replace_block_with_end(match):
            code = match.group(1)
            code = code.strip()
            return f'<RunnableCodeBlock>\n\n```dql\n{code}\n```\n\n</RunnableCodeBlock>'
        
        content = re.sub(
            r'<!--\s*runnable code block\s*-->\s*\n(.*?)\n<!--\s*end runnable\s*-->',
            replace_block_with_end,
            content,
            flags=re.DOTALL
        )
        
        # Then handle blocks where code follows directly (no code block markers)
        # Find comment, then capture code until next blank line or heading
        def replace_block_direct(match):
            full_match = match.group(0)
            code_start = full_match.find('-->') + 3
            code_section = full_match[code_start:].strip()
            
            # Remove code block markers if present
            if code_section.startswith('```'):
                # Extract code from ```dql ... ```
                code_match = re.search(r'```(?:dql|dgraph|graphql)?\s*\n(.*?)\n```', code_section, re.DOTALL)
                if code_match:
                    code = code_match.group(1).strip()
                else:
                    code = code_section.strip()
            else:
                code = code_section.strip()
            
            return f'<RunnableCodeBlock>\n\n```dql\n{code}\n```\n\n</RunnableCodeBlock>'
        
        # Match from comment to next blank line (double newline) or heading
        content = re.sub(
            r'<!--\s*runnable code block\s*-->\s*\n(.*?)(?=\n\n|\n#|\Z)',
            replace_block_direct,
            content,
            flags=re.DOTALL
        )
        
        if content != original:
            # Add import at the top if not present
            if 'import RunnableCodeBlock' not in content:
                if content.startswith('---'):
                    # Has frontmatter
                    frontmatter_end = content.find('---', 3)
                    if frontmatter_end != -1:
                        imports = '\nimport RunnableCodeBlock from \'@site/src/components/RunnableCodeBlock\';\n\n'
                        content = content[:frontmatter_end + 3] + imports + content[frontmatter_end + 3:]
                else:
                    # No frontmatter
                    imports = 'import RunnableCodeBlock from \'@site/src/components/RunnableCodeBlock\';\n\n'
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
    
    print(f"\nFixed runnable blocks in {fixed} files")

if __name__ == '__main__':
    main()

