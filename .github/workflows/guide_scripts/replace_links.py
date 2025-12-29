#!/usr/bin/env python3
"""
Script to replace certain strings in markdown files in the guide directory.

Handles:
1. Simple string replacements (defined in REPLACEMENTS dict)
2. Relative link transformations: ../[name]/#anchor -> ./xx-[name].md#anchor
"""

import os
import re
from pathlib import Path

# Directory containing the guide files
GUIDE_DIR = Path.cwd() / "guide"

# Simple find/replace mappings - add more as needed
REPLACEMENTS = {
    "@api/master/rocket": "https://docs.rs/rocket-community/latest/rocket_community",
    "(faq/)": "(./14-faq.md)",
    "@github": "https://github.com/rocket-rs-community/Rocket",
    "@git": "https://github.com/rocket-rs-community/Rocket/tree/master"
    # Add more simple replacements here:
    # "old_string": "new_string",
}

def build_file_mapping(guide_dir: Path) -> dict[str, str]:
    """
    Build a mapping from file base names (without index) to full filenames.
    
    E.g., "requests" -> "05-requests.md"
    """
    mapping = {}
    for file in guide_dir.glob("*.md"):
        filename = file.name
        # Match pattern like "05-requests.md"
        match = re.match(r"^(\d{2})-(.+)\.md$", filename)
        if match:
            base_name = match.group(2)  # e.g., "requests"
            mapping[base_name] = filename
    return mapping


def transform_relative_links(content: str, file_mapping: dict[str, str]) -> str:
    """
    Transform relative links from ../[name]/ or ../[name]/#anchor to ./xx-[name].md or ./xx-[name].md#anchor
    
    Handles patterns like:
    - ../requests/#body-data -> ./05-requests.md#body-data
    - ../state/#managed-state -> ./07-state.md#managed-state
    - ../requests/ -> ./05-requests.md
    - ../configuration -> ./10-configuration.md
    """
    # Pattern matches: ../name with optional trailing slash and optional #anchor
    # The anchor part is optional
    pattern = r"\.\./([a-z-]+)/?(?:#([a-z0-9-]+))?"
    
    def replace_link(match):
        name = match.group(1)
        anchor = match.group(2)  # May be None if no anchor
        
        if name in file_mapping:
            new_filename = file_mapping[name]
            if anchor:
                return f"./{new_filename}#{anchor}"
            else:
                return f"./{new_filename}"
        else:
            # If we can't find the mapping, leave it unchanged
            print(f"  Warning: Could not find mapping for '{name}'")
            return match.group(0)
    
    return re.sub(pattern, replace_link, content)


def apply_simple_replacements(content: str) -> str:
    """Apply all simple string replacements."""
    for old, new in REPLACEMENTS.items():
        content = content.replace(old, new)
    return content


def process_file(file_path: Path, file_mapping: dict[str, str], dry_run: bool = False) -> int:
    """
    Process a single markdown file.
    
    Returns the number of changes made.
    """
    original_content = file_path.read_text(encoding="utf-8")
    
    # Apply transformations
    content = apply_simple_replacements(original_content)
    content = transform_relative_links(content, file_mapping)
    
    # Count changes
    changes = 0
    if content != original_content:
        # Count simple replacements
        for old in REPLACEMENTS:
            changes += original_content.count(old)
        
        # Count relative link transformations
        pattern = r"\.\./([a-z-]+)/?#([a-z0-9-]+)"
        changes += len(re.findall(pattern, original_content))
        
        if not dry_run:
            file_path.write_text(content, encoding="utf-8")
    
    return changes


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Replace strings and transform links in guide markdown files."
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would be changed without making changes"
    )
    parser.add_argument(
        "--file", "-f",
        type=str,
        help="Process only a specific file (relative to guide directory)"
    )
    args = parser.parse_args()
    
    if not GUIDE_DIR.exists():
        print(f"Error: Guide directory not found: {GUIDE_DIR}")
        return 1
    
    # Build the file mapping
    file_mapping = build_file_mapping(GUIDE_DIR)
    print(f"Found {len(file_mapping)} indexed files in guide directory")
    print(f"File mapping: {file_mapping}")
    print()
    
    # Determine which files to process
    if args.file:
        files = [GUIDE_DIR / args.file]
    else:
        files = sorted(GUIDE_DIR.glob("*.md"))
    
    total_changes = 0
    files_changed = 0
    
    for file_path in files:
        if not file_path.exists():
            print(f"Warning: File not found: {file_path}")
            continue
            
        print(f"Processing: {file_path.name}")
        changes = process_file(file_path, file_mapping, dry_run=args.dry_run)
        
        if changes > 0:
            files_changed += 1
            total_changes += changes
            print(f"  -> {changes} replacement(s)")
    
    print()
    print(f"Summary: {total_changes} total replacements in {files_changed} file(s)")
    
    if args.dry_run:
        print("(Dry run - no files were modified)")
    
    return 0


if __name__ == "__main__":
    exit(main())
