"""
Generate MOCK line-graph images at the exact sizes derived for the poster's
Results block (tikzposter, A0 portrait, 0.62 column, Basic block style).

  block body \\linewidth        = 471.3 mm = 18.55 in
  0.92*\\linewidth (figplaceholder) = 433.6 mm = 17.07 in
  author's combined figure slot  = 28.0 cm  (\\figplaceholder[28cm])
  even split, 2 graphs + captions = ~11.8 cm = 4.65 in image height each

These are LAYOUT TEST placeholders only. Fake data, watermarked. NOT pipeline
output. Do not copy into figures/ as if real.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["CMU Serif", "DejaVu Serif"],
    "font.size": 15,
    "axes.linewidth": 1.0,
    "pdf.fonttype": 42,
})

OUT = "/private/tmp/claude-501/-Users-farhanazam-repos-Marginal-Value-of-Pathogen-Data-Poster/c277775f-8ef3-44da-8f22-06c9f5ade72d/scratchpad"

LINEWIDTH_IN = 18.55        # full block-body \linewidth
PANEL_H_IN   = 4.65         # even-split height per graph inside 28 cm slot
REF_H_IN     = 11.6         # 1.6:1 "reference aspect" height at this width

years = np.arange(2010, 2027)

def mock_curve(seed, lo, hi, plateau_at=2019):
    rng = np.random.default_rng(seed)
    x = years - years.min()
    # rising-then-plateau shape, obviously synthetic
    base = lo + (hi - lo) * (1 - np.exp(-x / 4.5))
    base = np.where(years >= plateau_at, base[years == plateau_at][0]
                    + (base - base[years == plateau_at][0]) * 0.15, base)
    return base + rng.normal(0, (hi - lo) * 0.02, size=base.shape)

def watermark(ax):
    ax.text(0.5, 0.5, "MOCK  —  NOT REAL DATA", transform=ax.transAxes,
            fontsize=40, color="0.6", alpha=0.30, rotation=18,
            ha="center", va="center", zorder=5, fontweight="bold")

def style(ax, ylabel, title):
    ax.set_xlabel("UniRef100 snapshot year  (mock axis)")
    ax.set_ylabel(ylabel)
    ax.set_title(title, loc="left", fontsize=15, fontweight="bold")
    ax.set_xticks(years[::2])
    ax.set_xlim(years.min(), years.max())
    ax.grid(True, alpha=0.25, linewidth=0.6)
    ax.spines[["top", "right"]].set_visible(False)

# ---- 1. two separate wide-short panels (fits the 28 cm slot) -----------------
for tag, seed, lo, hi, lbl in [
    ("A", 1, 0.10, 0.46, "Spearman $\\rho$  (mock: RBD binding)"),
    ("B", 2, 0.05, 0.38, "Spearman $\\rho$  (mock: RBD expression)"),
]:
    fig, ax = plt.subplots(figsize=(LINEWIDTH_IN, PANEL_H_IN))
    ax.plot(years, mock_curve(seed, lo, hi), marker="o", lw=2.2, ms=6,
            color="#2A9D8F")
    style(ax, lbl, f"MOCK SLOT {tag}  —  layout test  —  {LINEWIDTH_IN}in x {PANEL_H_IN}in")
    watermark(ax)
    fig.tight_layout(pad=0.6)
    fig.savefig(f"{OUT}/mock_slot_{tag}.pdf")
    fig.savefig(f"{OUT}/mock_slot_{tag}.png", dpi=300)
    plt.close(fig)

# ---- 2. one file, two stacked subplots (drop in at width=\linewidth) ---------
fig, axes = plt.subplots(2, 1, figsize=(LINEWIDTH_IN, 2 * PANEL_H_IN))
for ax, (seed, lo, hi, lbl, ttl) in zip(axes, [
    (1, 0.10, 0.46, "Spearman $\\rho$  (mock: RBD binding)",     "MOCK  —  panel 1 of 2  (layout test)"),
    (2, 0.05, 0.38, "Spearman $\\rho$  (mock: RBD expression)",  "MOCK  —  panel 2 of 2  (layout test)"),
]):
    ax.plot(years, mock_curve(seed, lo, hi), marker="o", lw=2.2, ms=6, color="#2A9D8F")
    style(ax, lbl, ttl)
    watermark(ax)
fig.suptitle(f"MOCK stacked results  —  image {LINEWIDTH_IN}in x {2*PANEL_H_IN:.1f}in "
             f"(~{2*PANEL_H_IN*25.4:.0f} mm) + tikzfigure caption",
             fontsize=13, y=0.995)
fig.tight_layout(pad=0.6, rect=(0, 0, 1, 0.97))
fig.savefig(f"{OUT}/mock_results_stacked.pdf")
fig.savefig(f"{OUT}/mock_results_stacked.png", dpi=300)
plt.close(fig)

# ---- 3. reference-aspect version (1.6:1) to show it does NOT fit -------------
fig, axes = plt.subplots(2, 1, figsize=(LINEWIDTH_IN, 2 * REF_H_IN))
for ax, (seed, lo, hi, lbl) in zip(axes, [
    (1, 0.10, 0.46, "Spearman $\\rho$  (mock)"),
    (2, 0.05, 0.38, "Spearman $\\rho$  (mock)"),
]):
    ax.plot(years, mock_curve(seed, lo, hi), marker="o", lw=2.5, ms=8, color="#E76F51")
    style(ax, lbl, "MOCK  —  1.6:1 reference aspect  (TOO TALL for the 28 cm slot)")
    watermark(ax)
fig.suptitle(f"MOCK  —  reference-aspect stack: image {LINEWIDTH_IN}in x {2*REF_H_IN:.1f}in "
             f"(~{2*REF_H_IN*25.4:.0f} mm)  —  ~2x the author's 280 mm slot",
             fontsize=13, y=0.997)
fig.tight_layout(pad=0.6, rect=(0, 0, 1, 0.98))
fig.savefig(f"{OUT}/mock_reference_aspect.pdf")
fig.savefig(f"{OUT}/mock_reference_aspect.png", dpi=150)
plt.close(fig)

print("wrote:")
import os
for f in sorted(os.listdir(OUT)):
    if f.startswith("mock_"):
        print(f"  {f:32s} {os.path.getsize(os.path.join(OUT, f))/1024:8.1f} KB")
