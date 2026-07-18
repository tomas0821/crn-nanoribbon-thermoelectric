#!/usr/bin/env python
"""Orbital-manifold caution figure: reduced (d+p_z) vs extended (+ conduction pocket) model.

The reduced out-of-plane manifold -- the natural minimal choice near E_F -- MISSES the majority
conduction band (electron pocket at K) of the DFT reference. That omission fabricates a sharp
majority transmission edge just above E_F and hence a spurious ZT ~ 0.2; restoring the pocket
(one effective orbital fitted to the digitized DFT band) removes the edge and collapses the
thermopower. This figure quantifies the artifact.

(a) majority T(E): reduced vs extended model (zigzag N=14).
(b) resulting ZT(mu) at 300 K on the same phonon background.

Run:  ~/venvs/crn-te/bin/python scripts/fig_manifold_comparison.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from crnte import thermo as th  # noqa: E402
from crnte.monolayer_sk import SKParams  # noqa: E402
from crnte.phonon import kappa_ph, ribbon_width  # noqa: E402

FIGDIR, DATADIR = os.path.join(ROOT, "figures"), os.path.join(ROOT, "data")
MU = np.linspace(-0.6, 1.2, 361)
T0 = 300.0


def main():
    p = SKParams()
    full = np.load(os.path.join(DATADIR, "zigzag_N14_TE.npz"))
    red = np.load(os.path.join(DATADIR, "zigzag_N14_TE_noc.npz"))
    W = ribbon_width("zigzag", 14, p.a)
    kph = kappa_ph(T0, W)

    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.8))

    axs[0].plot(red["E"], red["T_up"], color="C3", lw=1.6, ls="--",
                label="reduced manifold (no pocket)")
    axs[0].plot(full["E"], full["T_up"], color="C0", lw=1.6,
                label="extended (with K pocket)")
    axs[0].axvline(0, color="0.7", lw=0.6, ls=":")
    axs[0].set_xlim(-0.8, 1.2)
    axs[0].set_xlabel(r"$E - E_F$ (eV)")
    axs[0].set_ylabel(r"majority $T_\uparrow(E)$")
    axs[0].set_title("(a) majority transmission (zigzag N=14)")
    axs[0].legend(frameon=False, fontsize=8.5)

    for d, col, ls, lab in ((red, "C3", "--", "reduced manifold"),
                            (full, "C0", "-", "extended model")):
        up = th.sweep_mu(d["E"], d["T_up"], MU, T0)
        dn = th.sweep_mu(d["E"], d["T_dn"], MU, T0)
        tot = th.combine_spins(up, dn, T0)
        zt = th.ZT(tot, T0, kph)
        axs[1].plot(MU, zt, color=col, ls=ls, lw=1.8, label=lab)
        i = int(np.argmax(zt))
        print(f"{lab:18s}: peak ZT(300K) = {zt[i]:.4f} at mu-E_F = {MU[i]:+.2f} eV")
    axs[1].axvline(0, color="0.7", lw=0.6, ls=":")
    axs[1].set_xlabel(r"$\mu - E_F$ (eV)")
    axs[1].set_ylabel(r"$ZT$ (300 K)")
    axs[1].set_title("(b) resulting ZT — same $\\kappa_{ph}$")
    axs[1].legend(frameon=False, fontsize=8.5)

    fig.tight_layout()
    out = os.path.join(FIGDIR, "fig_manifold.png")
    fig.savefig(out, dpi=200)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
