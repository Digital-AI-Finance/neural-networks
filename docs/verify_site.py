"""
Neural Networks GitHub Pages Site Verification Script

Verifies:
1. All internal links exist
2. All 20 chart images present
3. Color consistency across HTML files
4. External URLs respond

Usage: python verify_site.py
"""

import os
import re
import sys
from pathlib import Path
from urllib.parse import urljoin
import urllib.request
import urllib.error

# Configuration
DOCS_DIR = Path(__file__).parent
EXPECTED_COLORS = {
    'primary_navy': '#1e3a5f',
    'primary_blue': '#2563eb',
    'light_blue': '#e0e7ff',
    'background': '#f8fafc',
    'border': '#e2e8f0',
}
FORBIDDEN_COLORS = ['#667eea', '#764ba2']  # Old purple colors

EXPECTED_IMAGES = [
    'biological_vs_artificial.png',
    'single_neuron_computation.png',
    'activation_functions.png',
    'linear_limitation.png',
    'network_architecture.png',
    'forward_propagation.png',
    'loss_landscape.png',
    'gradient_descent.png',
    'market_prediction_data.png',
    'prediction_results.png',
    'problem_visualization.png',
    'decision_boundary_concept.png',
    'neuron_decision_maker.png',
    'sigmoid_saturation.png',
    'boundary_evolution.png',
    'feature_hierarchy.png',
    'overfitting_underfitting.png',
    'learning_rate_comparison.png',
    'confusion_matrix.png',
    'trading_backtest.png',
    'quantlet-logo.png',
]

EXTERNAL_URLS = [
    'https://github.com/Digital-AI-Finance/neural-networks/raw/main/20251128_0825_quantlet_branding.pdf',
]


def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_result(check, passed, details=""):
    status = "[PASS]" if passed else "[FAIL]"
    print(f"  {status} {check}")
    if details:
        for line in details.split('\n'):
            print(f"         {line}")


def check_images():
    """Check all 20 chart images exist in assets/images/"""
    print_header("CHECK 1: Chart Images")

    images_dir = DOCS_DIR / 'assets' / 'images'
    missing = []
    found = []

    for img in EXPECTED_IMAGES:
        img_path = images_dir / img
        if img_path.exists():
            found.append(img)
        else:
            missing.append(img)

    print_result(
        f"Found {len(found)}/{len(EXPECTED_IMAGES)} images",
        len(missing) == 0,
        '\n'.join(f"Missing: {m}" for m in missing) if missing else ""
    )

    return len(missing) == 0


def check_internal_links():
    """Check all internal links in HTML files exist"""
    print_header("CHECK 2: Internal Links")

    # Only check layout files and topic files, skip includes (they use relative paths)
    html_files = list((DOCS_DIR / '_layouts').glob('*.html'))
    html_files += list((DOCS_DIR / 'topics').glob('*.md'))

    broken_links = []
    total_links = 0

    # Pattern to match href and src attributes
    link_pattern = re.compile(r'(?:href|src)=["\']([^"\']+)["\']')

    for html_file in html_files:
        try:
            content = html_file.read_text(encoding='utf-8')
        except:
            continue

        links = link_pattern.findall(content)

        for link in links:
            # Skip external links, anchors, and Jekyll variables
            if link.startswith(('http://', 'https://', '#', '{{', 'mailto:', 'javascript:')):
                continue

            # Skip CDN links
            if 'cdnjs.cloudflare.com' in link or 'cdn.jsdelivr.net' in link:
                continue

            # Skip relative .html links in layouts (they're resolved by Jekyll)
            if html_file.parent.name == '_layouts' and link.endswith('.html') and not link.startswith('/'):
                continue

            total_links += 1

            # Resolve the link relative to the HTML file
            if link.startswith('/'):
                # Absolute path from docs root
                target = DOCS_DIR / link.lstrip('/')
            else:
                # Relative path
                target = html_file.parent / link

            # Remove query strings and fragments
            target_str = str(target).split('?')[0].split('#')[0]
            target = Path(target_str)

            # Check if file exists (also check .html extension)
            if not target.exists():
                if not target.with_suffix('.html').exists():
                    broken_links.append(f"{html_file.name}: {link}")

    print_result(
        f"Checked {total_links} internal links",
        len(broken_links) == 0,
        '\n'.join(broken_links[:10]) + (f'\n... and {len(broken_links)-10} more' if len(broken_links) > 10 else '') if broken_links else ""
    )

    return len(broken_links) == 0


def check_color_consistency():
    """Check CSS colors are consistent across all HTML files"""
    print_header("CHECK 3: Color Consistency")

    html_files = list((DOCS_DIR / '_layouts').glob('*.html'))
    color_pattern = re.compile(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}')

    issues = []
    all_colors = {}

    for html_file in html_files:
        try:
            content = html_file.read_text(encoding='utf-8')
        except:
            continue

        colors = color_pattern.findall(content)
        all_colors[html_file.name] = set(c.lower() for c in colors)

        # Check for forbidden colors
        for color in colors:
            if color.lower() in [c.lower() for c in FORBIDDEN_COLORS]:
                issues.append(f"{html_file.name}: Found old purple color {color}")

    # Check expected colors are present
    for html_file in html_files:
        if html_file.name in all_colors:
            file_colors = all_colors[html_file.name]
            if EXPECTED_COLORS['primary_navy'] not in file_colors:
                issues.append(f"{html_file.name}: Missing primary navy {EXPECTED_COLORS['primary_navy']}")
            if EXPECTED_COLORS['primary_blue'] not in file_colors:
                issues.append(f"{html_file.name}: Missing primary blue {EXPECTED_COLORS['primary_blue']}")

    print_result(
        f"Checked {len(html_files)} layout files",
        len(issues) == 0,
        '\n'.join(issues) if issues else "All colors consistent (Blue Professional theme)"
    )

    # Print color summary
    print(f"\n  Color palette used:")
    print(f"    Primary Navy: {EXPECTED_COLORS['primary_navy']}")
    print(f"    Primary Blue: {EXPECTED_COLORS['primary_blue']}")
    print(f"    Light Blue:   {EXPECTED_COLORS['light_blue']}")
    print(f"    Background:   {EXPECTED_COLORS['background']}")
    print(f"    Border:       {EXPECTED_COLORS['border']}")

    return len(issues) == 0


