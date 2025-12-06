"""
Fix Topic MD Files

Renames topic markdown files to match new numbering and updates frontmatter.
"""

import re
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
TOPICS_DIR = PROJECT_ROOT / 'docs' / 'topics'

# Mapping: old slug -> (new number, new slug base)
SLUG_MAPPING = {
    '01-biological-neuron': ('01', 'biological-neuron'),
    '02-single-neuron-computation': ('02', 'single-neuron-computation'),
    '11-problem-visualization': ('03', 'problem-visualization'),
    '13-neuron-decision-maker': ('04', 'neuron-decision-maker'),
    '03-activation-functions': ('05', 'activation-functions'),
    '04-linear-limitation': ('06', 'linear-limitation'),
    '14-sigmoid-saturation': ('07', 'sigmoid-saturation'),
    '15-boundary-evolution': ('08', 'boundary-evolution'),
    '05-network-architecture': ('09', 'network-architecture'),
    '06-forward-propagation': ('10', 'forward-propagation'),
    '12-decision-boundary-concept': ('11', 'decision-boundary-concept'),
    '16-feature-hierarchy': ('12', 'feature-hierarchy'),
    '07-loss-landscape': ('13', 'loss-landscape'),
    '08-gradient-descent': ('14', 'gradient-descent'),
    '17-overfitting-underfitting': ('15', 'overfitting-underfitting'),
    '18-learning-rate-comparison': ('16', 'learning-rate-comparison'),
    '09-market-prediction-data': ('17', 'market-prediction-data'),
    '10-prediction-results': ('18', 'prediction-results'),
    '19-confusion-matrix': ('19', 'confusion-matrix'),
    '20-trading-backtest': ('20', 'trading-backtest'),
}


def update_frontmatter(content, old_num, new_num):
    """Update topic_num and other references in frontmatter."""
    # Update topic_num
    content = re.sub(
        rf'topic_num:\s*{int(old_num)}',
        f'topic_num: {int(new_num)}',
        content
    )
    return content


def update_navigation_links(content, old_num, new_num):
    """Update prev_topic and next_topic links."""
    # This is complex because we need to update the navigation chain
    # For now, we'll regenerate navigation separately
    return content


def main():
    print("\n=== Fixing Topic MD Files ===\n")

    if not TOPICS_DIR.exists():
        print(f"  [ERROR] Topics directory not found: {TOPICS_DIR}")
        return

    # First pass: rename to temp
    temp_mapping = {}
    for old_slug, (new_num, slug_base) in SLUG_MAPPING.items():
        old_file = TOPICS_DIR / f"{old_slug}.md"
        if old_file.exists():
            old_num = old_slug.split('-')[0]
            temp_file = TOPICS_DIR / f"temp_{old_slug}.md"
            print(f"  {old_slug}.md -> temp_{old_slug}.md")
            shutil.move(str(old_file), str(temp_file))
            temp_mapping[temp_file] = (new_num, slug_base, old_num)

    print()

    # Second pass: rename to final and update content
    for temp_file, (new_num, slug_base, old_num) in temp_mapping.items():
        new_slug = f"{new_num}-{slug_base}"
        new_file = TOPICS_DIR / f"{new_slug}.md"

        # Read and update content
        content = temp_file.read_text(encoding='utf-8')
        content = update_frontmatter(content, old_num, new_num)

        # Write to new file
        new_file.write_text(content, encoding='utf-8')
        temp_file.unlink()  # Remove temp file

        print(f"  temp_{temp_file.name.replace('temp_', '')} -> {new_slug}.md")

    print(f"\n  [DONE] Processed {len(temp_mapping)} topic files")

    # Now update navigation links in all files
    print("\n=== Updating Navigation Links ===\n")
    update_all_navigation()


def update_all_navigation():
    """Update prev_topic and next_topic in all topic files."""
    # New sequential order
    topic_order = [
        '01-biological-neuron',
        '02-single-neuron-computation',
        '03-problem-visualization',
        '04-neuron-decision-maker',
        '05-activation-functions',
        '06-linear-limitation',
        '07-sigmoid-saturation',
        '08-boundary-evolution',
        '09-network-architecture',
        '10-forward-propagation',
        '11-decision-boundary-concept',
        '12-feature-hierarchy',
        '13-loss-landscape',
        '14-gradient-descent',
        '15-overfitting-underfitting',
        '16-learning-rate-comparison',
        '17-market-prediction-data',
        '18-prediction-results',
        '19-confusion-matrix',
        '20-trading-backtest',
    ]

    for i, slug in enumerate(topic_order):
        filepath = TOPICS_DIR / f"{slug}.md"
        if not filepath.exists():
            print(f"  [SKIP] {slug}.md not found")
            continue

        content = filepath.read_text(encoding='utf-8')

        # Update prev_topic
        if i == 0:
            # First topic - no prev
            content = re.sub(r'prev_topic:.*\n', 'prev_topic: null\n', content)
        else:
            prev_slug = topic_order[i - 1]
            content = re.sub(r'prev_topic:.*\n', f'prev_topic: {prev_slug}\n', content)

        # Update next_topic
        if i == len(topic_order) - 1:
            # Last topic - no next
            content = re.sub(r'next_topic:.*\n', 'next_topic: null\n', content)
        else:
            next_slug = topic_order[i + 1]
            content = re.sub(r'next_topic:.*\n', f'next_topic: {next_slug}\n', content)

        filepath.write_text(content, encoding='utf-8')
        print(f"  Updated navigation: {slug}.md")

    print("\n  [DONE] Navigation links updated")


if __name__ == '__main__':
    main()
