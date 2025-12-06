"""
Update all extended topic PDFs to use template_beamer_final.tex preamble.

This script:
1. Reads the template preamble from template_beamer_final.tex
2. Replaces the old preamble in each topic_XX_extended.tex file
3. Adds appropriate \bottomnote{} annotations
4. Compiles each updated .tex file to PDF
5. Reports compilation status
"""

import os
import re
import subprocess
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent
TOPIC_DIR = BASE_DIR / "topic_pdfs"
TEMP_DIR = TOPIC_DIR / "temp"

# Create temp directory if it doesn't exist
TEMP_DIR.mkdir(exist_ok=True)

# Template preamble (from template_beamer_final.tex)
TEMPLATE_PREAMBLE = r"""\documentclass[8pt,aspectratio=169]{beamer}
\usetheme{Madrid}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{adjustbox}
\usepackage{multicol}
\usepackage{amsmath}
\usepackage{amssymb}

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
\definecolor{mlgray}{RGB}{127, 127, 127}

% Additional colors for template compatibility
\definecolor{lightgray}{RGB}{240, 240, 240}
\definecolor{midgray}{RGB}{180, 180, 180}

% Apply custom colors to Madrid theme
\setbeamercolor{palette primary}{bg=mllavender3,fg=mlpurple}
\setbeamercolor{palette secondary}{bg=mllavender2,fg=mlpurple}
\setbeamercolor{palette tertiary}{bg=mllavender,fg=white}
\setbeamercolor{palette quaternary}{bg=mlpurple,fg=white}

\setbeamercolor{structure}{fg=mlpurple}
\setbeamercolor{section in toc}{fg=mlpurple}
\setbeamercolor{subsection in toc}{fg=mlblue}
\setbeamercolor{title}{fg=mlpurple}
\setbeamercolor{frametitle}{fg=mlpurple,bg=mllavender3}
\setbeamercolor{block title}{bg=mllavender2,fg=mlpurple}
\setbeamercolor{block body}{bg=mllavender4,fg=black}

% Remove navigation symbols
\setbeamertemplate{navigation symbols}{}

% Clean itemize/enumerate
\setbeamertemplate{itemize items}[circle]
\setbeamertemplate{enumerate items}[default]

% Reduce margins for more content space
\setbeamersize{text margin left=5mm,text margin right=5mm}

% Command for bottom annotation (Madrid-style)
\newcommand{\bottomnote}[1]{%
\vfill
\vspace{-2mm}
\textcolor{mllavender2}{\rule{\textwidth}{0.4pt}}
\vspace{1mm}
\footnotesize
\textbf{#1}
}
"""

# Bottom notes for different slide types
BOTTOMNOTES = {
    'learning_goal': 'This slide establishes the learning objective for this topic',
    'key_concept': 'Understanding this concept is crucial for neural network fundamentals',
    'visualization': 'Visual representations help solidify abstract concepts',
    'formula': 'Mathematical formalization provides precision',
    'intuition': 'Intuitive explanations bridge theory and practice',
    'practice': 'Practice problems reinforce understanding',
    'takeaways': 'These key points summarize the essential learnings'
}

def extract_content_after_begin_document(tex_content):
    """Extract content after \begin{document}"""
    match = re.search(r'\\begin{document}', tex_content)
    if match:
        return tex_content[match.start():]
    return None

def add_bottomnotes_to_content(content):
    """Add appropriate \bottomnote{} to frames based on their title/type"""

    # Add bottomnote before \end{frame} for specific frame types
    def add_note_to_frame(match):
        frame_content = match.group(0)
        frame_title = match.group(1) if match.lastindex and match.lastindex >= 1 else ""

        # Skip if already has bottomnote
        if r'\bottomnote' in frame_content:
            return frame_content

        # Determine note based on frame title
        note = None
        title_lower = frame_title.lower()

        if 'learning goal' in title_lower:
            note = BOTTOMNOTES['learning_goal']
        elif 'key concept' in title_lower:
            note = BOTTOMNOTES['key_concept']
        elif 'visualization' in title_lower:
            note = BOTTOMNOTES['visualization']
        elif 'formula' in title_lower:
            note = BOTTOMNOTES['formula']
        elif 'intuitive explanation' in title_lower or 'intuition' in title_lower:
            note = BOTTOMNOTES['intuition']
        elif 'practice' in title_lower or 'problem' in title_lower:
            note = BOTTOMNOTES['practice']
        elif 'takeaway' in title_lower:
            note = BOTTOMNOTES['takeaways']

        # Add bottomnote before \end{frame}
        if note:
            frame_content = frame_content.replace(
                r'\end{frame}',
                f'\n\\bottomnote{{{note}}}\n\\end{{frame}}'
            )

        return frame_content

    # Match frames with optional title
    content = re.sub(
        r'\\begin{frame}(?:\{([^}]*)\})?.*?\\end{frame}',
        add_note_to_frame,
        content,
        flags=re.DOTALL
    )

    return content

