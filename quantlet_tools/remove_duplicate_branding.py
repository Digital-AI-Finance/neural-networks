"""
Remove all Quantlet branding blocks from .tex files

This script removes all auto-generated branding blocks
(identified by the comment: % Quantlet branding (auto-generated))
"""

import re
from pathlib import Path


def remove_branding_from_file(tex_file):
    """Remove all branding blocks from a .tex file"""
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match entire branding block
    pattern = r'\n% Quantlet branding \(auto-generated\).*?\\end\{tikzpicture\}\n'

    # Count matches
    matches = re.findall(pattern, content, re.DOTALL)
    count = len(matches)

    if count == 0:
        print(f"[SKIP] {tex_file.name}: No branding found")
        return False

    # Remove all branding blocks
    cleaned = re.sub(pattern, '\n', content, flags=re.DOTALL)

    # Write back
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(cleaned)

    print(f"[OK] {tex_file.name}: Removed {count} branding block(s)")
    return True


def main():
    """Remove branding from all .tex files in parent directory"""
    parent_dir = Path(__file__).parent.parent

    # Find all .tex files
    tex_files = list(parent_dir.glob("*.tex"))

    if not tex_files:
        print("No .tex files found in parent directory")
        return

    print(f"Found {len(tex_files)} .tex file(s)")
    print("="*60)

    updated_count = 0
    for tex_file in tex_files:
        if remove_branding_from_file(tex_file):
            updated_count += 1

    print("="*60)
    print(f"Updated {updated_count} file(s)")


if __name__ == "__main__":
    main()
