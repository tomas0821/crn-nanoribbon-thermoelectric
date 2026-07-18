#!/usr/bin/env python
"""Fig 3 (SK model): spin-resolved Landauer transmission T(E) of CrN nanoribbons.

Faithful reduced-SK model (crnte.ribbon_sk). Shows the half-metallic transport window: the
minority channel is gapped across E_F while the majority conducts -> 100% spin-polarized current,
the input to the thermoelectric integrals (Figs 4-5).

Run:  ~/venvs/crn-te/bin/python scripts/fig3_sk_transmission.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crnte.monolayer_sk import SKParams  # noqa: E402
from crnte.ribbon_sk import build_ribbon_sk, transmission  # noqa: E402

FIGDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(FIGDIR, exist_ok=True)

WIDTH = 14                       # ribbon width (# atom rows across); a DMRG primary width
ENERGIES = np.linspace(-4.0, 3.0, 181)


def main():
    p = SKParams()
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8), sharey=True)

    DATADIR = os.path.join(os.path.dirname(FIGDIR), "data")
    wide = {}
    for ax, edge in zip(axes, ("zigzag", "armchair")):
        for spin, style in ((+1, dict(color="C3", label=r"majority $\uparrow$")),
                            (-1, dict(color="C0", ls="--", label=r"minority $\downarrow$"))):
            syst = build_ribbon_sk(edge, WIDTH, p, spin)
            T = transmission(syst, ENERGIES)
            wide[f"{edge}_{'up' if spin > 0 else 'dn'}"] = T
            ax.plot(ENERGIES, T, lw=1.5, **style)
        ax.axvline(0.0, color="k", lw=0.7, ls=":")
        ax.set_title(f"{edge} CrN ribbon (N={WIDTH})")
        ax.set_xlabel(r"$E - E_F$ (eV)")
        ax.set_xlim(ENERGIES[0], ENERGIES[-1])
        ax.grid(alpha=0.25)
    axes[0].set_ylabel(r"transmission $T(E)$")
    axes[0].legend(frameon=False, fontsize=9, loc="upper left")

    np.savez(os.path.join(os.path.dirname(FIGDIR), "data", "wide_window_T.npz"),
             E=ENERGIES, **wide)
    out = os.path.join(FIGDIR, "fig3_sk_transmission.png")
    fig.suptitle("Spin-resolved Landauer transmission — extended SK model", fontsize=11)
    fig.tight_layout()
    fig.savefig(out, dpi=200)

    syst = build_ribbon_sk("zigzag", WIDTH, p, spin=-1)
    Tmin = transmission(syst, ENERGIES)
    open_ = ENERGIES[Tmin > 1e-6]
    lo = open_[open_ < 0].max() if (open_ < 0).any() else ENERGIES[0]
    hi = open_[open_ > 0].min() if (open_ > 0).any() else ENERGIES[-1]
    print(f"zigzag minority transport gap around E_F: [{lo:+.2f}, {hi:+.2f}] eV "
          f"({hi - lo:.1f} eV wide); majority T(E_F)="
          f"{transmission(build_ribbon_sk('zigzag', WIDTH, p, +1), np.array([0.0]))[0]:.0f}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
