"""
Extended Topic PDF Generator for Neural Networks Course
Generates 20 extended topic PDFs (6-10 slides each) from markdown files.

Structure per PDF:
1. Title Slide
2. Learning Goal slide
3. Key Concept slide (1-2 slides)
4. Visual/Chart slide
5. Key Formula slide (with LaTeX math)
6. Intuitive Explanation slide
7. Practice Problem slide(s)
8. Key Takeaways slide
"""

import re
from pathlib import Path
import subprocess
import sys

# Topic mapping: folder_name -> md_file
TOPIC_MAPPING = {
    '01_biological_neuron': '01-biological-neuron.md',
    '02_single_neuron_function': '02-single-neuron-computation.md',
    '03_problem_visualization': '03-problem-visualization.md',
    '04_neuron_decision_maker': '04-neuron-decision-maker.md',
    '05_activation_functions': '05-activation-functions.md',
    '06_linear_limitation': '06-linear-limitation.md',
    '07_sigmoid_saturation': '07-sigmoid-saturation.md',
    '08_boundary_evolution': '08-boundary-evolution.md',
    '09_network_architecture': '09-network-architecture.md',
    '10_forward_propagation': '10-forward-propagation.md',
    '11_decision_boundary_concept': '11-decision-boundary-concept.md',
    '12_feature_hierarchy': '12-feature-hierarchy.md',
    '13_loss_landscape': '13-loss-landscape.md',
    '14_gradient_descent': '14-gradient-descent.md',
    '15_overfitting_underfitting': '15-overfitting-underfitting.md',
    '16_learning_rate_comparison': '16-learning-rate-comparison.md',
    '17_market_prediction_data': '17-market-prediction-data.md',
    '18_prediction_results': '18-prediction-results.md',
    '19_confusion_matrix': '19-confusion-matrix.md',
    '20_trading_backtest': '20-trading-backtest.md',
}

# Chart PDF mapping: folder_name -> actual_pdf_name
CHART_PDF_MAPPING = {
    '01_biological_neuron': 'biological_vs_artificial.pdf',
    '02_single_neuron_function': 'single_neuron_computation.pdf',
    '03_problem_visualization': 'problem_visualization.pdf',
    '04_neuron_decision_maker': 'neuron_decision_maker.pdf',
    '05_activation_functions': 'activation_functions.pdf',
    '06_linear_limitation': 'linear_limitation.pdf',
    '07_sigmoid_saturation': 'sigmoid_saturation.pdf',
    '08_boundary_evolution': 'boundary_evolution.pdf',
    '09_network_architecture': 'network_architecture.pdf',
    '10_forward_propagation': 'forward_propagation.pdf',
    '11_decision_boundary_concept': 'decision_boundary_concept.pdf',
    '12_feature_hierarchy': 'feature_hierarchy.pdf',
    '13_loss_landscape': 'loss_landscape.pdf',
    '14_gradient_descent': 'gradient_descent.pdf',
    '15_overfitting_underfitting': 'overfitting_underfitting.pdf',
    '16_learning_rate_comparison': 'learning_rate_comparison.pdf',
    '17_market_prediction_data': 'market_prediction_data.pdf',
    '18_prediction_results': 'prediction_results.pdf',
    '19_confusion_matrix': 'confusion_matrix.pdf',
    '20_trading_backtest': 'trading_backtest.pdf',
}

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        frontmatter = {}
        for line in match.group(1).split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip().strip('"')
        remaining = content[match.end():]
        return frontmatter, remaining
    return {}, content

def split_sections(content):
    """Split markdown content into sections."""
    sections = {}
    current_section = None
    current_content = []

    for line in content.split('\n'):
        if line.startswith('## '):
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = line[3:].strip()
            current_content = []
        elif line.startswith('# ') and not current_section:
            # Skip main title
            continue
        elif line == '---':
            # Skip markdown separators
            continue
        else:
            current_content.append(line)

    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()

    return sections

def convert_math(text):
    """Convert markdown math to LaTeX math."""
    # Convert inline math $...$ to \(...\)
    text = re.sub(r'(?<!\$)\$(?!\$)(.+?)\$', r'\\(\1\\)', text)
    # Convert display math $$...$$ to \[...\]
    text = re.sub(r'\$\$(.+?)\$\$', r'\\[\1\\]', text, flags=re.DOTALL)
    return text

