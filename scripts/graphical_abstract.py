#!/usr/bin/env python
"""Graphical abstract (Elsevier: >= 1328 x 531 px, readable at 5 x 13 cm).

(left)   zigzag CrN ribbon schematic with ferromagnetic edge moments;
(middle) spin-resolved transmission: the 4-eV minority gap -> 100% spin-polarized current;
(right)  the thermal spin valve: T_P vs T_AP = 0.

Run:  ~/venvs/crn-te/bin/python scripts/graphical_abstract.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrow

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

A = 3.258
D = A / np.sqrt(3.0)
A1 = D * np.array([1.5, np.sqrt(3.0) / 2])
A2 = D * np.array([1.5, -np.sqrt(3.0) / 2])
DELTA0 = D * np.array([1.0, 0.0])


def draw_ribbon(ax):
    cr, nn = [], []
    for n in range(-8, 12):
        for m in range(-12, 10):
            base = n * A1 + m * A2
            cr.append(base)
            nn.append(base + DELTA0)
    xl, yl = (0.3, 12.6), (-0.2, 5.3)
    inside = lambda p: xl[0] - .05 <= p[0] <= xl[1] + .05 and yl[0] - .05 <= p[1] <= yl[1] + .05
    for a0 in cr:
        for dv in (DELTA0, D * np.array([-0.5, np.sqrt(3) / 2]), D * np.array([-0.5, -np.sqrt(3) / 2])):
            b = a0 + dv
            if inside(a0) and inside(b):
                ax.plot([a0[0], b[0]], [a0[1], b[1]], color="#606060", lw=1.3, zorder=1)
    crin = np.array([p for p in cr if inside(p)])
    nnin = np.array([p for p in nn if inside(p)])
    ax.scatter(crin[:, 0], crin[:, 1], s=70, color="#3b6fb0", edgecolors="k", lw=.5, zorder=3)
    ax.scatter(nnin[:, 0], nnin[:, 1], s=42, color="#c7ccd1", edgecolors="k", lw=.5, zorder=3)
    ytop, ybot = crin[:, 1].max(), crin[:, 1].min()
    for p in crin[np.abs(crin[:, 1] - ytop) < .1]:
        ax.add_patch(FancyArrow(p[0], p[1] + .12, 0, .55, width=.05, head_width=.22,
                                length_includes_head=True, color="C3", zorder=5))
    for p in crin[np.abs(crin[:, 1] - ybot) < .1]:
        ax.add_patch(FancyArrow(p[0], p[1] - .70, 0, .55, width=.05, head_width=.22,
                                length_includes_head=True, color="C3", zorder=5))
    ax.set_title("h-CrN nanoribbon\nferromagnetic half-metallic edges", fontsize=11)
    ax.set_xlim(0, 13)
    ax.set_ylim(ybot - 1.2, ytop + 1.2)
    ax.set_aspect("equal")
    ax.axis("off")


def main():
    d = np.load(os.path.join(ROOT, "data", "zigzag_N14_TE.npz"))
    v = np.load(os.path.join(ROOT, "data", "zigzag_N14_valve.npz"))

    fig, axs = plt.subplots(1, 3, figsize=(13.28, 4.4), width_ratios=[1.25, 1, 1])
    draw_ribbon(axs[0])

    m = (d["E"] >= -1.2) & (d["E"] <= 1.0)
    axs[1].plot(d["E"][m], d["T_up"][m], color="C3", lw=1.8, label=r"majority $\uparrow$")
    axs[1].plot(d["E"][m], d["T_dn"][m], color="C0", lw=2.0, ls="--",
                label=r"minority $\downarrow$ = 0")
    axs[1].axvline(0, color="0.7", lw=.6, ls=":")
    axs[1].set_xlabel(r"$E-E_F$ (eV)")
    axs[1].set_ylabel(r"$T_\sigma(E)$")
    axs[1].set_title("100% spin-polarized transport\n(4 eV minority gap)", fontsize=11)
    axs[1].legend(frameon=False, fontsize=9, loc="upper left")

    axs[2].plot(d["E"][m], (d["T_up"] + d["T_dn"])[m], color="C0", lw=1.8, label="parallel")
    axs[2].plot(v["E"], v["T_up"] + v["T_dn"], color="C3", lw=2.4, ls="--",
                label="antiparallel: $T=0$")
    axs[2].axvline(0, color="0.7", lw=.6, ls=":")
    axs[2].set_xlabel(r"$E-E_F$ (eV)")
    axs[2].set_ylabel(r"$T_\uparrow+T_\downarrow$")
    axs[2].set_title("thermal spin valve\n(thermocurrent ON/OFF)", fontsize=11)
    axs[2].legend(frameon=False, fontsize=9, loc="upper left")

    fig.tight_layout()
    out = os.path.join(ROOT, "manuscript", "figures", "graphical_abstract.png")
    fig.savefig(out, dpi=125)
    fig.savefig(os.path.join(ROOT, "figures", "graphical_abstract.png"), dpi=125)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
