"""
Generate Individual Topic PDFs

Creates 20 separate PDF files, one for each topic.
Each PDF contains the concept slide + chart slide for that topic.

Usage: python generate_topic_pdfs.py
"""

import os
import re
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
TOPIC_PDFS_DIR = PROJECT_ROOT / 'topic_pdfs'
MAIN_TEX = PROJECT_ROOT / '20251128_0825_quantlet_branding.tex'

# Topic definitions with frame titles to extract
TOPICS = {
    '01': {'name': 'Biological Neuron', 'frames': ['Nature\'s Computer', 'From Biology to Artificial']},
    '02': {'name': 'Single Neuron', 'frames': ['The Artificial Neuron', 'Single Neuron Computation']},
    '03': {'name': 'Problem Visualization', 'frames': ['Why Simple Rules Fail', 'What We Need']},
    '04': {'name': 'Neuron Decision Maker', 'frames': ['From Concept to Computation', 'Practice: Calculate']},
    '05': {'name': 'Activation Functions', 'frames': ['Activation Functions: Why', 'Activation Functions: Visual']},
    '06': {'name': 'Linear Limitation', 'frames': ['The Limitation: Why One', 'Visual Proof: The XOR']},
    '07': {'name': 'Sigmoid Saturation', 'frames': ['Advanced: The Vanishing', 'Solution: How Adding']},
    '08': {'name': 'Boundary Evolution', 'frames': ['The Goal: Learn Complex', 'Solution: How Adding']},
    '09': {'name': 'Network Architecture', 'frames': ['Building the Network', 'Neural Network Architecture']},
    '10': {'name': 'Forward Propagation', 'frames': ['Forward Propagation: How', 'Forward Propagation: Detailed']},
    '11': {'name': 'Decision Boundary', 'frames': ['The Goal: Learn Complex', 'Solution: How Adding']},
    '12': {'name': 'Feature Hierarchy', 'frames': ['Feature Hierarchy (Part 1)', 'Feature Hierarchy (Part 2)']},
    '13': {'name': 'Loss Landscape', 'frames': ['Learning from Mistakes', 'Loss Landscape']},
    '14': {'name': 'Gradient Descent', 'frames': ['Gradient Descent: Learning', 'Gradient Descent: Optimization']},
    '15': {'name': 'Overfitting', 'frames': ['Critical Concept: Overfitting', 'Discussion: Part 4']},
    '16': {'name': 'Learning Rate', 'frames': ['Gradient Descent: Learning', 'Gradient Descent: Optimization']},
    '17': {'name': 'Market Data', 'frames': ['Putting It Together', 'Market Data: Input']},
    '18': {'name': 'Prediction Results', 'frames': ['Training Results', 'Prediction Results']},
    '19': {'name': 'Confusion Matrix', 'frames': ['Understanding Model Performance', 'The Business Case']},
    '20': {'name': 'Trading Backtest', 'frames': ['The Business Case', 'Summary: Three Key']},
}

# Chart files for each topic (using new numbering)
CHART_FILES = {
    '01': '01_biological_neuron/biological_vs_artificial.pdf',
    '02': '02_single_neuron_function/single_neuron_computation.pdf',
    '03': '03_problem_visualization/problem_visualization.pdf',
    '04': '04_neuron_decision_maker/neuron_decision_maker.pdf',
    '05': '05_activation_functions/activation_functions.pdf',
    '06': '06_linear_limitation/linear_limitation.pdf',
    '07': '07_sigmoid_saturation/sigmoid_saturation.pdf',
    '08': '08_boundary_evolution/boundary_evolution.pdf',
    '09': '09_network_architecture/network_architecture.pdf',
    '10': '10_forward_propagation/forward_propagation.pdf',
    '11': '11_decision_boundary_concept/decision_boundary_concept.pdf',
    '12': '12_feature_hierarchy/feature_hierarchy.pdf',
    '13': '13_loss_landscape/loss_landscape.pdf',
    '14': '14_gradient_descent/gradient_descent.pdf',
    '15': '15_overfitting_underfitting/overfitting_underfitting.pdf',
    '16': '16_learning_rate_comparison/learning_rate_comparison.pdf',
    '17': '17_market_prediction_data/market_prediction_data.pdf',
    '18': '18_prediction_results/prediction_results.pdf',
    '19': '19_confusion_matrix/confusion_matrix.pdf',
    '20': '20_trading_backtest/trading_backtest.pdf',
}


