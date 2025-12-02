"""
Update all topic pages with new front matter for navigation.
"""
import re
from pathlib import Path

# Topic metadata: (filename, title, topic_num, part, part_name, prev, next)
TOPICS = [
    ("01-biological-neuron", "01. Biological vs Artificial Neuron", 1, 1, "Foundations", None, "02-single-neuron-computation"),
    ("02-single-neuron-computation", "02. Single Neuron Computation", 2, 1, "Foundations", "01-biological-neuron", "03-activation-functions"),
    ("03-activation-functions", "03. Activation Functions", 3, 2, "Building Blocks", "02-single-neuron-computation", "04-linear-limitation"),
    ("04-linear-limitation", "04. Linear Limitation", 4, 2, "Building Blocks", "03-activation-functions", "05-network-architecture"),
    ("05-network-architecture", "05. Network Architecture", 5, 3, "Architecture", "04-linear-limitation", "06-forward-propagation"),
    ("06-forward-propagation", "06. Forward Propagation", 6, 3, "Architecture", "05-network-architecture", "07-loss-landscape"),
    ("07-loss-landscape", "07. Loss Landscape", 7, 4, "Learning Process", "06-forward-propagation", "08-gradient-descent"),
    ("08-gradient-descent", "08. Gradient Descent", 8, 4, "Learning Process", "07-loss-landscape", "09-market-prediction-data"),
    ("09-market-prediction-data", "09. Market Prediction Data", 9, 5, "Application", "08-gradient-descent", "10-prediction-results"),
    ("10-prediction-results", "10. Prediction Results", 10, 5, "Application", "09-market-prediction-data", "11-problem-visualization"),
    ("11-problem-visualization", "11. Problem Visualization", 11, 1, "Foundations", "10-prediction-results", "12-decision-boundary-concept"),
    ("12-decision-boundary-concept", "12. Decision Boundary Concept", 12, 1, "Foundations", "11-problem-visualization", "13-neuron-decision-maker"),
    ("13-neuron-decision-maker", "13. Neuron Decision Maker", 13, 1, "Foundations", "12-decision-boundary-concept", "14-sigmoid-saturation"),
    ("14-sigmoid-saturation", "14. Sigmoid Saturation", 14, 2, "Building Blocks", "13-neuron-decision-maker", "15-boundary-evolution"),
    ("15-boundary-evolution", "15. Boundary Evolution", 15, 2, "Building Blocks", "14-sigmoid-saturation", "16-feature-hierarchy"),
    ("16-feature-hierarchy", "16. Feature Hierarchy", 16, 3, "Architecture", "15-boundary-evolution", "17-overfitting-underfitting"),
    ("17-overfitting-underfitting", "17. Overfitting vs Underfitting", 17, 4, "Learning Process", "16-feature-hierarchy", "18-learning-rate-comparison"),
    ("18-learning-rate-comparison", "18. Learning Rate Comparison", 18, 4, "Learning Process", "17-overfitting-underfitting", "19-confusion-matrix"),
    ("19-confusion-matrix", "19. Confusion Matrix", 19, 5, "Application", "18-learning-rate-comparison", "20-trading-backtest"),
    ("20-trading-backtest", "20. Trading Backtest", 20, 5, "Application", "19-confusion-matrix", None),
]

def update_topic(filename, title, topic_num, part, part_name, prev_topic, next_topic):
    """Update a single topic file with new front matter."""
    filepath = Path(f"docs/topics/{filename}.md")

    if not filepath.exists():
        print(f"  ERROR: {filepath} not found")
        return False

    content = filepath.read_text(encoding='utf-8')

    # Build new front matter
    front_matter = f'''---
layout: topic
title: "{title}"
topic_num: {topic_num}
part: {part}
part_name: "{part_name}"
'''
    if prev_topic:
        front_matter += f'prev_topic: "{prev_topic}"\n'
    if next_topic:
        front_matter += f'next_topic: "{next_topic}"\n'
    front_matter += '---\n'

    # Remove old front matter
    content = re.sub(r'^---\n.*?---\n', '', content, flags=re.DOTALL)

    # Remove old "[Back to Home]" link (we have breadcrumb now)
    content = re.sub(r'\[Back to Home\]\([^)]+\)\n*', '', content)

    # Remove old "Next Topic" section at the end
    content = re.sub(r'\*\*Next Topic:\*\*.*$', '', content, flags=re.DOTALL)

    # Clean up multiple newlines
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Write updated file
    new_content = front_matter + '\n' + content.strip() + '\n'
    filepath.write_text(new_content, encoding='utf-8')

    print(f"  Updated: {filename}")
    return True

def main():
    print("Updating topic pages with navigation front matter...\n")

    success = 0
    for topic in TOPICS:
        if update_topic(*topic):
            success += 1

    print(f"\nDone: {success}/{len(TOPICS)} files updated")

if __name__ == '__main__':
    main()
