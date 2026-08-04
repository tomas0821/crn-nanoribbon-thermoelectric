#!/usr/bin/env python
"""Figure: the armchair N=8 ribbon — the geometry whose optimum lies INSIDE the fully
polarized window (referee round 1, major point 6: the flagship result must be inspectable).

(a) Spin-resolved transmission T_sigma(E).
(b) Seebeck S(mu) at 300 K.
(c) ZT(mu) at 300 K with the kappa_ph bracket; polarized window (T_dn = 0) shaded.

Uses the cached fine transmission (data/armchair_N8_TE.npz).
Run:  ~/venvs/crn-te/bin/python scripts/fig_armchair8.py
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
T_K = 300.0
MU = np.linspace(-0.6, 1.2, 361)
MIN_EDGE = 1.0     # minority conduction edge (eV): polarized window mu < MIN_EDGE


def main():
    p = SKParams()
    d = np.load(os.path.join(DATADIR, "armchair_N8_TE.npz"))
    E, Tu, Td = d["E"], d["T_up"], d["T_dn"]
    W = ribbon_width("armchair", 8, p.a)
    kph = kappa_ph(T_K, W)

    up = th.sweep_mu(E, Tu, MU, T_K)
    dn = th.sweep_mu(E, Td, MU, T_K)
    tot = th.combine_spins(up, dn, T_K)

    fig, axs = plt.subplots(1, 3, figsize=(11.4, 3.6))

    axs[0].plot(E, Tu, color="C3", lw=1.6, label=r"$T_\uparrow$ (majority)")
    axs[0].plot(E, Td, color="C0", lw=1.6, ls="--", label=r"$T_\downarrow$ (minority)")
    axs[0].set_xlabel(r"$E - E_F$ (eV)")
    axs[0].set_ylabel(r"transmission $T_\sigma(E)$")
    axs[0].set_title("(a) transmission")
    axs[0].axvline(0, color="0.8", lw=0.6, ls=":")
    axs[0].legend(frameon=False, fontsize=9)

    axs[1].plot(MU, tot["S"] * 1e6, color="C2", lw=1.8)
    axs[1].set_xlabel(r"$\mu - E_F$ (eV)")
    axs[1].set_ylabel(r"Seebeck $S$ ($\mu$V/K)")
    axs[1].set_title("(b) Seebeck (300 K)")
    axs[1].axhline(0, color="k", lw=0.6, ls=":")
    axs[1].axvline(0, color="0.8", lw=0.6, ls=":")

    for fac, col, lab in ((0.5, "C2", r"$0.5\,\kappa_{ph}$"),
                          (1.0, "C0", r"$\kappa_{ph}$"),
                          (2.0, "C3", r"$2\,\kappa_{ph}$")):
        axs[2].plot(MU, th.ZT(tot, T_K, fac * kph), color=col, lw=1.6, label=lab)
    axs[2].set_xlabel(r"$\mu - E_F$ (eV)")
    axs[2].set_ylabel(r"$ZT$")
    axs[2].set_title("(c) ZT (300 K)")
    axs[2].legend(frameon=False, fontsize=8, loc="upper left")

    for ax in (axs[1], axs[2]):
        ax.axvspan(MU[0], MIN_EDGE, color="C1", alpha=0.08)
        ax.axvline(MIN_EDGE, color="C1", lw=0.8, ls="--")
    axs[2].annotate("fully spin-polarized\nwindow ($T_\\downarrow=0$)",
                    xy=(0.15, 0.62), xycoords="axes fraction", fontsize=8, color="C1")

    zt = th.ZT(tot, T_K, kph)
    i = int(np.argmax(zt))
    axs[2].plot(MU[i], zt[i], "k*", ms=10)
    print(f"peak ZT = {zt[i]:.4f} at mu-E_F = {MU[i]:+.2f} eV, S = {tot['S'][i]*1e6:+.1f} uV/K, "
          f"kph = {kph*1e9:.2f} nW/K")

    fig.tight_layout()
    out = os.path.join(FIGDIR, "fig_armchair8.png")
    fig.savefig(out, dpi=200)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
