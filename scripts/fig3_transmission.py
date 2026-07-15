#!/usr/bin/env python
"""Fig 3 (provisional): spin-resolved Landauer transmission T(E) of CrN nanoribbons.

Shows the half-metallic transport window: the minority channel is gapped (~3.9 eV) while the
majority channel conducts -> 100% spin-polarized current, the input to the thermoelectric
integrals (Figs 4-5). Provisional effective model; refine with the multi-orbital fit.

Run:  ~/venvs/crn-te/bin/python scripts/fig3_transmission.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crnte.monolayer import MonolayerParams  # noqa: E402
from crnte.ribbon import build_ribbon, transmission  # noqa: E402

FIGDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(FIGDIR, exist_ok=True)

WIDTH = 14           # ribbon width (# atom rows across); one of the DMRG primary widths
ENERGIES = np.linspace(-2.5, 2.5, 251)


def main():
    p = MonolayerParams()
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8), sharey=True)

    for ax, edge in zip(axes, ("zigzag", "armchair")):
        for spin, style in ((+1, dict(color="C3", label=r"majority $\uparrow$")),
                            (-1, dict(color="C0", ls="--", label=r"minority $\downarrow$"))):
            syst = build_ribbon(edge, WIDTH, p, spin)
            T = transmission(syst, ENERGIES)
            ax.plot(ENERGIES, T, lw=1.6, **style)
        ax.axvline(0.0, color="k", lw=0.7, ls=":")
        ax.set_title(f"{edge} CrN ribbon (N$\\approx${WIDTH})")
        ax.set_xlabel(r"$E - E_F$ (eV)")
        ax.set_xlim(ENERGIES[0], ENERGIES[-1])
        ax.grid(alpha=0.25)
    axes[0].set_ylabel(r"transmission $T(E)$")
    axes[0].legend(frameon=False, fontsize=9, loc="upper center")

    out = os.path.join(FIGDIR, "fig3_transmission.png")
    fig.suptitle("Spin-resolved Landauer transmission — provisional model", fontsize=11)
    fig.tight_layout()
    fig.savefig(out, dpi=200)

    # report the minority transport gap (window of zero transmission around E_F)
    syst = build_ribbon("zigzag", WIDTH, p, spin=-1)
    Tmin = transmission(syst, ENERGIES)
    zero = ENERGIES[Tmin < 1e-6]
    if zero.size:
        print(f"minority zero-T window: [{zero.min():+.2f}, {zero.max():+.2f}] eV "
              f"(width {zero.max() - zero.min():.1f} eV)")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
