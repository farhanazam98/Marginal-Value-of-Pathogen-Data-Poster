# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A standalone repo containing the LaTeX source for a single A0 research poster, plus the small data files (`data/`) and plotting code needed to render its figures. It has no connection to the `marginal-value-pathogen-data-v1` pipeline repo — no pipeline code lives here, and nothing in this repo should ever reference a path into that other repo. Figure *data* is real pipeline output, supplied by the user; Claude may plot that data locally (matplotlib etc.), but never fabricates or invents the underlying numbers.

The repo currently contains the unmodified Overleaf `tikzposter` starter template (`main.tex`) plus its sample logo — the actual poster content has not yet been built out.

## Build

```
pdflatex main.tex
```

Run twice if citations/references are added (for cross-reference resolution). Output should be directed to `build/poster.pdf` (create `build/` if it doesn't exist).

There is no lint or test suite in this repo — the only validation is a successful compile plus visual review of the rendered PDF.

## Iteration convention

When asked for a change: make the edit, then recompile immediately so the user can review the rendered PDF. Don't batch multiple unreviewed changes together before showing the result — one change, one compile, one look.

## Deliverable spec

- Single A0 portrait poster (841mm x 1189mm / 33.1in x 46.8in), LaTeX + `tikzposter`, compiled to one PDF.
- **Raster images must be 300dpi+ at their placed size on the A0 canvas** — not native dpi, but dpi as actually rendered at the size it's placed. Prefer vector PDF/SVG figures over raster wherever the pipeline repo's source allows it, since vector sidesteps the dpi requirement entirely.
### TODO before finalizing

**Figures** — the remaining raster figures in the poster are at a resolution that will visibly pixelate at A0 print size. Re-export each from its source as vector (SVG or vector PDF), or failing that as raster at 300dpi+ measured at its placed size, and swap it in before the poster is considered final.

1. **Pipeline schematic** (`figures/protein-varient-scoring.png`, Methodology block) — rebuild it: drop the first stage, and widen the remaining stages so the diagram spans the full width of its column instead of sitting at `0.645\linewidth`. Re-render in a non-pixelating format. Highest priority.
2. **Results figure** (Band 2, currently the `\figplaceholder[28cm]` stub) — drop in the real marginal-value plot once data lands, as vector or 300dpi+ raster, sized to the slot per the layout TODO below.
3. ~~**Growth chart** (`figures/uniref100_growth.pdf`, Background & Motivation block)~~ — **DONE.** Regenerated as a true vector PDF (embedded fonts, no raster) from `data/uniref_archive_growth.csv`.

**Layout** — the interpretation and implications content does not all fit at a legible size in the current three-band grid: Band 2's right column ("What the curve shows") plus the full Band 3 row (Policy Relevance, Limitations, Acknowledgements & Contact). Consolidate — merge or cut sections, tighten bullets, or restructure the bands — so everything fits without shrinking body text below the size used elsewhere on the poster.
- Minimize AI use across the poster as a whole, per organizer spec. The organizer's wording: *"Minimise using AI for the whole poster — our printers will not be able to produce a high enough quality poster if you do!"* Read this primarily as a print-quality constraint: AI-generated images, illustrations, icons, or whole-poster layouts tend to be raster and will not hold up at A0 print size, so don't produce them. It is also a content constraint: no AI-written filler passed off as findings.
- Individual plots built from the user's real data are fine. Claude assisting with LaTeX layout, typesetting, prose editing, and plotting user-supplied data is fine; Claude inventing scientific content or illustrations is not.

## Structure / style

- Visual style should take inspiration from the reference posters in `references/` (Andy, Perla, Zuzanna) — dark header bar, colored section-header bars, 2-3 column grid, ERA/CBH logo placement in top corners.
- `docs/` contains the project's midterm writeup, which can be treated as a reference for background/methodology content and framing — but it is source material to draw from, not text to copy in verbatim. It does not substitute for the user supplying actual poster prose (see below).
- Poster sections: Background/Motivation, Research Question/Methodology, Results, Policy Relevance, Limitations, Acknowledgements/Contact.
- The Results section is placeholder content until final data lands. If the alignment-selection/PSSM diagnosis isn't resolved by the time this section is filled in, mark it clearly as **PRELIMINARY**.
- Rendered figures belong in `figures/`; their source data belongs in `data/`.

**All prose (section text, findings, captions, any scientific claims) must come from the user, not from Claude.** Claude may edit for grammar, tighten wording, or adjust for layout/space constraints, but must not originate or invent substantive content — including placeholder filler standing in for real findings. If a section's prose hasn't been supplied yet, leave it explicitly marked as a placeholder (e.g. `[PROSE NEEDED]`) rather than filling it in.

## Git

Standard commits; no special branch conventions, since this repo is scoped entirely to poster work.