def check_external_urls():
    """Check external URLs respond"""
    print_header("CHECK 4: External URLs")

    issues = []

    for url in EXTERNAL_URLS:
        try:
            req = urllib.request.Request(url, method='HEAD')
            req.add_header('User-Agent', 'Mozilla/5.0')
            response = urllib.request.urlopen(req, timeout=10)
            status = response.getcode()
            if status >= 400:
                issues.append(f"HTTP {status}: {url}")
            else:
                print_result(f"URL responds ({status})", True, url[:60])
        except urllib.error.HTTPError as e:
            issues.append(f"HTTP {e.code}: {url}")
        except urllib.error.URLError as e:
            issues.append(f"Connection error: {url} - {e.reason}")
        except Exception as e:
            issues.append(f"Error: {url} - {str(e)}")

    if issues:
        for issue in issues:
            print_result("URL check failed", False, issue)

    return len(issues) == 0


def check_topic_files():
    """Check all 20 topic markdown files exist"""
    print_header("CHECK 5: Topic Files")

    topics_dir = DOCS_DIR / 'topics'
    expected_topics = [
        '01-biological-neuron.md',
        '02-single-neuron-computation.md',
        '03-activation-functions.md',
        '04-linear-limitation.md',
        '05-network-architecture.md',
        '06-forward-propagation.md',
        '07-loss-landscape.md',
        '08-gradient-descent.md',
        '09-market-prediction-data.md',
        '10-prediction-results.md',
        '11-problem-visualization.md',
        '12-decision-boundary-concept.md',
        '13-neuron-decision-maker.md',
        '14-sigmoid-saturation.md',
        '15-boundary-evolution.md',
        '16-feature-hierarchy.md',
        '17-overfitting-underfitting.md',
        '18-learning-rate-comparison.md',
        '19-confusion-matrix.md',
        '20-trading-backtest.md',
    ]

    missing = []
    for topic in expected_topics:
        if not (topics_dir / topic).exists():
            missing.append(topic)

    print_result(
        f"Found {len(expected_topics) - len(missing)}/{len(expected_topics)} topic files",
        len(missing) == 0,
        '\n'.join(f"Missing: {m}" for m in missing) if missing else ""
    )

    return len(missing) == 0


def check_layout_structure():
    """Check required layout elements exist"""
    print_header("CHECK 6: Layout Structure")

    issues = []

    # Check home.html has required sections
    home_html = DOCS_DIR / '_layouts' / 'home.html'
    if home_html.exists():
        content = home_html.read_text(encoding='utf-8')

        required_elements = [
            ('top-nav', 'Top navigation bar'),
            ('sidebar', 'Left sidebar'),
            ('hero', 'Hero section'),
            ('topic-grid', 'Topic grid'),
            ('chart-gallery', 'Chart gallery'),
            ('gallery-grid', 'Gallery grid'),
        ]

        for element, name in required_elements:
            if element not in content:
                issues.append(f"home.html: Missing {name} ({element})")

        # Count chart images in gallery
        chart_count = content.count('gallery-item')
        if chart_count < 20:
            issues.append(f"home.html: Only {chart_count} charts in gallery (expected 20)")
    else:
        issues.append("home.html: File not found")

    # Check topic.html has required sections
    topic_html = DOCS_DIR / '_layouts' / 'topic.html'
    if topic_html.exists():
        content = topic_html.read_text(encoding='utf-8')

        required_elements = [
            ('sidebar', 'Left sidebar'),
            ('sidebar-header', 'Sidebar header with logo'),
            ('search-container', 'Search box'),
            ('progress-container', 'Progress indicator'),
            ('breadcrumb', 'Breadcrumb navigation'),
            ('topic-nav', 'Prev/Next navigation'),
        ]

        for element, name in required_elements:
            if element not in content:
                issues.append(f"topic.html: Missing {name} ({element})")
    else:
        issues.append("topic.html: File not found")

    print_result(
        f"Layout structure check",
        len(issues) == 0,
        '\n'.join(issues) if issues else "All required elements present"
    )

    return len(issues) == 0


def main():
    print("\n" + "="*60)
    print("  NEURAL NETWORKS SITE VERIFICATION")
    print("  " + str(DOCS_DIR))
    print("="*60)

    results = []

    results.append(("Images", check_images()))
    results.append(("Internal Links", check_internal_links()))
    results.append(("Color Consistency", check_color_consistency()))
    results.append(("External URLs", check_external_urls()))
    results.append(("Topic Files", check_topic_files()))
    results.append(("Layout Structure", check_layout_structure()))

    # Summary
    print_header("SUMMARY")

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status} {name}")

    print(f"\n  Total: {passed}/{total} checks passed")

    if passed == total:
        print("\n  All checks passed!")
        return 0
    else:
        print(f"\n  {total - passed} check(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
