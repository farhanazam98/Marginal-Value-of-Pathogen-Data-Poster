#!/usr/bin/env python3
"""Preliminary-results figure for the poster's Band 2.

Plots PSSM-vs-DMS Spearman's rho against UniRef100 snapshot year for all
three DMS assays on one figure, per the mentor's suggestion:

  * protease  -- flynn_fitness      (main protease, fitness assay)
  * spike     -- starr_binding      (RBD, ACE2 binding)
  * spike     -- starr_expression   (RBD, expression)

All series use bitscore_per_residue = 0.1, matching the hardcoded value
stated in the poster's Limitations block (no alignment-selection heuristic
applied yet -- results are PRELIMINARY).

Data: data/sweep_results.csv (real pipeline output, supplied by the user).
Outputs (true vector PDF, embedded fonts, no raster):
  * figures/pssm_accuracy_three_assays_overlay.pdf   -- single shared-axis panel
  * figures/pssm_accuracy_three_assays_panels.pdf    -- 3 small multiples, shared axes
"""

import csv
import pathlib

import matplotlib as mpl

mpl.use("pdf")
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "pdf.fonttype": 42,          # embed TrueType, keep text as text (vector)
    "ps.fonttype": 42,
    "svg.fonttype": "none",
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "axes.linewidth": 0.9,
    "axes.edgecolor": "#3a3a3a",
})

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "sweep_results.csv"
FIGDIR = ROOT / "figures"

BITSCORE = "0.1"

# assay key -> (display label, colour).  Okabe-Ito, colour-blind safe.
ASSAYS = [
    ("flynn_fitness",    "protease · fitness",       "#0072B2"),
    ("starr_expression", "spike RBD · expression",   "#009E73"),
    ("starr_binding",    "spike RBD · ACE2 binding", "#D55E00"),
]


def load():
    series = {k: [] for k, _, _ in ASSAYS}
    with open(DATA, newline="") as fh:
        for r in csv.DictReader(fh):
            if r["bitscore_per_residue"] != BITSCORE:
                continue
            key = r["dms_id"]
            if key not in series:
                continue
            series[key].append((
                int(r["year"]),
                float(r["spearman_rho"]),
                float(r["bootstrap_ci_95_lo"]),
                float(r["bootstrap_ci_95_hi"]),
            ))
    for k in series:
        series[k].sort()
    return series


def unpack(rows):
    yr = [d[0] for d in rows]
    rho = [d[1] for d in rows]
    lo = [d[2] for d in rows]
    hi = [d[3] for d in rows]
    return yr, rho, lo, hi


def style_axes(ax, years, xpad_right=0.6, xticks=None):
    ax.set_xlim(min(years) - 0.6, max(years) + xpad_right)
    ticks = xticks if xticks is not None else years
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(y) for y in ticks], rotation=45, ha="right")
    ax.yaxis.grid(True, color="#d7d7d7", linewidth=0.7)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def make_overlay(series):
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    all_years = sorted({d[0] for rows in series.values() for d in rows})

    for key, label, colour in ASSAYS:
        yr, rho, lo, hi = unpack(series[key])
        ax.fill_between(yr, lo, hi, color=colour, alpha=0.15, linewidth=0)
        ax.plot(yr, rho, "-o", color=colour, lw=2.4, ms=6.5,
                mec="white", mew=0.8, label=label, zorder=3)
        ax.annotate(label, xy=(yr[-1], rho[-1]), xytext=(8, 0),
                    textcoords="offset points", va="center", ha="left",
                    fontsize=12.5, fontweight="bold", color=colour)

    style_axes(ax, all_years, xpad_right=5.5)  # headroom for right-hand labels
    ax.set_ylim(0.0, 0.62)
    ax.set_xlabel("UniRef100 snapshot year", fontsize=13)
    ax.set_ylabel("Spearman's ρ  (PSSM vs. DMS)", fontsize=13)
    ax.tick_params(labelsize=11)
    fig.tight_layout()
    out = FIGDIR / "pssm_accuracy_three_assays_overlay.pdf"
    fig.savefig(out)
    plt.close(fig)
    return out


def make_panels(series):
    # Independent y-axis per panel: the three assays span very different rho
    # ranges, so a shared axis would flatten the two spike trends to a
    # near-flat line.  The overlay figure carries the shared-scale comparison;
    # this one is for reading the shape of each individual trend.
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 5.0))
    all_years = sorted({d[0] for rows in series.values() for d in rows})
    xticks = [y for y in all_years if y % 2 == 0]

    for ax, (key, label, colour) in zip(axes, ASSAYS):
        yr, rho, lo, hi = unpack(series[key])
        ax.fill_between(yr, lo, hi, color=colour, alpha=0.18, linewidth=0)
        ax.plot(yr, rho, "-o", color=colour, lw=2.4, ms=6, mec="white", mew=0.8)
        style_axes(ax, all_years, xticks=xticks)
        span = max(hi) - min(lo)
        ax.set_ylim(min(lo) - 0.15 * span, max(hi) + 0.15 * span)
        ax.set_title(label, fontsize=13, fontweight="bold", color=colour, pad=8)
        ax.set_xlabel("snapshot year", fontsize=11.5)
        ax.tick_params(labelsize=9.5)
        ax.set_ylabel("Spearman's ρ  (PSSM vs. DMS)", fontsize=11.5)

    fig.tight_layout()
    out = FIGDIR / "pssm_accuracy_three_assays_panels.pdf"
    fig.savefig(out)
    plt.close(fig)
    return out


if __name__ == "__main__":
    s = load()
    for k, _, _ in ASSAYS:
        print(f"{k:18s} {len(s[k])} years  "
              f"rho {min(d[1] for d in s[k]):.3f}..{max(d[1] for d in s[k]):.3f}")
    print("wrote", make_overlay(s))
    print("wrote", make_panels(s))
