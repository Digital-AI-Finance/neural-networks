"""
Topic Renumbering Script

Renumbers topics 01-20 sequentially by part:
- Part 1 (Foundations): 01-04
- Part 2 (Building Blocks): 05-08
- Part 3 (Architecture): 09-12
- Part 4 (Learning): 13-16
- Part 5 (Application): 17-20

Usage: python renumber_topics.py
"""

import os
import re
import shutil
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent
DOCS_DIR = PROJECT_ROOT / 'docs'
GITHUB_BASE = 'https://github.com/Digital-AI-Finance/neural-networks/tree/main/'

# Mapping: current number -> (new number, folder suffix, display name)
TOPIC_MAPPING = {
    # Part 1: Foundations (01-04)
    '01': ('01', 'biological_neuron', 'Biological Neuron'),
    '02': ('02', 'single_neuron_function', 'Single Neuron'),
    '11': ('03', 'problem_visualization', 'Problem Visualization'),
    '13': ('04', 'neuron_decision_maker', 'Neuron Decision Maker'),
    # Part 2: Building Blocks (05-08)
    '03': ('05', 'activation_functions', 'Activation Functions'),
    '04': ('06', 'linear_limitation', 'Linear Limitation'),
    '14': ('07', 'sigmoid_saturation', 'Sigmoid Saturation'),
    '15': ('08', 'boundary_evolution', 'Boundary Evolution'),
    # Part 3: Architecture (09-12)
    '05': ('09', 'network_architecture', 'Network Architecture'),
    '06': ('10', 'forward_propagation', 'Forward Propagation'),
    '12': ('11', 'decision_boundary_concept', 'Decision Boundary'),
    '16': ('12', 'feature_hierarchy', 'Feature Hierarchy'),
    # Part 4: Learning (13-16)
    '07': ('13', 'loss_landscape', 'Loss Landscape'),
    '08': ('14', 'gradient_descent', 'Gradient Descent'),
    '17': ('15', 'overfitting_underfitting', 'Overfitting/Underfitting'),
    '18': ('16', 'learning_rate_comparison', 'Learning Rate'),
    # Part 5: Application (17-20)
    '09': ('17', 'market_prediction_data', 'Market Prediction Data'),
    '10': ('18', 'prediction_results', 'Prediction Results'),
    '19': ('19', 'confusion_matrix', 'Confusion Matrix'),
    '20': ('20', 'trading_backtest', 'Trading Backtest'),
}


def get_current_folders():
    """Get all numbered chart folders."""
    folders = []
    for item in PROJECT_ROOT.iterdir():
        if item.is_dir() and re.match(r'^\d{2}_', item.name):
            folders.append(item)
    return sorted(folders)


def rename_folders():
    """Rename folders from old to new numbering."""
    print("\n=== Phase 1: Renaming Folders ===\n")

    # First pass: rename to temp names to avoid conflicts
    temp_mapping = {}
    for old_num, (new_num, suffix, _) in TOPIC_MAPPING.items():
        old_folder = PROJECT_ROOT / f"{old_num}_{suffix}"
        if old_folder.exists():
            temp_folder = PROJECT_ROOT / f"temp_{old_num}_{suffix}"
            print(f"  {old_folder.name} -> temp_{old_num}_{suffix}")
            shutil.move(str(old_folder), str(temp_folder))
            temp_mapping[temp_folder] = (new_num, suffix)

    # Second pass: rename to final names
    print()
    for temp_folder, (new_num, suffix) in temp_mapping.items():
        new_folder = PROJECT_ROOT / f"{new_num}_{suffix}"
        print(f"  {temp_folder.name} -> {new_folder.name}")
        shutil.move(str(temp_folder), str(new_folder))

    print(f"\n  [DONE] Renamed {len(temp_mapping)} folders")


def update_chart_metadata():
    """Update CHART_METADATA URLs in all Python scripts."""
    print("\n=== Phase 2: Updating CHART_METADATA ===\n")

    updated = 0
    for old_num, (new_num, suffix, _) in TOPIC_MAPPING.items():
        folder = PROJECT_ROOT / f"{new_num}_{suffix}"
        if not folder.exists():
            print(f"  [SKIP] {folder.name} not found")
            continue

        # Find Python script in folder
        py_files = list(folder.glob('*.py'))
        for py_file in py_files:
            content = py_file.read_text(encoding='utf-8')

            # Update URL in CHART_METADATA
            old_url = f"{old_num}_{suffix}/"
            new_url = f"{new_num}_{suffix}/"

            if old_url in content:
                new_content = content.replace(old_url, new_url)
                py_file.write_text(new_content, encoding='utf-8')
                print(f"  Updated: {py_file.name}")
                updated += 1

    print(f"\n  [DONE] Updated {updated} Python scripts")


def update_latex_files():
    """Update all references in LaTeX .tex files."""
    print("\n=== Phase 3: Updating LaTeX Files ===\n")

    tex_files = list(PROJECT_ROOT.glob('*.tex'))
    updated = 0

    for tex_file in tex_files:
        content = tex_file.read_text(encoding='utf-8')
        original = content

        for old_num, (new_num, suffix, _) in TOPIC_MAPPING.items():
            # Update includegraphics paths
            old_pattern = f"{old_num}_{suffix}/"
            new_pattern = f"{new_num}_{suffix}/"
            content = content.replace(old_pattern, new_pattern)

        if content != original:
            tex_file.write_text(content, encoding='utf-8')
            print(f"  Updated: {tex_file.name}")
            updated += 1

    print(f"\n  [DONE] Updated {updated} LaTeX files")


