#!/usr/bin/env python
"""Fig 2 (provisional): spin-resolved TB band structure of the h-CrN monolayer.

Run with the Kwant venv:  ~/venvs/crn-te/bin/python scripts/fig2_monolayer_bands.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crnte.monolayer import MonolayerParams, bands_along_path  # noqa: E402

FIGDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(FIGDIR, exist_ok=True)

# High-symmetry path in fractional (b1, b2) coordinates: Gamma -> M -> K -> Gamma
FRAC = [(0.0, 0.0), (0.5, 0.0), (2.0 / 3, 1.0 / 3), (0.0, 0.0)]
LABELS = [r"$\Gamma$", "M", "K", r"$\Gamma$"]


def main():
    p = MonolayerParams()
    fig, ax = plt.subplots(figsize=(5.2, 4.2))

    styles = {+1: dict(color="C3", label=r"majority ($\uparrow$)"),
              -1: dict(color="C0", label=r"minority ($\downarrow$)", ls="--")}
    ticks = None
    for spin in (+1, -1):
        x, e, ticks, labels = bands_along_path(FRAC, LABELS, p, spin)
        e = e - p.E_fermi  # shift so E_F = 0
        for band in range(e.shape[1]):
            ax.plot(x, e[:, band], lw=1.8,
                    **({k: v for k, v in styles[spin].items()} if band == 0
                       else {k: v for k, v in styles[spin].items() if k != "label"}))

    ax.axhline(0.0, color="k", lw=0.7, ls=":")
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)
    for t in ticks:
        ax.axvline(t, color="0.85", lw=0.6, zorder=0)
    ax.set_xlim(ticks[0], ticks[-1])
    ax.set_ylabel(r"$E - E_F$ (eV)")
    ax.set_title("h-CrN monolayer — provisional TB bands (Dirac half-metal)")
    ax.legend(frameon=False, fontsize=9, loc="upper right")

    gap = _minority_gap(p)
    ax.text(0.02, 0.02, f"minority gap $\\approx$ {gap:.1f} eV", transform=ax.transAxes,
            fontsize=8, color="C0")

    out = os.path.join(FIGDIR, "fig2_monolayer_bands.png")
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    print(f"lattice constant a = {p.a:.3f} Angstrom")
    print(f"minority (spin-down) gap = {gap:.2f} eV  (target ~4 eV)")
    print(f"wrote {out}")


def _minority_gap(p):
    """Direct gap of the minority channel, scanned over the k-path."""
    _, e, _, _ = bands_along_path(FRAC, LABELS, p, spin=-1)
    return float((e[:, 1] - e[:, 0]).min())


if __name__ == "__main__":
    main()
