#!/usr/bin/env python
"""Fig 1: geometry of hexagonal CrN and its nanoribbons.

(a) h-CrN monolayer honeycomb (Cr + N sublattices, lattice vectors, unit cell).
(b) Zigzag ribbon (ZCNR): horizontal (transport along x), magnetic edges.
(c) Armchair ribbon (ACNR): horizontal (transport along x).
Pure matplotlib schematic (no Kwant); publication style.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrow, Polygon

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

CR_COLOR = "#3b6fb0"
N_COLOR = "#c7ccd1"
BOND_COLOR = "#606060"


def _rot(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]])


def honeycomb(theta=0.0):
    R = _rot(theta)
    cr, nn = [], []
    for n in range(-16, 20):
        for m in range(-20, 18):
            base = n * A1 + m * A2
            cr.append(R @ base)
            nn.append(R @ (base + DELTAS[0]))
    return np.array(cr), np.array(nn)


def _in(p, xl, yl, pad=0.05):
    return xl[0] - pad <= p[0] <= xl[1] + pad and yl[0] - pad <= p[1] <= yl[1] + pad


def draw(ax, xl, yl, theta=0.0, both_inside_bonds=True, s=150):
    cr, nn = honeycomb(theta)
    Rd = [_rot(theta) @ dv for dv in DELTAS]
    for a in cr:
        for dv in Rd:
            b = a + dv
            ain, bin_ = _in(a, xl, yl), _in(b, xl, yl)
            if (ain and bin_) if both_inside_bonds else (ain or bin_):
                ax.plot([a[0], b[0]], [a[1], b[1]], color=BOND_COLOR, lw=1.6, zorder=1)
    crin = np.array([p for p in cr if _in(p, xl, yl)])
    nnin = np.array([p for p in nn if _in(p, xl, yl)])
    if len(crin):
        ax.scatter(crin[:, 0], crin[:, 1], s=s, color=CR_COLOR, edgecolors="k", lw=0.7, zorder=3)
    if len(nnin):
        ax.scatter(nnin[:, 0], nnin[:, 1], s=s * 0.62, color=N_COLOR, edgecolors="k",
                   lw=0.7, zorder=3)
    return crin, nnin


def panel_monolayer(ax):
    xl, yl = (-0.6, 7.0), (-3.2, 3.2)
    draw(ax, xl, yl, both_inside_bonds=False)
    o = np.array([0.0, 0.0])
    for v, lab in ((A1, r"$\mathbf{a}_1$"), (A2, r"$\mathbf{a}_2$")):
        ax.add_patch(FancyArrow(o[0], o[1], v[0], v[1], width=0.03, head_width=0.24,
                                length_includes_head=True, color="C3", zorder=4))
        ax.text(v[0] * 1.02 + 0.1, v[1] * 1.02 + (0.2 if v[1] > 0 else -0.35), lab,
                color="C3", fontsize=13)
    ax.add_patch(Polygon([o, A1, A1 + A2, A2], closed=True, fill=False, ec="C3", ls="--", lw=1.3))
    ax.scatter([], [], s=150, color=CR_COLOR, edgecolors="k", label="Cr")
    ax.scatter([], [], s=95, color=N_COLOR, edgecolors="k", label="N")
    ax.legend(loc="upper right", frameon=True, fontsize=11)
    ax.set_title("(a) h-CrN monolayer", fontsize=13)
    ax.set_xlim(*xl)
    ax.set_ylim(*yl)


def panel_zigzag(ax):
    # theta=0: horizontal cuts are zigzag edges. Wide (periodic x), a few rows tall.
    xl, yl = (0.4, 11.5), (-0.2, 6.7)
    crin, _ = draw(ax, xl, yl, theta=0.0)
    ytop, ybot = crin[:, 1].max(), crin[:, 1].min()
    for p in crin[np.abs(crin[:, 1] - ytop) < 0.1]:
        ax.add_patch(FancyArrow(p[0], p[1] + 0.12, 0, 0.62, width=0.045, head_width=0.2,
                                length_includes_head=True, color="C3", zorder=5))
    for p in crin[np.abs(crin[:, 1] - ybot) < 0.1]:
        ax.add_patch(FancyArrow(p[0], p[1] - 0.78, 0, 0.62, width=0.045, head_width=0.2,
                                length_includes_head=True, color="C3", zorder=5))
    ax.annotate("", xy=(11.7, ybot), xytext=(11.7, ytop),
                arrowprops=dict(arrowstyle="<->", color="k"))
    ax.text(12.0, (ytop + ybot) / 2, r"width $N$", rotation=90, va="center", fontsize=11)
    ax.text((xl[0] + xl[1]) / 2, ytop + 1.05, "ferromagnetic Cr edge moments",
            color="C3", fontsize=9.5, ha="center")
    ax.annotate("", xy=(1.0, ybot - 0.95), xytext=(9.5, ybot - 0.95),
                arrowprops=dict(arrowstyle="<->", color="0.4"))
    ax.text(5.2, ybot - 1.35, "periodic (transport)", color="0.4", fontsize=9, ha="center")
    ax.set_title("(b) Zigzag ribbon (ZCNR)", fontsize=13)
    ax.set_xlim(xl[0] - 0.3, xl[1] + 1.3)
    ax.set_ylim(ybot - 1.8, ytop + 1.6)


def panel_armchair(ax):
    # theta=90 deg: horizontal cuts are armchair edges. Wide (periodic x), a few rows tall.
    xl, yl = (0.4, 11.5), (0.2, 6.4)
    crin, _ = draw(ax, xl, yl, theta=np.pi / 2)
    ytop, ybot = crin[:, 1].max(), crin[:, 1].min()
    ax.annotate("", xy=(11.7, ybot), xytext=(11.7, ytop),
                arrowprops=dict(arrowstyle="<->", color="k"))
    ax.text(12.0, (ytop + ybot) / 2, r"width $N$", rotation=90, va="center", fontsize=11)
    ax.annotate("", xy=(1.0, ybot - 0.75), xytext=(9.5, ybot - 0.75),
                arrowprops=dict(arrowstyle="<->", color="0.4"))
    ax.text(5.2, ybot - 1.15, "periodic (transport)", color="0.4", fontsize=9, ha="center")
    ax.set_title("(c) Armchair ribbon (ACNR)", fontsize=13)
    ax.set_xlim(xl[0] - 0.3, xl[1] + 1.3)
    ax.set_ylim(ybot - 1.6, ytop + 0.8)


def main():
    fig = plt.figure(figsize=(13, 8.6))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1.55])
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, :])
    panel_monolayer(ax_a)
    panel_zigzag(ax_b)
    panel_armchair(ax_c)
    for ax in (ax_a, ax_b, ax_c):
        ax.set_aspect("equal")
        ax.axis("off")
    fig.tight_layout()
    out = os.path.join(FIGDIR, "fig1_geometry.png")
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
