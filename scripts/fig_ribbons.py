#!/usr/bin/env python
"""Intro figure: the hexagonal CrN nanoribbons we compute (zigzag + armchair).

Clean rectangular strips rendered from the honeycomb lattice (same geometry as the transport
calculations), with Cr/N sublattices, ferromagnetic edge moments, semi-infinite leads and the
transport direction. Designed as an inviting overview figure for the introduction.
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
FIGDIR = os.path.join(ROOT, "figures")
os.makedirs(FIGDIR, exist_ok=True)

A = 3.258
D = A / np.sqrt(3.0)
A1 = D * np.array([1.5, np.sqrt(3.0) / 2])
A2 = D * np.array([1.5, -np.sqrt(3.0) / 2])
DELTAS = [D * np.array([1.0, 0.0]),
          D * np.array([-0.5, np.sqrt(3.0) / 2]),
          D * np.array([-0.5, -np.sqrt(3.0) / 2])]

CR_COLOR = "#2f6fb3"
N_COLOR = "#d3d7db"
BOND_COLOR = "#5b5b5b"
MOM_COLOR = "#c0392b"


def _rot(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]])


def honeycomb(theta=0.0):
    R = _rot(theta)
    cr, nn = [], []
    for n in range(-22, 26):
        for m in range(-26, 24):
            base = n * A1 + m * A2
            cr.append(R @ base)
            nn.append(R @ (base + DELTAS[0]))
    return np.array(cr), np.array(nn)


def _crop(pts, xl, yl, pad=0.05):
    m = ((pts[:, 0] >= xl[0] - pad) & (pts[:, 0] <= xl[1] + pad) &
         (pts[:, 1] >= yl[0] - pad) & (pts[:, 1] <= yl[1] + pad))
    return pts[m]


def draw_ribbon(ax, theta, xl, yl, title):
    cr, nn = honeycomb(theta)
    crc, nnc = _crop(cr, xl, yl), _crop(nn, xl, yl)
    # bonds (both ends inside -> clean terminated edges)
    for a in crc:
        d = np.linalg.norm(nnc - a, axis=1)
        for b in nnc[d < 1.15 * D]:
            ax.plot([a[0], b[0]], [a[1], b[1]], color=BOND_COLOR, lw=1.5, zorder=2)
    # semi-infinite leads: faded ghost repeats of the end columns
    span = xl[1] - xl[0]
    for side, xedge in ((-1, xl[0]), (+1, xl[1])):
        col_c = crc[np.abs(crc[:, 0] - xedge) < 1.7 * D]
        col_n = nnc[np.abs(nnc[:, 0] - xedge) < 1.7 * D]
        for k, al in ((1, 0.5), (2, 0.28), (3, 0.13)):
            sh = np.array([side * k * 3.0 * D, 0.0])
            ax.scatter(*(col_n + sh).T, s=60, color=N_COLOR, edgecolors="none", alpha=al, zorder=1)
            ax.scatter(*(col_c + sh).T, s=100, color=CR_COLOR, edgecolors="none", alpha=al, zorder=1)
        ax.text(xedge + side * 3.1 * D, (yl[0] + yl[1]) / 2, "semi-infinite\nlead", fontsize=8.5,
                color="0.45", ha="center", va="center")
    # atoms
    ax.scatter(nnc[:, 0], nnc[:, 1], s=80, color=N_COLOR, edgecolors="k", lw=0.5, zorder=3)
    ax.scatter(crc[:, 0], crc[:, 1], s=125, color=CR_COLOR, edgecolors="k", lw=0.6, zorder=4)
    # ferromagnetic edge moments on top & bottom edge Cr
    ytop, ybot = crc[:, 1].max(), crc[:, 1].min()
    for p in crc[np.abs(crc[:, 1] - ytop) < 0.1]:
        ax.add_patch(FancyArrowPatch((p[0], p[1] + 0.2 * D), (p[0], p[1] + 1.15 * D),
                                     arrowstyle="-|>", mutation_scale=11, color=MOM_COLOR, lw=1.8))
    for p in crc[np.abs(crc[:, 1] - ybot) < 0.1]:
        ax.add_patch(FancyArrowPatch((p[0], p[1] - 1.15 * D), (p[0], p[1] - 0.2 * D),
                                     arrowstyle="-|>", mutation_scale=11, color=MOM_COLOR, lw=1.8))
    # transport arrow + width bracket
    yb = ybot - 2.1 * D
    ax.add_patch(FancyArrowPatch((xl[0], yb), (xl[1], yb), arrowstyle="<->",
                                 mutation_scale=16, color="0.3", lw=1.4))
    ax.text((xl[0] + xl[1]) / 2, yb - 0.8 * D, "transport (periodic)", fontsize=9.5,
            color="0.3", ha="center", va="top")
    xr = xl[1] + 4.4 * D
    ax.annotate("", xy=(xr, ybot), xytext=(xr, ytop), arrowprops=dict(arrowstyle="<->", color="k"))
    ax.text(xr + 0.6 * D, (ytop + ybot) / 2, "width $N$", rotation=90, va="center", fontsize=11)
    ax.set_title(title, fontsize=14, pad=12)
    ax.set_xlim(xl[0] - 4.5 * D, xr + 1.6 * D)
    ax.set_ylim(yb - 1.9 * D, ytop + 2.0 * D)
    ax.set_aspect("equal")
    ax.axis("off")


def main():
    fig, axes = plt.subplots(2, 1, figsize=(9.5, 8.2))
    draw_ribbon(axes[0], 0.0, (0.0, 22.0), (0.0, 11.5), "(a) Zigzag CrN nanoribbon (ZCNR)")
    draw_ribbon(axes[1], np.pi / 2, (0.0, 22.0), (0.0, 10.5), "(b) Armchair CrN nanoribbon (ACNR)")
    h_cr = axes[0].scatter([], [], s=125, color=CR_COLOR, edgecolors="k", label="Cr")
    h_n = axes[0].scatter([], [], s=80, color=N_COLOR, edgecolors="k", label="N")
    h_m, = axes[0].plot([], [], color=MOM_COLOR, lw=1.8, label="FM Cr edge moment")
    fig.legend(handles=[h_cr, h_n, h_m], loc="upper center", frameon=True, fontsize=10,
               ncol=3, bbox_to_anchor=(0.5, 1.005))
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out = os.path.join(FIGDIR, "fig_ribbons.png")
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
