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
- Minimize AI-generated content per organizer spec: no AI-generated images/illustrations/icons, no AI-written filler passed off as findings. Figures must be real pipeline output copied in as static files — never fabricated or regenerated. Claude assisting with LaTeX layout, typesetting, and prose editing is fine; Claude inventing scientific content or illustrations is not.

## Structure / style

- Visual style should take inspiration from the reference posters in `references/` (Andy, Perla, Zuzanna) — dark header bar, colored section-header bars, 2-3 column grid, ERA/CBH logo placement in top corners.
- Poster sections: Background/Motivation, Research Question/Methodology, Results, Policy Relevance, Limitations, Acknowledgements/Contact.
- The Results section is placeholder content until final data lands. If the alignment-selection/PSSM diagnosis isn't resolved by the time this section is filled in, mark it clearly as **PRELIMINARY**.
- Figures belong in `figures/`, copied in manually — never authored or generated in this repo.

## Git

Standard commits; no special branch conventions, since this repo is scoped entirely to poster work.
