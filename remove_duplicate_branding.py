"""Remove duplicate branding blocks from .tex file"""
import re
from pathlib import Path

tex_file = Path('20251126_0049_quantlet_branding.tex')
content = tex_file.read_text(encoding='utf-8')

print(f"Processing {tex_file.name}...")
print(f"Original size: {len(content)} characters")

# Remove ALL existing branding blocks
# Pattern matches from comment line through the full tikzpicture environment
pattern = r'\n% Quantlet branding \(auto-generated\).*?\\end\{tikzpicture\}\n'
cleaned = re.sub(pattern, '\n', content, flags=re.DOTALL)

print(f"Cleaned size: {len(cleaned)} characters")
print(f"Removed {len(content) - len(cleaned)} characters")

# Save cleaned version
tex_file.write_text(cleaned, encoding='utf-8')
print(f"\nRemoved all branding blocks from {tex_file.name}")
