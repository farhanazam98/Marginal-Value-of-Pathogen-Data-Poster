#!/usr/bin/env bash
# Convert the pipeline-schematic SVG source to a vector PDF for pdflatex.
#
#   figures/protein-varient-scoring.svg  -->  figures/protein-varient-scoring.pdf
#
# The SVG is the canonical, hand-editable source. pdflatex cannot \includegraphics
# an SVG directly, so this produces a true-vector PDF (no rasterisation) via
# svglib + reportlab, both pure-Python (no system Cairo / Inkscape needed).
#
# First run creates a local virtualenv at .venv-svg/ (git-ignored) and installs
# svglib into it. Re-run any time the SVG changes.

set -euo pipefail
cd "$(dirname "$0")/.."

VENV=.venv-svg
SRC=figures/protein-varient-scoring.svg
OUT=figures/protein-varient-scoring.pdf

if [ ! -x "$VENV/bin/python" ]; then
  echo "creating $VENV ..."
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install --quiet --upgrade pip
  "$VENV/bin/pip" install --quiet 'svglib==2.2.0'
fi

"$VENV/bin/python" - "$SRC" "$OUT" <<'PY'
import sys
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

src, out = sys.argv[1], sys.argv[2]
drawing = svg2rlg(src)
renderPDF.drawToFile(drawing, out)

# fail loudly if a raster image snuck into the "vector" PDF
data = open(out, "rb").read()
n = data.count(b"/Subtype /Image")
print(f"wrote {out}  ({len(data)} bytes, {drawing.width:.0f}x{drawing.height:.0f}pt, raster XObjects: {n})")
if n:
    sys.exit("ERROR: output PDF contains a raster image")
PY