def update_website_files():
    """Update all website HTML and MD files."""
    print("\n=== Phase 4: Updating Website Files ===\n")

    files_to_update = [
        DOCS_DIR / '_layouts' / 'home.html',
        DOCS_DIR / '_layouts' / 'page.html',
        DOCS_DIR / '_layouts' / 'topic.html',
        DOCS_DIR / '_includes' / 'sidebar.html',
        DOCS_DIR / 'index.html' if (DOCS_DIR / 'index.html').exists() else None,
    ]

    # Add all topic HTML files
    topics_dir = DOCS_DIR / 'topics'
    if topics_dir.exists():
        files_to_update.extend(topics_dir.glob('*.html'))

    # Add markdown files
    files_to_update.extend(DOCS_DIR.glob('*.md'))

    updated = 0
    for filepath in files_to_update:
        if filepath is None or not filepath.exists():
            continue

        content = filepath.read_text(encoding='utf-8')
        original = content

        for old_num, (new_num, suffix, name) in TOPIC_MAPPING.items():
            # Update folder references in paths
            old_folder = f"{old_num}_{suffix}"
            new_folder = f"{new_num}_{suffix}"
            content = content.replace(old_folder, new_folder)

            # Update topic number displays (e.g., "01." to keep as is if same)
            # Update HTML topic links like 01-biological-neuron.html
            old_slug = f"{old_num}-{suffix.replace('_', '-')}"
            new_slug = f"{new_num}-{suffix.replace('_', '-')}"
            content = content.replace(old_slug, new_slug)

            # Update topic_num in frontmatter
            if f'topic_num: {int(old_num)}' in content:
                content = content.replace(
                    f'topic_num: {int(old_num)}',
                    f'topic_num: {int(new_num)}'
                )

        if content != original:
            filepath.write_text(content, encoding='utf-8')
            print(f"  Updated: {filepath.name}")
            updated += 1

    print(f"\n  [DONE] Updated {updated} website files")


def rename_topic_html_files():
    """Rename topic HTML files to match new numbering."""
    print("\n=== Phase 5: Renaming Topic HTML Files ===\n")

    topics_dir = DOCS_DIR / 'topics'
    if not topics_dir.exists():
        print("  [SKIP] topics directory not found")
        return

    # First pass: rename to temp
    temp_mapping = {}
    for old_num, (new_num, suffix, _) in TOPIC_MAPPING.items():
        old_slug = f"{old_num}-{suffix.replace('_', '-')}.html"
        old_file = topics_dir / old_slug
        if old_file.exists():
            temp_file = topics_dir / f"temp_{old_slug}"
            shutil.move(str(old_file), str(temp_file))
            temp_mapping[temp_file] = (new_num, suffix)

    # Second pass: rename to final
    for temp_file, (new_num, suffix) in temp_mapping.items():
        new_slug = f"{new_num}-{suffix.replace('_', '-')}.html"
        new_file = topics_dir / new_slug
        shutil.move(str(temp_file), str(new_file))
        print(f"  Renamed: {temp_file.name.replace('temp_', '')} -> {new_slug}")

    print(f"\n  [DONE] Renamed {len(temp_mapping)} topic files")


def update_image_references():
    """Update image references to use new numbering."""
    print("\n=== Phase 6: Updating Image References ===\n")

    # Check assets/images for PNG files
    images_dir = DOCS_DIR / 'assets' / 'images'
    if not images_dir.exists():
        print("  [SKIP] images directory not found")
        return

    # No renaming needed for images as they use content-based names (e.g., biological_vs_artificial.png)
    # Just verify they exist
    image_count = len(list(images_dir.glob('*.png')))
    print(f"  Found {image_count} images in assets/images/")
    print("  [INFO] Images use content-based names, no renaming needed")


def print_summary():
    """Print summary of changes."""
    print("\n" + "=" * 70)
    print("  RENUMBERING COMPLETE")
    print("=" * 70)
    print("\n  New Topic Organization:\n")

    parts = {
        'Part 1: Foundations': ['01', '02', '03', '04'],
        'Part 2: Building Blocks': ['05', '06', '07', '08'],
        'Part 3: Architecture': ['09', '10', '11', '12'],
        'Part 4: Learning': ['13', '14', '15', '16'],
        'Part 5: Application': ['17', '18', '19', '20'],
    }

    # Invert mapping for display
    new_to_info = {}
    for old_num, (new_num, suffix, name) in TOPIC_MAPPING.items():
        new_to_info[new_num] = (suffix, name)

    for part_name, topic_nums in parts.items():
        print(f"  {part_name}")
        for num in topic_nums:
            if num in new_to_info:
                suffix, name = new_to_info[num]
                print(f"    {num}. {name}")
        print()


def main():
    """Main execution."""
    print("\n" + "=" * 70)
    print("  TOPIC RENUMBERING SCRIPT")
    print("=" * 70)
    print("\n  This will renumber all topics 01-20 sequentially by part.")
    print("  Current folders will be renamed and all references updated.\n")

    # Execute phases
    rename_folders()
    update_chart_metadata()
    update_latex_files()
    update_website_files()
    rename_topic_html_files()
    update_image_references()
    print_summary()

    print("\n  Next steps:")
    print("  1. Run: python generate_qr_codes.py (to regenerate QR codes)")
    print("  2. Regenerate all charts with updated URLs")
    print("  3. Recompile LaTeX presentation")
    print("  4. Verify website locally")
    print()


if __name__ == '__main__':
    main()