def convert_bold(text):
    """Convert markdown **bold** to LaTeX \textbf{bold}."""
    # Special case: if bold contains math notation (^, _, etc), use \mathbf in math mode
    def replace_bold(match):
        content = match.group(1)
        # Check if content has math-like characters
        if re.search(r'[\^_{}]|\[.\]', content):
            # Wrap in math mode with mathbf
            return f'\\(\\mathbf{{{content}}}\\)'
        else:
            return f'\\textbf{{{content}}}'

    text = re.sub(r'\*\*(.+?)\*\*', replace_bold, text)
    return text

def convert_italic(text):
    """Convert markdown *italic* to LaTeX \textit{italic}."""
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)\*(?!\*)', r'\\textit{\1}', text)
    return text

def escape_latex(text):
    """Escape special LaTeX characters."""
    # Don't escape already escaped characters or math mode
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '#': r'\#',
        '_': r'\_',
        '^': r'\^{}',
    }
    for char, escaped in replacements.items():
        # Only replace if not already escaped and not in LaTeX commands
        if char == '^':
            # Don't escape ^ if followed by { (already LaTeX syntax) or inside \textbf{}
            text = re.sub(r'(?<!\\)\^(?![{\[])', escaped, text)
        else:
            text = re.sub(f'(?<!\\\\){re.escape(char)}', escaped, text)
    return text

def process_text(text):
    """Process markdown text to LaTeX."""
    # First handle math (before escaping)
    text = convert_math(text)
    # Then handle bold and italic (before escaping)
    text = convert_bold(text)
    text = convert_italic(text)
    # Then escape remaining special chars (but not in math mode)
    # Split by math delimiters and only escape text parts
    parts = re.split(r'(\\\(.*?\\\)|\\\[.*?\\\])', text, flags=re.DOTALL)
    processed_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 0:  # Text part
            part = escape_latex(part)
        processed_parts.append(part)
    text = ''.join(processed_parts)
    return text

def create_itemize_list(items):
    """Create LaTeX itemize environment from list items."""
    if not items:
        return ''
    latex = '\\begin{itemize}\n'
    for item in items:
        latex += f'  \\item {process_text(item)}\n'
    latex += '\\end{itemize}\n'
    return latex

def parse_practice_problems(content):
    """Parse practice problems section into individual problems."""
    problems = []
    current_problem = {'question': '', 'solution': ''}
    in_solution = False

    for line in content.split('\n'):
        if line.startswith('### Problem'):
            if current_problem['question']:
                problems.append(current_problem)
            current_problem = {'question': '', 'solution': '', 'title': line[4:].strip()}
            in_solution = False
        elif '<details>' in line or '<summary>' in line or '</summary>' in line or '</details>' in line:
            in_solution = '<details>' in line or in_solution
            continue
        elif in_solution:
            current_problem['solution'] += line + '\n'
        else:
            current_problem['question'] += line + '\n'

    if current_problem['question']:
        problems.append(current_problem)

    return problems

def split_long_text(text, max_length=500):
    """Split long text into chunks for multiple slides."""
    # Split by paragraphs
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    chunks = []
    current_chunk = []
    current_length = 0

    for para in paragraphs:
        para_length = len(para)
        if current_length + para_length > max_length and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_length = para_length
        else:
            current_chunk.append(para)
            current_length += para_length

    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))

    return chunks if chunks else [text]

