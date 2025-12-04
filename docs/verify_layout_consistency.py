"""
Layout Consistency Verification Script

Compares CSS values across all layout files to ensure visual consistency.
Checks: sidebar width, top nav, spacing, colors, fonts.

Usage: python verify_layout_consistency.py
"""

import re
from pathlib import Path

DOCS_DIR = Path(__file__).parent
LAYOUTS_DIR = DOCS_DIR / '_layouts'

# Expected consistent values (Blue Professional theme)
EXPECTED_VALUES = {
    'sidebar_width': '260px',
    'container_max_width': '1600px',
    'top_nav_padding': '10px 20px',
    'top_nav_gap': '25px',
    'top_nav_font_size': '0.9rem',
    'sidebar_header_padding': '15px',
    'sidebar_logo_width': '36px',
    'sidebar_logo_height': '36px',
    'course_title_font_size': '16px',
    'nav_padding': '8px 0',
    'part_section_summary_padding': '10px 15px',
    'part_section_summary_font_size': '11px',
    'part_section_link_padding': '6px 15px 6px 25px',
    'part_section_link_font_size': '12px',
    'primary_navy': '#1e3a5f',
    'primary_blue': '#2563eb',
    'background': '#f8fafc',
    'border': '#e2e8f0',
}


def extract_css_value(content, property_pattern):
    """Extract CSS value matching pattern."""
    match = re.search(property_pattern, content)
    return match.group(1) if match else None


def check_layout_file(filepath):
    """Check a single layout file for consistency."""
    content = filepath.read_text(encoding='utf-8')
    issues = []
    matches = []

    # Define patterns to extract
    patterns = {
        'sidebar_width': r'\.sidebar\s*\{[^}]*width:\s*([^;]+);',
        'container_max_width': r'\.container\s*\{[^}]*max-width:\s*([^;]+);',
        'top_nav_padding': r'\.top-nav\s*\{[^}]*padding:\s*([^;]+);',
        'top_nav_gap': r'\.top-nav\s*\{[^}]*gap:\s*([^;]+);',
        'top_nav_font_size': r'\.top-nav a\s*\{[^}]*font-size:\s*([^;]+);',
        'sidebar_header_padding': r'\.sidebar-header\s*\{[^}]*padding:\s*([^;]+);',
        'sidebar_logo_width': r'\.sidebar-logo\s*\{[^}]*width:\s*([^;]+);',
        'course_title_font_size': r'\.course-title\s*\{[^}]*font-size:\s*([^;]+);',
        'part_section_summary_font_size': r'\.part-section summary\s*\{[^}]*font-size:\s*([^;]+);',
        'part_section_link_font_size': r'\.part-section a\s*\{[^}]*font-size:\s*([^;]+);',
    }

    for name, pattern in patterns.items():
        value = extract_css_value(content, pattern)
        if value:
            value = value.strip()
            expected = EXPECTED_VALUES.get(name)
            if expected and value != expected:
                issues.append({
                    'property': name,
                    'found': value,
                    'expected': expected
                })
            else:
                matches.append({
                    'property': name,
                    'value': value
                })

    # Check colors
    colors_found = re.findall(r'#[0-9a-fA-F]{6}', content)
    colors_set = set(c.lower() for c in colors_found)

    # Check for old purple colors (should not exist)
    forbidden = ['#667eea', '#764ba2']
    for color in forbidden:
        if color in colors_set:
            issues.append({
                'property': 'forbidden_color',
                'found': color,
                'expected': 'Not present (old purple)'
            })

    return issues, matches


def compare_layouts():
    """Compare all layout files."""
    layout_files = list(LAYOUTS_DIR.glob('*.html'))

    print("=" * 70)
    print("  LAYOUT CONSISTENCY VERIFICATION")
    print("=" * 70)

    all_values = {}
    all_issues = {}

    for layout_file in layout_files:
        issues, matches = check_layout_file(layout_file)
        all_issues[layout_file.name] = issues
        all_values[layout_file.name] = {m['property']: m['value'] for m in matches}

    # Print comparison table
    print("\n## CSS Value Comparison\n")

    properties_to_compare = [
        'sidebar_width',
        'container_max_width',
        'top_nav_padding',
        'top_nav_gap',
        'top_nav_font_size',
        'sidebar_header_padding',
        'sidebar_logo_width',
        'course_title_font_size',
        'part_section_summary_font_size',
        'part_section_link_font_size',
    ]

    # Header
    files = list(all_values.keys())
    print(f"{'Property':<35} | {'Expected':<12} | " + " | ".join(f"{f:<15}" for f in files))
    print("-" * (35 + 15 + 15 * len(files) + len(files) * 3))

    inconsistencies = 0

    for prop in properties_to_compare:
        expected = EXPECTED_VALUES.get(prop, 'N/A')
        row = f"{prop:<35} | {expected:<12} | "

        values = []
        for f in files:
            val = all_values.get(f, {}).get(prop, 'N/A')
            if val != expected and val != 'N/A':
                val = f"*{val}*"  # Mark inconsistent
                inconsistencies += 1
            values.append(f"{val:<15}")

        row += " | ".join(values)
        print(row)

    # Print issues
    print("\n" + "=" * 70)
    print("  ISSUES FOUND")
    print("=" * 70)

    total_issues = 0
    for filename, issues in all_issues.items():
        if issues:
            print(f"\n{filename}:")
            for issue in issues:
                print(f"  [MISMATCH] {issue['property']}: found '{issue['found']}', expected '{issue['expected']}'")
                total_issues += 1

    if total_issues == 0:
        print("\n  [PASS] All layouts are consistent!")
    else:
        print(f"\n  [FAIL] {total_issues} inconsistencies found")

    # Summary
    print("\n" + "=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    print(f"\n  Layout files checked: {len(layout_files)}")
    print(f"  Total inconsistencies: {total_issues}")

    return total_issues == 0


def main():
    """Main entry point."""
    print("\nScanning layout files in:", LAYOUTS_DIR)

    if not LAYOUTS_DIR.exists():
        print(f"ERROR: Layouts directory not found: {LAYOUTS_DIR}")
        return 1

    success = compare_layouts()
    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
