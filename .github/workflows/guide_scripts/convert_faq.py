#!/usr/bin/env python3
"""
Script to convert FAQ macros in markdown files to collapsible question admonitions.

Removes macro definitions and converts:
    {{ faq("id") }}
    Question text here?
    {{ answer() }}
    
    Answer content...
    {{ endfaq() }}

To:
    ??? question: "Question text here?"

        Answer content...
"""

import re
import sys
from pathlib import Path


def remove_macro_definitions(content: str) -> str:
    """Remove {% macro ... %} ... {% endmacro %} blocks."""
    # Match from {% macro to {% endmacro %} including newlines
    pattern = r'\{%\s*macro\s+\w+\([^)]*\)\s*%\}.*?\{%\s*endmacro\s*%\}\n*'
    return re.sub(pattern, '', content, flags=re.DOTALL)


def convert_faq_blocks(content: str) -> str:
    """Convert {{ faq() }}...{{ answer() }}...{{ endfaq() }} to admonitions."""
    # Pattern to match the entire FAQ block
    pattern = r'\{\{\s*faq\(["\']([^"\']+)["\']\)\s*\}\}\n(.+?)\n\{\{\s*answer\(\)\s*\}\}\n(.*?)\{\{\s*endfaq\(\)\s*\}\}'
    
    def replace_faq(match):
        faq_id = match.group(1)
        question = match.group(2).strip()
        answer_content = match.group(3)
        
        # Indent the answer content by 4 spaces
        indented_lines = []
        for line in answer_content.split('\n'):
            if line.strip():  # Non-empty line
                indented_lines.append('    ' + line)
            else:  # Empty line
                indented_lines.append('')
        
        # Remove trailing empty lines from indented content
        while indented_lines and not indented_lines[-1].strip():
            indented_lines.pop()
        
        indented_answer = '\n'.join(indented_lines)
        
        # Build the admonition
        return f'??? Question "{question}"\n\n{indented_answer}\n'
    
    return re.sub(pattern, replace_faq, content, flags=re.DOTALL)


def process_file(input_path: str | Path, output_path: str | Path | None = None) -> None:
    """Process a markdown file and convert FAQ macros to admonitions."""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Step 1: Remove macro definitions
    content = remove_macro_definitions(content)
    
    # Step 2: Convert FAQ blocks to admonitions
    content = convert_faq_blocks(content)
    
    # Determine output path
    if output_path is None:
        output_path = input_path
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Processed: {input_path} -> {output_path}")


def main():
    if len(sys.argv) < 2:
        # Default to processing the FAQ file
        input_file = Path.cwd() / 'guide' / '14-faq.md'
    else:
        input_file = sys.argv[1]
    
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    process_file(input_file, output_file)


if __name__ == '__main__':
    main()
