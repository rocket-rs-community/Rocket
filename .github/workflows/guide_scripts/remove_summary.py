#!/usr/bin/env python3
"""
Script to remove +++ summary +++ front matter blocks from markdown files.
"""

import os
import re
from pathlib import Path


def remove_summary_block(content: str) -> str:
    """Remove the +++ summary = ... +++ block from the beginning of content."""
    # Pattern matches +++ followed by any content until the closing +++
    # at the start of the file, including trailing newlines
    pattern = r'^\+\+\+\n.*?\n\+\+\+\n*'
    return re.sub(pattern, '', content, count=1, flags=re.DOTALL)


def process_file(filepath: Path) -> bool:
    """Process a single file, returning True if changes were made."""
    content = filepath.read_text(encoding='utf-8')
    
    if not content.startswith('+++'):
        return False
    
    new_content = remove_summary_block(content)
    
    if new_content != content:
        filepath.write_text(new_content, encoding='utf-8')
        return True
    
    return False


def main():
    guide_dir = Path.cwd() / 'guide'
    
    if not guide_dir.exists():
        print(f"Error: Directory '{guide_dir}' not found")
        return
    
    processed = 0
    modified = 0
    
    for filepath in sorted(guide_dir.glob('*.md')):
        processed += 1
        if process_file(filepath):
            modified += 1
            print(f"Modified: {filepath.name}")
        else:
            print(f"Skipped:  {filepath.name} (no summary block)")
    
    print(f"\nProcessed {processed} files, modified {modified}")


if __name__ == '__main__':
    main()
