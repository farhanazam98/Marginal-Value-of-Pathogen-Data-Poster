#!/usr/bin/env bash
# Local render helper. This machine has no system TeX; prefer tectonic
# (brew install tectonic), fall back to a Docker TeXLive image.
# Output: build/main.pdf
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$ROOT/build"
cd "$ROOT"

# Homebrew bin isn't always on PATH in non-login shells
[ -x /opt/homebrew/bin/tectonic ] && PATH="/opt/homebrew/bin:$PATH"

if command -v tectonic >/dev/null 2>&1; then
  tectonic -X compile main.tex --outdir build
elif command -v pdflatex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
elif command -v docker >/dev/null 2>&1; then
  docker run --rm -v "$ROOT:/work" -w /work texlive/texlive:latest \
    pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
else
  echo "No tectonic, pdflatex, or docker found." >&2
  exit 1
fi
echo "-> $ROOT/build/main.pdf"
