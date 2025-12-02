# QuantLet Branding - Quick Reference

## One-Time Setup (New Project)

```bash
# 1. Copy quantlet_tools folder to your project
cp -r quantlet_tools /path/to/your/project/

# 2. Add CHART_METADATA to each chart's Python script
```

```python
# In your chart script (e.g., 01_chart/my_chart.py):
CHART_METADATA = {
    'title': 'Chart Title',
    'url': 'https://github.com/YourOrg/your-repo/tree/main/01_chart'
}
```

```bash
# 3. Copy QR code generator to project root
cp quantlet_tools/generate_qr_codes_template.py ../generate_qr_codes.py
```

---

## Add Branding (3 Commands)

```bash
# Step 1: Generate QR codes
python generate_qr_codes.py

# Step 2: Add branding to LaTeX
python quantlet_tools/add_latex_branding.py

# Step 3: Compile
pdflatex your_slides.tex
```

---

## Remove Branding

```bash
python quantlet_tools/remove_duplicate_branding.py
```

---

## File Structure

```
your_project/
├── quantlet_tools/              # Copy this entire folder
│   ├── add_latex_branding.py
│   ├── remove_duplicate_branding.py
│   ├── logo/quantlet.png
│   └── BRANDING_GUIDE.md
├── generate_qr_codes.py         # Copy from template
├── 01_chart/
│   ├── chart.py                 # Add CHART_METADATA here
│   ├── chart.pdf
│   └── qr_code.png              # Auto-generated
└── slides.tex
```

---

## What Gets Added

**Logo** (fully visible, 100% opaque) + **QR Code** (slightly transparent, 80% opaque) + **URL text**

All positioned at bottom-right via `\begin{tikzpicture}[remember picture, overlay]`

---

## Customization

Edit `quantlet_tools/add_latex_branding.py`:

- **Logo size**: Change `width=0.8cm`
- **Logo opacity**: Change `opacity=1.0` (currently 100%, fully visible)
- **Logo position**: Change `xshift=-0.3cm, yshift=0.6cm`
- **QR size**: Change `width=0.6cm`
- **QR opacity**: Change `opacity=0.8` (currently 80%, slightly transparent)
- **Font**: Change `\tiny` to `\scriptsize`, `\footnotesize`, etc.

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Logo not showing | Check `quantlet_tools/logo/quantlet.png` exists |
| QR not showing | Run `python generate_qr_codes.py` |
| Duplicate branding | Run `remove_duplicate_branding.py`, then re-add |
| No QR codes generated | Check CHART_METADATA exists in .py files |

---

## Full Documentation

See `BRANDING_GUIDE.md` for complete details.
