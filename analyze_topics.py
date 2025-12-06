"""
Pedagogical Completeness Analysis for Neural Networks Course
Analyzes all 20 topics for learning structure and content quality
"""

import re
from pathlib import Path
from collections import defaultdict

def analyze_topic_file(filepath):
    """Extract key pedagogical elements from a topic file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title_match = re.search(r'\\title\{(.*?)\}', content)
    title = title_match.group(1) if title_match else "Unknown"

    # Count slides by frame type
    frames = {
        'learning_goal': bool(re.search(r'\\begin\{frame\}\{Learning Goal\}', content)),
        'key_concept': len(re.findall(r'\\begin\{frame\}\{Key Concept', content)),
        'visualization': bool(re.search(r'\\includegraphics.*\.pdf', content)),
        'key_formula': bool(re.search(r'\\begin\{frame\}\{Key Formula\}', content)),
        'intuitive_explanation': bool(re.search(r'\\begin\{frame\}\{Intuitive Explanation\}', content)),
        'practice_problems': len(re.findall(r'\\begin\{frame\}\{Practice Problem', content)),
        'key_takeaways': bool(re.search(r'\\begin\{frame\}\{Key Takeaways\}', content)),
    }

    # Check for solutions to practice problems
    solutions_count = len(re.findall(r'\\begin\{block\}\{Solution\}', content))

    # Count total frames
    total_frames = len(re.findall(r'\\begin\{frame\}', content))

    # Extract learning goal text
    learning_goal_match = re.search(
        r'\\begin\{frame\}\{Learning Goal\}(.*?)\\end\{frame\}',
        content,
        re.DOTALL
    )
    learning_goal = learning_goal_match.group(1).strip() if learning_goal_match else ""

    # Extract key takeaways
    takeaways_match = re.search(
        r'\\begin\{frame\}\{Key Takeaways\}(.*?)\\end\{frame\}',
        content,
        re.DOTALL
    )
    takeaways_count = len(re.findall(r'\\item', takeaways_match.group(1))) if takeaways_match else 0

    return {
        'title': title,
        'frames': frames,
        'total_frames': total_frames,
        'solutions_count': solutions_count,
        'learning_goal': learning_goal,
        'takeaways_count': takeaways_count,
        'filepath': filepath
    }

def check_pedagogical_standards(analysis):
    """Check if topic meets pedagogical standards"""
    issues = []
    warnings = []

    frames = analysis['frames']

    # Critical checks
    if not frames['learning_goal']:
        issues.append("Missing Learning Goal")
    if not frames['key_takeaways']:
        issues.append("Missing Key Takeaways")
    if frames['practice_problems'] == 0:
        warnings.append("No practice problems")
    if frames['practice_problems'] != analysis['solutions_count']:
        issues.append(f"{frames['practice_problems']} problems but {analysis['solutions_count']} solutions")

    # Quality checks
    if not frames['visualization']:
        warnings.append("No visualization included")
    if not frames['key_formula']:
        warnings.append("No key formula slide")
    if not frames['intuitive_explanation']:
        warnings.append("No intuitive explanation")
    if frames['key_concept'] < 1:
        warnings.append("No key concept slides")
    if analysis['takeaways_count'] < 3:
        warnings.append(f"Only {analysis['takeaways_count']} takeaways (recommend 4-6)")

    return issues, warnings

def analyze_learning_progression(all_analyses):
    """Analyze how topics build on each other"""
    progression = []

    for i, analysis in enumerate(all_analyses):
        topic_num = i + 1
        title = analysis['title']

        # Extract topic number and name
        if '. ' in title:
            parts = title.split('. ', 1)
            topic_name = parts[1] if len(parts) > 1 else title
        else:
            topic_name = title

        progression.append({
            'number': topic_num,
            'name': topic_name,
            'complexity': analysis['total_frames'],
            'has_math': analysis['frames']['key_formula'],
            'practice_count': analysis['frames']['practice_problems']
        })

    return progression

def generate_report(all_analyses):
    """Generate comprehensive pedagogical analysis report"""
    report = []
    report.append("=" * 80)
    report.append("PEDAGOGICAL COMPLETENESS ANALYSIS - NEURAL NETWORKS COURSE")
    report.append("=" * 80)
    report.append("")

    # Overall statistics
    total_topics = len(all_analyses)
    total_frames = sum(a['total_frames'] for a in all_analyses)
    total_problems = sum(a['frames']['practice_problems'] for a in all_analyses)

    report.append(f"Total Topics: {total_topics}")
    report.append(f"Total Slides: {total_frames}")
    report.append(f"Total Practice Problems: {total_problems}")
    report.append(f"Average Slides per Topic: {total_frames / total_topics:.1f}")
    report.append("")

    # Individual topic analysis
    report.append("=" * 80)
    report.append("INDIVIDUAL TOPIC ANALYSIS")
    report.append("=" * 80)
    report.append("")

    total_issues = 0
    total_warnings = 0

    for i, analysis in enumerate(all_analyses):
        topic_num = i + 1
        issues, warnings = check_pedagogical_standards(analysis)

        status = "PASS"
        if issues:
            status = "CRITICAL"
            total_issues += len(issues)
        elif warnings:
            status = "WARNING"
            total_warnings += len(warnings)

        report.append(f"Topic {topic_num:02d}: {analysis['title']}")
        report.append(f"  Status: {status}")
        report.append(f"  Total Slides: {analysis['total_frames']}")
        report.append(f"  Practice Problems: {analysis['frames']['practice_problems']}")
        report.append(f"  Takeaways: {analysis['takeaways_count']}")

        if issues:
            report.append("  ISSUES:")
            for issue in issues:
                report.append(f"    - {issue}")

        if warnings:
            report.append("  WARNINGS:")
            for warning in warnings:
                report.append(f"    - {warning}")

        report.append("")

    # Learning progression analysis
    report.append("=" * 80)
    report.append("LEARNING PROGRESSION ANALYSIS")
    report.append("=" * 80)
    report.append("")

    progression = analyze_learning_progression(all_analyses)

    # Group topics by conceptual areas
    foundations = progression[0:4]    # Topics 1-4: Neuron basics
    architecture = progression[4:8]   # Topics 5-8: Network structure and training
    application = progression[8:12]   # Topics 9-12: Market prediction application
    deep_dive = progression[12:16]    # Topics 13-16: Advanced concepts
    evaluation = progression[16:20]   # Topics 17-20: Model evaluation

    def report_section(section_name, topics):
        report.append(f"{section_name}:")
        for t in topics:
            report.append(f"  {t['number']:02d}. {t['name']} ({t['complexity']} slides, {t['practice_count']} problems)")
        report.append("")

    report_section("PART 1: FOUNDATIONS (Topics 1-4)", foundations)
    report_section("PART 2: ARCHITECTURE & TRAINING (Topics 5-8)", architecture)
    report_section("PART 3: APPLICATION - MARKET PREDICTION (Topics 9-12)", application)
    report_section("PART 4: DEEP DIVE - ADVANCED CONCEPTS (Topics 13-16)", deep_dive)
    report_section("PART 5: EVALUATION & DEPLOYMENT (Topics 17-20)", evaluation)

    # Content quality assessment
    report.append("=" * 80)
    report.append("CONTENT QUALITY ASSESSMENT")
    report.append("=" * 80)
    report.append("")

    quality_metrics = {
        'learning_objectives': sum(1 for a in all_analyses if a['frames']['learning_goal']),
        'visualizations': sum(1 for a in all_analyses if a['frames']['visualization']),
        'formulas': sum(1 for a in all_analyses if a['frames']['key_formula']),
        'intuitive_explanations': sum(1 for a in all_analyses if a['frames']['intuitive_explanation']),
        'practice_problems': sum(a['frames']['practice_problems'] for a in all_analyses),
        'key_takeaways': sum(1 for a in all_analyses if a['frames']['key_takeaways']),
    }

    report.append("Content Element Coverage:")
    report.append(f"  Learning Objectives: {quality_metrics['learning_objectives']}/{total_topics} topics ({quality_metrics['learning_objectives']/total_topics*100:.0f}%)")
    report.append(f"  Visualizations: {quality_metrics['visualizations']}/{total_topics} topics ({quality_metrics['visualizations']/total_topics*100:.0f}%)")
    report.append(f"  Key Formulas: {quality_metrics['formulas']}/{total_topics} topics ({quality_metrics['formulas']/total_topics*100:.0f}%)")
    report.append(f"  Intuitive Explanations: {quality_metrics['intuitive_explanations']}/{total_topics} topics ({quality_metrics['intuitive_explanations']/total_topics*100:.0f}%)")
    report.append(f"  Practice Problems: {quality_metrics['practice_problems']} total")
    report.append(f"  Key Takeaways: {quality_metrics['key_takeaways']}/{total_topics} topics ({quality_metrics['key_takeaways']/total_topics*100:.0f}%)")
    report.append("")

    # Final validation
    report.append("=" * 80)
    report.append("FINAL VALIDATION")
    report.append("=" * 80)
    report.append("")

    if total_issues == 0 and total_warnings == 0:
        report.append("STATUS: ALL TOPICS PASS PEDAGOGICAL STANDARDS")
        report.append("The course is complete and ready for delivery.")
    elif total_issues == 0:
        report.append(f"STATUS: MINOR WARNINGS ({total_warnings} warnings)")
        report.append("The course is acceptable but could be enhanced.")
    else:
        report.append(f"STATUS: ISSUES DETECTED ({total_issues} critical issues, {total_warnings} warnings)")
        report.append("The course requires fixes before delivery.")

    report.append("")
    report.append("=" * 80)

    return "\n".join(report)

def main():
    topic_dir = Path(__file__).parent / "topic_pdfs"

    # Analyze all topics
    all_analyses = []
    for i in range(1, 21):
        filepath = topic_dir / f"topic_{i:02d}_extended.tex"
        if filepath.exists():
            analysis = analyze_topic_file(filepath)
            all_analyses.append(analysis)
        else:
            print(f"WARNING: {filepath} not found")

    # Generate and print report
    report = generate_report(all_analyses)
    print(report)

    # Save report
    report_path = Path(__file__).parent / "pedagogical_analysis_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nReport saved to: {report_path}")

if __name__ == "__main__":
    main()