def update_tex_file(tex_file):
    """Update a single .tex file with the new template preamble"""
    print(f"\nProcessing {tex_file.name}...")

    # Read original file
    with open(tex_file, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # Extract content after \begin{document}
    document_content = extract_content_after_begin_document(original_content)

    if not document_content:
        print(f"  ERROR: Could not find \\begin{{document}} in {tex_file.name}")
        return False

    # Add bottomnotes to content
    document_content = add_bottomnotes_to_content(document_content)

    # Combine template preamble with document content
    new_content = TEMPLATE_PREAMBLE + "\n" + document_content

    # Write updated file
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  Updated {tex_file.name} successfully")
    return True

def compile_pdf(tex_file):
    """Compile a .tex file to PDF using pdflatex"""
    print(f"  Compiling {tex_file.name} to PDF...")

    try:
        # Run pdflatex
        result = subprocess.run(
            ['pdflatex', '-output-directory', str(tex_file.parent), str(tex_file)],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print(f"  Successfully compiled {tex_file.stem}.pdf")

            # Move auxiliary files to temp/
            aux_extensions = ['.aux', '.log', '.nav', '.out', '.snm', '.toc']
            for ext in aux_extensions:
                aux_file = tex_file.with_suffix(ext)
                if aux_file.exists():
                    dest = TEMP_DIR / aux_file.name
                    aux_file.rename(dest)

            return True
        else:
            print(f"  ERROR: Compilation failed for {tex_file.name}")
            print(f"  {result.stderr[:500]}")  # Print first 500 chars of error
            return False

    except subprocess.TimeoutExpired:
        print(f"  ERROR: Compilation timeout for {tex_file.name}")
        return False
    except Exception as e:
        print(f"  ERROR: {str(e)}")
        return False

def main():
    """Main execution function"""
    print("=" * 80)
    print("UPDATING EXTENDED TOPIC PDFS WITH PROFESSIONAL TEMPLATE")
    print("=" * 80)

    # Find all topic_XX_extended.tex files
    tex_files = sorted(TOPIC_DIR.glob("topic_*_extended.tex"))

    if not tex_files:
        print("ERROR: No topic_*_extended.tex files found")
        return

    print(f"\nFound {len(tex_files)} extended topic files")

    # Track results
    update_results = []
    compile_results = []

    # Process each file
    for i, tex_file in enumerate(tex_files, 1):
        print(f"\n{'='*60}")
        print(f"TOPIC {i}/{len(tex_files)}")
        print(f"{'='*60}")

        # Update .tex file
        update_success = update_tex_file(tex_file)
        update_results.append((tex_file.name, update_success))

        if not update_success:
            compile_results.append((tex_file.name, False))
            continue

        # Compile to PDF
        compile_success = compile_pdf(tex_file)
        compile_results.append((tex_file.name, compile_success))

        # Reflection gate: Pause after every 5 topics
        if i % 5 == 0 and i < len(tex_files):
            print(f"\n{'='*60}")
            print(f"REFLECTION GATE: {i} topics processed")
            print(f"{'='*60}")
            successes = sum(1 for _, s in compile_results[-5:] if s)
            print(f"Last 5 compilations: {successes}/5 successful")
            print("Continuing to next batch...")

    # Final report
    print("\n" + "="*80)
    print("FINAL REPORT")
    print("="*80)

    print("\n--- Update Results ---")
    update_success_count = sum(1 for _, s in update_results if s)
    print(f"Successfully updated: {update_success_count}/{len(update_results)}")

    for name, success in update_results:
        status = "OK" if success else "FAILED"
        print(f"  {name}: {status}")

    print("\n--- Compilation Results ---")
    compile_success_count = sum(1 for _, s in compile_results if s)
    print(f"Successfully compiled: {compile_success_count}/{len(compile_results)}")

    for name, success in compile_results:
        status = "OK" if success else "FAILED"
        print(f"  {name}: {status}")

    # Summary
    print("\n" + "="*80)
    if update_success_count == len(tex_files) and compile_success_count == len(tex_files):
        print("SUCCESS: All topics updated and compiled successfully!")
    else:
        print(f"PARTIAL SUCCESS: {update_success_count}/{len(tex_files)} updated, "
              f"{compile_success_count}/{len(tex_files)} compiled")
    print("="*80)

if __name__ == '__main__':
    main()
