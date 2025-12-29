#!/usr/bin/env python3
"""
Script to elaborate reference links containing backticks in markdown files.

For each markdown file in ./guide:
1. Find all reference definitions (e.g., [`title`]: url)
2. Error if any reference is defined multiple times
3. Find references with backticks in the title
4. Replace inline references like [`title`] with [`title`](url)
"""

import os
import re
import sys
from pathlib import Path


def find_reference_definitions(content: str) -> dict[str, tuple[str, int]]:
    """
    Find all reference definitions in the content.
    Returns a dict mapping reference title to (url, line_number).
    Raises an error if a reference is defined multiple times.
    """
    # Pattern to match reference definitions: [title]: url
    # The title can contain backticks and other characters
    # Reference definitions are at the start of a line
    pattern = r'^(\[([^\]]+)\]):\s*(.+)$'
    
    definitions = {}
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        match = re.match(pattern, line)
        if match:
            full_ref = match.group(1)  # [title]
            title = match.group(2)      # title (without brackets)
            url = match.group(3).strip()
            
            if title in definitions:
                prev_line = definitions[title][1]
                raise ValueError(
                    f"Duplicate reference definition '{title}' "
                    f"found at line {line_num} (previously defined at line {prev_line})"
                )
            
            definitions[title] = (url, line_num)
    
    return definitions


def find_backtick_references(definitions: dict[str, tuple[str, int]]) -> dict[str, str]:
    """
    Filter definitions to only those with backticks in the title.
    Returns a dict mapping title to url.
    """
    return {
        title: url
        for title, (url, _) in definitions.items()
        if '`' in title
    }


def elaborate_backtick_links(content: str, backtick_refs: dict[str, str]) -> str:
    """
    Replace inline backtick reference links with full markdown links.
    
    For example:
    - [`some title`] becomes [`some title`](url)
    - But [`some title`](existing) is left alone (already elaborated)
    - And [`some title`]: url is left alone (definition line)
    """
    if not backtick_refs:
        return content
    
    # For each backtick reference, replace [title] with [title](url)
    # But only if it's not already followed by (url) or : url
    
    for title, url in backtick_refs.items():
        # Escape special regex characters in the title
        escaped_title = re.escape(title)
        
        # Pattern matches [title] but NOT:
        # - [title](something) - already a full link
        # - [title]: something - a definition
        # Use negative lookahead to exclude these cases
        pattern = rf'\[{escaped_title}\](?!\(|:)'
        
        replacement = f'[{title}]({url})'
        
        content = re.sub(pattern, replacement, content)
    
    return content


def process_file(filepath: Path) -> tuple[bool, str]:
    """
    Process a single markdown file.
    Returns (success, message).
    """
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return False, f"Error reading file: {e}"
    
    # Find all reference definitions
    try:
        definitions = find_reference_definitions(content)
    except ValueError as e:
        return False, str(e)
    
    # Find references with backticks
    backtick_refs = find_backtick_references(definitions)
    
    if not backtick_refs:
        return True, "No backtick references found"
    
    # Elaborate the backtick links
    new_content = elaborate_backtick_links(content, backtick_refs)
    
    # Count changes
    changes = 0
    for title in backtick_refs:
        # Count occurrences that were changed (not definitions)
        escaped_title = re.escape(title)
        # Count in original that would match (not definitions, not already linked)
        original_matches = len(re.findall(rf'\[{escaped_title}\](?!\(|:)', content))
        changes += original_matches
    
    if changes == 0:
        return True, f"Found {len(backtick_refs)} backtick reference(s), but no inline references to elaborate"
    
    # Write the updated content
    try:
        filepath.write_text(new_content, encoding='utf-8')
    except Exception as e:
        return False, f"Error writing file: {e}"
    
    return True, f"Elaborated {changes} reference(s) from {len(backtick_refs)} backtick definition(s)"


def main():
    guide_dir = Path.cwd() / 'guide'
    
    if not guide_dir.exists():
        print(f"Error: Directory '{guide_dir}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Get all markdown files
    md_files = sorted(guide_dir.glob('*.md'))
    
    if not md_files:
        print(f"No markdown files found in '{guide_dir}'", file=sys.stderr)
        sys.exit(1)
    
    print(f"Processing {len(md_files)} markdown file(s) in '{guide_dir}'...\n")
    
    success_count = 0
    error_count = 0
    
    for filepath in md_files:
        print(f"Processing: {filepath.name}")
        success, message = process_file(filepath)
        
        if success:
            print(f"  ✓ {message}")
            success_count += 1
        else:
            print(f"  ✗ ERROR: {message}", file=sys.stderr)
            error_count += 1
            print(f"\nStopping due to error in {filepath.name}", file=sys.stderr)
            sys.exit(1)
    
    print(f"\nDone! Processed {success_count} file(s) successfully.")


if __name__ == '__main__':
    main()
