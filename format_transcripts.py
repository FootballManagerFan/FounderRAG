"""
Auto-format transcript files to have proper line breaks.

This script:
1. Reads all .md files in the transcripts folder
2. Adds line breaks after sentences (periods followed by spaces)
3. Preserves existing line breaks
4. Saves the formatted version back to the file

Usage:
    python format_transcripts.py              # Format all transcripts
    python format_transcripts.py --check      # Check which files need formatting
    python format_transcripts.py --dry-run    # Show what would be changed without saving
"""

import os
import re
import argparse
from pathlib import Path


def format_transcript(file_path: str, dry_run: bool = False) -> bool:
    """
    Format a transcript file by adding line breaks after sentences.
    
    Args:
        file_path: Path to the markdown file
        dry_run: If True, don't actually modify the file
        
    Returns:
        True if file was modified or would be modified, False otherwise
    """
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Check current line count
        line_count = content.count('\n')
        
        # Skip if file is already well-formatted (has multiple lines)
        if line_count > 50:  # If already has decent line breaks
            print(f"  [OK] {os.path.basename(file_path)} already formatted ({line_count} lines)")
            return False
        
        # Add line breaks after sentences
        # Pattern: period followed by space and capital letter or quotes
        content = re.sub(r'\. ([A-Z"])', r'.\n\n\1', content)
        
        # Add line breaks after question marks and exclamation points
        content = re.sub(r'([!?]) ([A-Z"])', r'\1\n\n\2', content)
        
        # Clean up multiple consecutive newlines (max 2)
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Write back if changed
        if content != original_content:
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            new_line_count = content.count('\n')
            action = "[DRY-RUN]" if dry_run else "[DONE]"
            print(f"  {action} Formatted {os.path.basename(file_path)}: {line_count} -> {new_line_count} lines")
            return True
        else:
            print(f"  [SKIP] No changes needed for {os.path.basename(file_path)}")
            return False
            
    except Exception as e:
        print(f"  [ERROR] Error formatting {os.path.basename(file_path)}: {e}")
        return False


def format_all_transcripts(directory: str = "transcripts", dry_run: bool = False):
    """Format all markdown files in the transcripts directory."""
    
    action = "Checking" if dry_run else "Formatting"
    print(f"{action} transcripts in '{directory}' folder...")
    print("=" * 60)
    
    # Find all .md files
    md_files = list(Path(directory).glob("*.md"))
    
    if not md_files:
        print(f"No .md files found in {directory}/")
        return
    
    print(f"Found {len(md_files)} files to process\n")
    
    formatted_count = 0
    for file_path in sorted(md_files):
        if format_transcript(str(file_path), dry_run):
            formatted_count += 1
    
    print("\n" + "=" * 60)
    if dry_run:
        print(f"Check complete! {formatted_count}/{len(md_files)} files would be formatted")
        print("Run without --dry-run to actually format the files")
    else:
        print(f"Complete! Formatted {formatted_count}/{len(md_files)} files")
        if formatted_count > 0:
            print("\nYou can now run: python create_database.py")


def main():
    parser = argparse.ArgumentParser(description="Format transcript files with proper line breaks")
    parser.add_argument("--check", action="store_true", help="Check which files need formatting")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed without saving")
    parser.add_argument("--directory", default="transcripts", help="Directory containing transcript files")
    
    args = parser.parse_args()
    
    # Check is same as dry-run
    dry_run = args.check or args.dry_run
    
    format_all_transcripts(args.directory, dry_run)


if __name__ == "__main__":
    main()
