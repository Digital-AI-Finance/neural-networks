"""
Fix Topic Titles and Numbers

Ensures all topic MD files have correct titles matching their topic number.
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
TOPICS_DIR = PROJECT_ROOT / 'docs' / 'topics'

# Correct topic information
TOPICS = {
    '01': {'name': 'Biological Neuron', 'part': 1, 'part_name': 'Foundations'},
    '02': {'name': 'Single Neuron Computation', 'part': 1, 'part_name': 'Foundations'},
    '03': {'name': 'Problem Visualization', 'part': 1, 'part_name': 'Foundations'},
    '04': {'name': 'Neuron Decision Maker', 'part': 1, 'part_name': 'Foundations'},
    '05': {'name': 'Activation Functions', 'part': 2, 'part_name': 'Building Blocks'},
    '06': {'name': 'Linear Limitation', 'part': 2, 'part_name': 'Building Blocks'},
    '07': {'name': 'Sigmoid Saturation', 'part': 2, 'part_name': 'Building Blocks'},
    '08': {'name': 'Boundary Evolution', 'part': 2, 'part_name': 'Building Blocks'},
    '09': {'name': 'Network Architecture', 'part': 3, 'part_name': 'Architecture'},
    '10': {'name': 'Forward Propagation', 'part': 3, 'part_name': 'Architecture'},
    '11': {'name': 'Decision Boundary Concept', 'part': 3, 'part_name': 'Architecture'},
    '12': {'name': 'Feature Hierarchy', 'part': 3, 'part_name': 'Architecture'},
    '13': {'name': 'Loss Landscape', 'part': 4, 'part_name': 'Learning Process'},
    '14': {'name': 'Gradient Descent', 'part': 4, 'part_name': 'Learning Process'},
    '15': {'name': 'Overfitting and Underfitting', 'part': 4, 'part_name': 'Learning Process'},
    '16': {'name': 'Learning Rate Comparison', 'part': 4, 'part_name': 'Learning Process'},
    '17': {'name': 'Market Prediction Data', 'part': 5, 'part_name': 'Application'},
    '18': {'name': 'Prediction Results', 'part': 5, 'part_name': 'Application'},
    '19': {'name': 'Confusion Matrix', 'part': 5, 'part_name': 'Application'},
    '20': {'name': 'Trading Backtest', 'part': 5, 'part_name': 'Application'},
}


def fix_topic_file(filepath, topic_num, topic_info):
    """Fix the frontmatter of a topic file."""
    content = filepath.read_text(encoding='utf-8')

    # Calculate prev/next topics
    num = int(topic_num)
    prev_topic = None
    next_topic = None

    if num > 1:
        prev_num = f'{num-1:02d}'
        prev_info = TOPICS.get(prev_num)
        if prev_info:
            prev_name = prev_info['name'].lower().replace(' ', '-')
            prev_topic = f'{prev_num}-{prev_name}'

    if num < 20:
        next_num = f'{num+1:02d}'
        next_info = TOPICS.get(next_num)
        if next_info:
            next_name = next_info['name'].lower().replace(' ', '-')
            next_topic = f'{next_num}-{next_name}'

    # Build new frontmatter
    new_frontmatter = f'''---
layout: topic
title: "{topic_num}. {topic_info['name']}"
topic_num: {int(topic_num)}
part: {topic_info['part']}
part_name: "{topic_info['part_name']}"'''

    if prev_topic:
        new_frontmatter += f'\nprev_topic: {prev_topic}'
    if next_topic:
        new_frontmatter += f'\nnext_topic: {next_topic}'

    new_frontmatter += '\n---'

    # Replace old frontmatter
    content = re.sub(r'^---\n.*?\n---', new_frontmatter, content, flags=re.DOTALL)

    filepath.write_text(content, encoding='utf-8')
    return True


def main():
    print("=" * 60)
    print("  FIXING TOPIC TITLES AND NUMBERS")
    print("=" * 60)

    fixed = 0

    for topic_num, topic_info in TOPICS.items():
        # Find the matching file
        pattern = f'{topic_num}-*.md'
        matches = list(TOPICS_DIR.glob(pattern))

        if matches:
            filepath = matches[0]
            print(f"\n  Fixing {filepath.name}...")
            print(f"    Title: {topic_num}. {topic_info['name']}")
            print(f"    Part: {topic_info['part']} ({topic_info['part_name']})")

            if fix_topic_file(filepath, topic_num, topic_info):
                fixed += 1
                print(f"    [OK] Fixed")
        else:
            print(f"\n  [WARN] No file found for topic {topic_num}")

    print("\n" + "=" * 60)
    print(f"  COMPLETE: {fixed}/20 files fixed")
    print("=" * 60)


if __name__ == '__main__':
    main()