def generate_latex(topic_num, folder_name, md_file):
    """Generate LaTeX for a single topic."""

    # Read markdown file
    base_path = Path(__file__).parent
    md_path = base_path / 'docs' / 'topics' / md_file

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter, body = extract_frontmatter(content)
    sections = split_sections(body)

    # Extract title
    title = frontmatter.get('title', f'Topic {topic_num:02d}')

    # Start LaTeX document
    latex = r'''\documentclass[8pt,aspectratio=169]{beamer}
\usetheme{Madrid}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{tikz}

% Color definitions
\definecolor{mlblue}{RGB}{0,102,204}
\definecolor{mlpurple}{RGB}{51,51,178}
\definecolor{mllavender}{RGB}{173,173,224}
\definecolor{mllavender2}{RGB}{193,193,232}
\definecolor{mllavender3}{RGB}{204,204,235}
\definecolor{mllavender4}{RGB}{214,214,239}
\definecolor{mlorange}{RGB}{255, 127, 14}
\definecolor{mlgreen}{RGB}{44, 160, 44}
\definecolor{mlred}{RGB}{214, 39, 40}

% Apply custom colors
\setbeamercolor{palette primary}{bg=mllavender3,fg=mlpurple}
\setbeamercolor{palette secondary}{bg=mllavender2,fg=mlpurple}
\setbeamercolor{palette tertiary}{bg=mllavender,fg=white}
\setbeamercolor{palette quaternary}{bg=mlpurple,fg=white}
\setbeamercolor{structure}{fg=mlpurple}
\setbeamercolor{frametitle}{fg=mlpurple,bg=mllavender3}
\setbeamercolor{block title}{bg=mllavender2,fg=mlpurple}
\setbeamercolor{block body}{bg=mllavender4,fg=black}

\setbeamertemplate{navigation symbols}{}
\setbeamersize{text margin left=5mm,text margin right=5mm}

'''

    latex += f'\\title{{{title}}}\n'
    latex += '\\subtitle{Neural Networks - From Brain to Business}\n'
    latex += '\\date{}\n\n'
    latex += '\\begin{document}\n\n'

    # 1. Title slide
    latex += '\\begin{frame}[plain]\n\\titlepage\n\\end{frame}\n\n'

    # 2. Learning Goal slide
    if 'Learning Goal' in sections:
        latex += '\\begin{frame}{Learning Goal}\n'
        latex += process_text(sections['Learning Goal'])
        latex += '\n\\end{frame}\n\n'

    # 3. Key Concept slide(s) - split if too long
    if 'Key Concept' in sections:
        concept_chunks = split_long_text(sections['Key Concept'])
        for i, chunk in enumerate(concept_chunks):
            title_suffix = f' ({i+1}/{len(concept_chunks)})' if len(concept_chunks) > 1 else ''
            latex += f'\\begin{{frame}}{{Key Concept{title_suffix}}}\n'
            latex += process_text(chunk)
            latex += '\n\\end{frame}\n\n'

    # 4. Visual/Chart slide
    chart_pdf_name = CHART_PDF_MAPPING.get(folder_name, f'{folder_name}.pdf')
    chart_pdf = f'{folder_name}/{chart_pdf_name}'

    latex += '\\begin{frame}{Visualization}\n'
    latex += '\\begin{center}\n'
    latex += f'\\includegraphics[width=0.9\\textwidth,height=0.75\\textheight,keepaspectratio]{{{chart_pdf}}}\n'
    latex += '\\end{center}\n'
    latex += '\\end{frame}\n\n'

    # 5. Key Formula slide
    if 'Key Formula' in sections or 'Key Formulas' in sections:
        formula_content = sections.get('Key Formula', sections.get('Key Formulas', ''))
        latex += '\\begin{frame}{Key Formula}\n'
        latex += process_text(formula_content)
        latex += '\n\\end{frame}\n\n'

    # 6. Intuitive Explanation slide
    if 'Intuitive Explanation' in sections:
        latex += '\\begin{frame}{Intuitive Explanation}\n'
        latex += process_text(sections['Intuitive Explanation'])
        latex += '\n\\end{frame}\n\n'

    # 7. Practice Problems slide(s)
    if 'Practice Problems' in sections:
        problems = parse_practice_problems(sections['Practice Problems'])
        for i, problem in enumerate(problems[:2], 1):  # Limit to 2 problems for space
            latex += f'\\begin{{frame}}{{Practice Problem {i}}}\n'
            latex += '\\textbf{' + process_text(problem.get('title', f'Problem {i}')) + '}\n\n'
            latex += process_text(problem['question'])
            latex += '\n\\vspace{1em}\n'
            if problem['solution'].strip():
                latex += '\\begin{block}{Solution}\n'
                latex += '\\small\n'
                # Smart truncation: find a good breaking point (paragraph or sentence)
                solution = problem['solution']
                if len(solution) > 800:
                    # Try to break at paragraph
                    paras = solution.split('\n\n')
                    if len(paras) > 1:
                        solution = '\n\n'.join(paras[:2])  # First 2 paragraphs
                    else:
                        solution = solution[:800]
                latex += process_text(solution)
                latex += '\n\\end{block}\n'
            latex += '\\end{frame}\n\n'

    # 8. Key Takeaways slide
    if 'Key Takeaways' in sections:
        takeaways = sections['Key Takeaways']
        # Extract bullet points
        items = [line.strip('- ').strip() for line in takeaways.split('\n') if line.strip().startswith('-')]

        latex += '\\begin{frame}{Key Takeaways}\n'
        if items:
            latex += create_itemize_list(items)
        else:
            latex += process_text(takeaways)
        latex += '\\end{frame}\n\n'

    latex += '\\end{document}\n'

    return latex

