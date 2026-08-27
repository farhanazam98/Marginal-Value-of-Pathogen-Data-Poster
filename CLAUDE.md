# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A standalone repo containing only the LaTeX source for a single A0 research poster. It has no connection to the `marginal-value-pathogen-data-v1` pipeline repo — no pipeline code, data, or scripts live here, and nothing in this repo should ever reference a path into that other repo. Figures reach this repo only via manual copy-paste from the pipeline repo's output; Claude never generates, fetches, or regenerates figure data here.

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
- **TODO before finalizing: convert the current figures to SVG/vector.** The figures now in the poster are raster and will not meet the 300dpi rule at print size — re-export them as SVG (or vector PDF) from their source and swap them in before the poster is considered final:
  - `figures/protein-varient-scoring.png` — pipeline schematic, ~876px wide (~230dpi at placed size). Highest priority.
  - `figures/uniref100_growth.pdf` — growth chart; already vector PDF, but regenerate as SVG if a single vector format is wanted across all figures (matplotlib: `savefig(..., format="svg")`).
- Minimize AI-generated content per organizer spec: no AI-generated images/illustrations/icons, no AI-written filler passed off as findings. Figures must be real pipeline output copied in as static files — never fabricated or regenerated. Claude assisting with LaTeX layout, typesetting, and prose editing is fine; Claude inventing scientific content or illustrations is not.

## Structure / style

- Visual style should take inspiration from the reference posters in `references/` (Andy, Perla, Zuzanna) — dark header bar, colored section-header bars, 2-3 column grid, ERA/CBH logo placement in top corners.
- `docs/` contains the project's midterm writeup, which can be treated as a reference for background/methodology content and framing — but it is source material to draw from, not text to copy in verbatim. It does not substitute for the user supplying actual poster prose (see below).
- Poster sections: Background/Motivation, Research Question/Methodology, Results, Policy Relevance, Limitations, Acknowledgements/Contact.
- The Results section is placeholder content until final data lands. If the alignment-selection/PSSM diagnosis isn't resolved by the time this section is filled in, mark it clearly as **PRELIMINARY**.
- Figures belong in `figures/`, copied in manually — never authored or generated in this repo.

**All prose (section text, findings, captions, any scientific claims) must come from the user, not from Claude.** Claude may edit for grammar, tighten wording, or adjust for layout/space constraints, but must not originate or invent substantive content — including placeholder filler standing in for real findings. If a section's prose hasn't been supplied yet, leave it explicitly marked as a placeholder (e.g. `[PROSE NEEDED]`) rather than filling it in.

## Git

Standard commits; no special branch conventions, since this repo is scoped entirely to poster work.
