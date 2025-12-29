#!/usr/bin/env python3
"""
Script to convert admonitions from old format to new markdown format.

Old format:
    ! note: Some text

      more text

New format:
    !!! note

        Some text

        more text
"""

import re
import sys
from pathlib import Path


def convert_admonitions(content: str) -> str:
    """Convert admonitions from old format to new markdown format."""
    lines = content.split('\n')
    result = []
    i = 0
    
    # Pattern to match admonition start: ! note: or ! warning:
    admonition_pattern = re.compile(r'^! (note|warning|tip):?\s*(.*)$')
    
    while i < len(lines):
        line = lines[i]
        match = admonition_pattern.match(line)
        
        if match:
            admonition_type = match.group(1)
            first_line_text = match.group(2).strip()
            
            # Start the new admonition format
            result.append(f'!!! {admonition_type}')
            result.append('')  # Empty line after the admonition header
            
            # Add the first line text if present (with 4-space indent)
            if first_line_text:
                result.append(f'    {first_line_text}')
            
            i += 1
            
            # Process continuation lines (lines that are indented with 2 spaces)
            while i < len(lines):
                next_line = lines[i]
                
                # Check if line is part of the admonition block
                # It should be either empty or start with at least 2 spaces
                if next_line == '':
                    # Empty line - keep it but check if we're still in the block
                    # Look ahead to see if next non-empty line is still indented
                    j = i + 1
                    while j < len(lines) and lines[j] == '':
                        j += 1
                    
                    if j < len(lines) and lines[j].startswith('  '):
                        # Still in the admonition block
                        result.append('')
                        i += 1
                    else:
                        # End of admonition block
                        break
                elif next_line.startswith('  '):
                    # Continuation line - convert 2-space indent to 4-space
                    # Remove the original 2-space indent and add 4-space indent
                    stripped = next_line[2:]  # Remove first 2 spaces
                    result.append(f'    {stripped}')
                    i += 1
                else:
                    # Not part of the admonition anymore
                    break
        else:
            result.append(line)
            i += 1
    
    return '\n'.join(result)


def process_file(filepath: Path) -> bool:
    """Process a single file and return True if changes were made."""
    content = filepath.read_text(encoding='utf-8')
    new_content = convert_admonitions(content)
    
    if content != new_content:
        filepath.write_text(new_content, encoding='utf-8')
        return True
    return False


def main():
    if len(sys.argv) < 2:
        # Default to processing all .md files in the guide directory
        guide_dir = Path.cwd() / 'guide'
        
        if guide_dir.exists():
            files = list(guide_dir.glob('*.md'))
        else:
            print("Usage: python convert_admonitions.py <file.md> [file2.md ...]")
            print("       or run from directory containing 'guide' folder")
            sys.exit(1)
    else:
        files = [Path(f) for f in sys.argv[1:]]
    
    changed_count = 0
    for filepath in files:
        if not filepath.exists():
            print(f"Warning: {filepath} does not exist, skipping")
            continue
        
        if process_file(filepath):
            print(f"Converted: {filepath}")
            changed_count += 1
        else:
            print(f"No changes: {filepath}")
    
    print(f"\nTotal files modified: {changed_count}")


if __name__ == '__main__':
    main()