def compile_pdf(tex_file, output_dir):
    """Compile LaTeX to PDF using pdflatex."""
    try:
        # Run pdflatex twice for proper references
        for _ in range(2):
            result = subprocess.run(
                ['pdflatex', '-output-directory', str(output_dir), str(tex_file)],
                capture_output=True,
                text=True,
                timeout=60
            )

        # Check if PDF was created
        pdf_file = tex_file.with_suffix('.pdf')
        if pdf_file.exists():
            return True, None
        else:
            return False, result.stderr

    except subprocess.TimeoutExpired:
        return False, "Compilation timeout"
    except Exception as e:
        return False, str(e)

def main():
    """Generate all 20 extended topic PDFs."""

    base_path = Path(__file__).parent
    output_dir = base_path / 'topic_pdfs'
    output_dir.mkdir(exist_ok=True)

    results = []
    failed = []

    for topic_num, (folder_name, md_file) in enumerate(TOPIC_MAPPING.items(), 1):
        print(f"[{topic_num}/20] Generating {folder_name}...")

        try:
            # Generate LaTeX
            latex_content = generate_latex(topic_num, folder_name, md_file)

            # Write .tex file
            tex_file = output_dir / f'topic_{topic_num:02d}_extended.tex'
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)

            # Compile to PDF
            success, error = compile_pdf(tex_file, output_dir)

            if success:
                # Count slides (approximate by counting \begin{frame})
                slide_count = latex_content.count('\\begin{frame}')
                results.append((topic_num, folder_name, slide_count, 'SUCCESS'))
                print(f"  [OK] Generated {slide_count} slides")
            else:
                failed.append((topic_num, folder_name, error))
                results.append((topic_num, folder_name, 0, f'FAILED: {error}'))
                print(f"  [FAIL] Compilation failed: {error}")

        except Exception as e:
            failed.append((topic_num, folder_name, str(e)))
            results.append((topic_num, folder_name, 0, f'ERROR: {str(e)}'))
            print(f"  [ERROR] Error: {e}")

        # Reflection gates
        if topic_num in [5, 10, 15, 20]:
            print(f"\n{'='*60}")
            print(f"REFLECTION GATE: Topics 1-{topic_num} Complete")
            print(f"{'='*60}")
            successful = [r for r in results if 'SUCCESS' in r[3]]
            print(f"Successful: {len(successful)}/{topic_num}")
            print(f"Failed: {len(failed)}")
            if failed:
                print("\nFailed topics:")
                for num, name, err in failed[-5:]:  # Show last 5 failures
                    print(f"  Topic {num} ({name}): {err[:100]}")
            print(f"{'='*60}\n")

    # Final report
    print("\n" + "="*60)
    print("FINAL REPORT")
    print("="*60)

    print("\nSlide counts per topic:")
    for topic_num, folder, slides, status in results:
        print(f"  Topic {topic_num:02d}: {slides} slides - {status}")

    successful = [r for r in results if 'SUCCESS' in r[3]]
    print(f"\nTotal successful: {len(successful)}/20")
    print(f"Total failed: {len(failed)}/20")

    if failed:
        print("\nFailed topics details:")
        for num, name, err in failed:
            print(f"\n  Topic {num} ({name}):")
            print(f"    {err[:200]}")

    print("\n" + "="*60)

if __name__ == '__main__':
    main()