def create_topic_tex(topic_num, topic_info):
    """Create a minimal LaTeX file for a single topic with its chart."""
    chart_path = CHART_FILES.get(topic_num, '')

    tex_content = f'''\\documentclass[8pt,aspectratio=169]{{beamer}}
\\usetheme{{Madrid}}
\\usepackage{{graphicx}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}

% Color definitions
\\definecolor{{mlblue}}{{RGB}}{{0,102,204}}
\\definecolor{{mlpurple}}{{RGB}}{{51,51,178}}
\\definecolor{{mllavender}}{{RGB}}{{173,173,224}}
\\definecolor{{mllavender2}}{{RGB}}{{193,193,232}}
\\definecolor{{mllavender3}}{{RGB}}{{204,204,235}}
\\definecolor{{mllavender4}}{{RGB}}{{214,214,239}}

% Apply custom colors
\\setbeamercolor{{palette primary}}{{bg=mllavender3,fg=mlpurple}}
\\setbeamercolor{{palette secondary}}{{bg=mllavender2,fg=mlpurple}}
\\setbeamercolor{{palette tertiary}}{{bg=mllavender,fg=white}}
\\setbeamercolor{{palette quaternary}}{{bg=mlpurple,fg=white}}
\\setbeamercolor{{structure}}{{fg=mlpurple}}
\\setbeamercolor{{frametitle}}{{fg=mlpurple,bg=mllavender3}}

\\setbeamertemplate{{navigation symbols}}{{}}
\\setbeamersize{{text margin left=5mm,text margin right=5mm}}

\\title{{Topic {topic_num}: {topic_info['name']}}}
\\subtitle{{Neural Networks - From Brain to Business}}
\\date{{}}

\\begin{{document}}

\\begin{{frame}}[plain]
\\titlepage
\\end{{frame}}

\\begin{{frame}}{{Topic {topic_num}: {topic_info['name']}}}
\\begin{{center}}
\\includegraphics[width=0.9\\textwidth,height=0.75\\textheight,keepaspectratio]{{{chart_path}}}
\\end{{center}}
\\end{{frame}}

\\end{{document}}
'''
    return tex_content


def compile_tex(tex_file, output_dir):
    """Compile a LaTeX file to PDF."""
    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(tex_file)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(PROJECT_ROOT)
        )
        return result.returncode == 0
    except Exception as e:
        print(f"  [ERROR] Compilation failed: {e}")
        return False


def main():
    print("\n" + "=" * 70)
    print("  GENERATING INDIVIDUAL TOPIC PDFs")
    print("=" * 70)

    # Create output directory
    TOPIC_PDFS_DIR.mkdir(exist_ok=True)
    print(f"\n  Output directory: {TOPIC_PDFS_DIR}")

    success_count = 0

    for topic_num, topic_info in TOPICS.items():
        print(f"\n  Processing Topic {topic_num}: {topic_info['name']}...")

        # Create .tex file
        tex_content = create_topic_tex(topic_num, topic_info)
        tex_file = TOPIC_PDFS_DIR / f"topic_{topic_num}.tex"
        tex_file.write_text(tex_content, encoding='utf-8')

        # Compile to PDF
        if compile_tex(tex_file, TOPIC_PDFS_DIR):
            pdf_file = TOPIC_PDFS_DIR / f"topic_{topic_num}.pdf"
            if pdf_file.exists():
                print(f"    [OK] Created: topic_{topic_num}.pdf")
                success_count += 1
            else:
                print(f"    [WARN] PDF not found after compilation")
        else:
            print(f"    [ERROR] Compilation failed")

    # Clean up auxiliary files
    print("\n  Cleaning up auxiliary files...")
    for ext in ['.aux', '.log', '.nav', '.out', '.snm', '.toc']:
        for f in TOPIC_PDFS_DIR.glob(f'*{ext}'):
            f.unlink()

    print("\n" + "=" * 70)
    print(f"  COMPLETE: {success_count}/20 PDFs generated")
    print("=" * 70)

    if success_count == 20:
        print("\n  All topic PDFs created successfully!")
    else:
        print(f"\n  [WARN] {20 - success_count} PDFs failed to generate")

    print(f"\n  PDFs located in: {TOPIC_PDFS_DIR}")


if __name__ == '__main__':
    main()
