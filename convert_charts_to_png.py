"""
Convert all chart PDFs to PNG format for GitHub Pages web display.
Uses pdf2image library (requires poppler).
"""
import subprocess
from pathlib import Path

def convert_pdf_to_png(pdf_path, output_dir, dpi=150):
    """Convert a PDF to PNG using pdftoppm (poppler)."""
    output_path = output_dir / f"{pdf_path.stem}.png"

    try:
        # Use pdftoppm from poppler (cross-platform)
        result = subprocess.run([
            'pdftoppm',
            '-png',
            '-r', str(dpi),
            '-singlefile',
            str(pdf_path),
            str(output_path.with_suffix(''))  # pdftoppm adds .png
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print(f"  Converted: {pdf_path.name} -> {output_path.name}")
            return True
        else:
            print(f"  ERROR: {pdf_path.name} - {result.stderr}")
            return False
    except FileNotFoundError:
        # Fallback: try using ImageMagick convert
        try:
            result = subprocess.run([
                'magick',
                '-density', str(dpi),
                str(pdf_path),
                '-flatten',
                str(output_path)
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print(f"  Converted (ImageMagick): {pdf_path.name} -> {output_path.name}")
                return True
            else:
                print(f"  ERROR: {pdf_path.name} - {result.stderr}")
                return False
        except FileNotFoundError:
            print(f"  ERROR: Neither poppler nor ImageMagick found. Install one of them.")
            return False

def main():
    """Convert all chart PDFs to PNGs."""
    print("Converting chart PDFs to PNG for web display...\n")

    # Create output directory
    output_dir = Path('docs/assets/images')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all chart folders
    chart_folders = sorted([f for f in Path('.').iterdir()
                           if f.is_dir() and f.name[0:2].isdigit()])

    if not chart_folders:
        print("ERROR: No chart folders found")
        return

    print(f"Found {len(chart_folders)} chart folders\n")
    print("=" * 60)

    success_count = 0
    for folder in chart_folders:
        pdf_files = list(folder.glob('*.pdf'))
        if pdf_files:
            # Use first PDF (main chart)
            pdf_file = pdf_files[0]
            if convert_pdf_to_png(pdf_file, output_dir):
                success_count += 1
        else:
            print(f"  WARNING: No PDF in {folder.name}")

    print("=" * 60)
    print(f"\nCOMPLETE: Converted {success_count}/{len(chart_folders)} charts")
    print(f"Output directory: {output_dir}")

if __name__ == '__main__':
    main()
