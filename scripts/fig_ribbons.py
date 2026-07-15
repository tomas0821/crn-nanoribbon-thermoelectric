#!/usr/bin/env python
"""Intro figure: the hexagonal CrN nanoribbons we compute, at their true width N=14.

Rendered from the SAME honeycomb lattice and row convention as the transport code
(crnte.ribbon_sk): N = number of Cr+N atomic rows across the ribbon. Clean rectangular strips,
Cr/N sublattices, ferromagnetic edge moments, semi-infinite leads and transport direction.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from crnte.monolayer_sk import SKParams  # noqa: E402
from crnte.ribbon_sk import _transverse_bound  # noqa: E402

FIGDIR = os.path.join(ROOT, "figures")
os.makedirs(FIGDIR, exist_ok=True)

A = SKParams().a
D = A / np.sqrt(3.0)
PV0 = np.array([A, 0.0])
PV1 = np.array([A / 2.0, A * np.sqrt(3.0) / 2.0])
N_BASIS = np.array([0.0, D])
NROWS = 14

CR_COLOR = "#2f6fb3"
N_COLOR = "#d3d7db"
BOND_COLOR = "#5b5b5b"
MOM_COLOR = "#c0392b"


def _lattice_atoms(nmax=40):
    cr, nn = [], []
    for n in range(-nmax, nmax + 1):
        for m in range(-nmax, nmax + 1):
            base = n * PV0 + m * PV1
            cr.append(base)
            nn.append(base + N_BASIS)
    return np.array(cr), np.array(nn)


def ribbon_atoms(edge, n_rows, n_cells):
    """Clean rectangular ribbon: exactly n_rows across, n_cells along transport. Horizontal."""
    cr, nn = _lattice_atoms()
    lo, hi = _transverse_bound(edge, n_rows, A)
    if edge == "zigzag":               # transport x, transverse y
        long_hi = n_cells * A
        keep = lambda P: (lo <= P[:, 1]) & (P[:, 1] <= hi) & (P[:, 0] >= 0) & (P[:, 0] < long_hi)
        crk, nnk = cr[keep(cr)], nn[keep(nn)]
    else:                              # armchair: transport y, transverse x -> rotate to horizontal
        long_hi = n_cells * A * np.sqrt(3.0)
        keep = lambda P: (lo <= P[:, 0]) & (P[:, 0] <= hi) & (P[:, 1] >= 0) & (P[:, 1] < long_hi)
        crk, nnk = cr[keep(cr)], nn[keep(nn)]
        rot = np.array([[0.0, 1.0], [-1.0, 0.0]])       # rotate -90 deg -> transport along x
        crk, nnk = crk @ rot.T, nnk @ rot.T
    # recentre
    allp = np.vstack([crk, nnk])
    off = np.array([allp[:, 0].min(), (allp[:, 1].min() + allp[:, 1].max()) / 2])
    return crk - off, nnk - off


def draw(ax, crk, nnk, title):
    for a in crk:
        d = np.linalg.norm(nnk - a, axis=1)
        for b in nnk[d < 1.15 * D]:
            ax.plot([a[0], b[0]], [a[1], b[1]], color=BOND_COLOR, lw=1.5, zorder=2)
    xmin, xmax = crk[:, 0].min(), crk[:, 0].max()
    ymin, ymax = min(crk[:, 1].min(), nnk[:, 1].min()), max(crk[:, 1].max(), nnk[:, 1].max())
    # semi-infinite leads: faded ghost repeats of the end columns
    for side, xe in ((-1, xmin), (+1, xmax)):
        cc = crk[np.abs(crk[:, 0] - xe) < 1.7 * D]
        cn = nnk[np.abs(nnk[:, 0] - xe) < 1.7 * D]
        for k, al in ((1, 0.5), (2, 0.28), (3, 0.13)):
            sh = np.array([side * k * 3.0 * D, 0.0])
            ax.scatter(*(cn + sh).T, s=55, color=N_COLOR, edgecolors="none", alpha=al, zorder=1)
            ax.scatter(*(cc + sh).T, s=95, color=CR_COLOR, edgecolors="none", alpha=al, zorder=1)
        ax.text(xe + side * 3.1 * D, (ymin + ymax) / 2, "semi-infinite\nlead", fontsize=8.5,
                color="0.45", ha="center", va="center")
    ax.scatter(nnk[:, 0], nnk[:, 1], s=70, color=N_COLOR, edgecolors="k", lw=0.5, zorder=3)
    ax.scatter(crk[:, 0], crk[:, 1], s=105, color=CR_COLOR, edgecolors="k", lw=0.6, zorder=4)
    # FM edge moments (all parallel, pointing up) on the outermost rows (top & bottom)
    for yt in (ymax, ymin):
        edge_atoms = np.vstack([crk, nnk])
        outer = edge_atoms[np.abs(edge_atoms[:, 1] - yt) < 0.1]
        for pt in outer[::2]:
            y0 = pt[1] + 0.35 * D if yt == ymax else pt[1] - 1.35 * D
            ax.add_patch(FancyArrowPatch((pt[0], y0), (pt[0], y0 + 1.0 * D),
                                         arrowstyle="-|>", mutation_scale=10, color=MOM_COLOR, lw=1.7))
    yb = ymin - 2.2 * D
    ax.add_patch(FancyArrowPatch((xmin, yb), (xmax, yb), arrowstyle="<->",
                                 mutation_scale=16, color="0.3", lw=1.4))
    ax.text((xmin + xmax) / 2, yb - 0.9 * D, "transport (periodic)", fontsize=9.5,
            color="0.3", ha="center", va="top")
    xr = xmax + 4.6 * D
    ax.annotate("", xy=(xr, ymin), xytext=(xr, ymax), arrowprops=dict(arrowstyle="<->", color="k"))
    ax.text(xr + 0.7 * D, (ymin + ymax) / 2, f"$N={NROWS}$", rotation=90, va="center", fontsize=11)
    ax.set_title(title, fontsize=14, pad=10)
    ax.set_xlim(xmin - 4.7 * D, xr + 1.8 * D)
    ax.set_ylim(yb - 1.8 * D, ymax + 1.6 * D)
    ax.set_aspect("equal")
    ax.axis("off")


def main():
    fig, axes = plt.subplots(2, 1, figsize=(10, 9))
    crz, nnz = ribbon_atoms("zigzag", NROWS, n_cells=9)
    draw(axes[0], crz, nnz, "(a) Zigzag CrN nanoribbon (ZCNR)")
    cra, nna = ribbon_atoms("armchair", NROWS, n_cells=6)
    draw(axes[1], cra, nna, "(b) Armchair CrN nanoribbon (ACNR)")
    h_cr = axes[0].scatter([], [], s=105, color=CR_COLOR, edgecolors="k", label="Cr")
    h_n = axes[0].scatter([], [], s=70, color=N_COLOR, edgecolors="k", label="N")
    h_m, = axes[0].plot([], [], color=MOM_COLOR, lw=1.7, label="FM Cr edge moment")
    fig.legend(handles=[h_cr, h_n, h_m], loc="upper center", frameon=True, fontsize=10,
               ncol=3, bbox_to_anchor=(0.5, 1.005))
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out = os.path.join(FIGDIR, "fig_ribbons.png")
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"wrote {out} (zigzag {len(crz)+len(nnz)} atoms, armchair {len(cra)+len(nna)} atoms)")


if __name__ == "__main__":
    main()
