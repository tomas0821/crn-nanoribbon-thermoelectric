#!/usr/bin/env python
"""Numerical convergence demonstration for the thermoelectric results.

Two knobs that could bias the peak ZT (zigzag N=14, 300 K):
  (1) energy-grid spacing dE of T(E) feeding the Onsager integrals -- must resolve the Fermi
      window (~0.1 eV at 300 K) and the sharp band edge;
  (2) scattering-region length (# unit cells) -- for a pristine ballistic ribbon T(E) should be
      length-independent (a good self-consistency check).
Also checks a low-temperature case (100 K), where the narrow Fermi window is most demanding.

Run:  ~/venvs/crn-te/bin/python scripts/convergence.py
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
from crnte.ribbon_sk import build_ribbon_sk, transmission  # noqa: E402

FIGDIR = os.path.join(ROOT, "figures")
EMIN, EMAX = -0.6, 1.5
MU = np.linspace(-0.4, 1.2, 321)


W14 = ribbon_width("zigzag", 14, SKParams().a)


def peak_zt(E, Tu, Td, T_K):
    up = th.sweep_mu(E, Tu, MU, T_K)
    dn = th.sweep_mu(E, Td, MU, T_K)
    zt = th.ZT(th.combine_spins(up, dn, T_K), T_K, kappa_ph(T_K, W14))
    return float(zt.max())


def main():
    p = SKParams()

    # ---- (1) energy-grid spacing ----
    print("Convergence vs energy-grid spacing dE (zigzag N=14, length=2):")
    dEs = [0.02, 0.01, 0.005, 0.0025]
    zt300, zt100 = [], []
    for dE in dEs:
        n = int(round((EMAX - EMIN) / dE)) + 1
        E = np.linspace(EMIN, EMAX, n)
        Tu = transmission(build_ribbon_sk("zigzag", 14, p, +1), E)
        Td = transmission(build_ribbon_sk("zigzag", 14, p, -1), E)
        z3, z1 = peak_zt(E, Tu, Td, 300.0), peak_zt(E, Tu, Td, 100.0)
        zt300.append(z3); zt100.append(z1)
        print(f"  dE={dE:.4f} eV ({n:4d} pts):  peak ZT(300K)={z3:.4f}  peak ZT(100K)={z1:.4f}")

    # ---- (2) scattering-region length (pristine -> should be flat) ----
    print("\nConvergence vs scattering-region length (dE=0.005 eV, 300 K):")
    E = np.linspace(EMIN, EMAX, int(round((EMAX - EMIN) / 0.005)) + 1)
    lengths = [1, 2, 3, 4]
    ztL = []
    for L in lengths:
        Tu = transmission(build_ribbon_sk("zigzag", 14, p, +1, length=L), E)
        Td = transmission(build_ribbon_sk("zigzag", 14, p, -1, length=L), E)
        z = peak_zt(E, Tu, Td, 300.0)
        ztL.append(z)
        print(f"  length={L} cells:  peak ZT(300K)={z:.4f}")

    # ---- plot ----
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
    ax[0].plot(dEs, zt300, "o-", label="300 K")
    ax[0].plot(dEs, zt100, "s--", label="100 K")
    ax[0].set_xscale("log"); ax[0].invert_xaxis()
    ax[0].set_xlabel("energy-grid spacing dE (eV)")
    ax[0].set_ylabel("peak ZT")
    ax[0].set_title("(a) convergence vs dE")
    ax[0].legend(frameon=False)
    ax[1].plot(lengths, ztL, "o-", color="C2")
    ax[1].set_xlabel("scattering-region length (cells)")
    ax[1].set_ylabel("peak ZT (300 K)")
    ax[1].set_title("(b) length independence (pristine)")
    ax[1].set_xticks(lengths)
    ax[1].set_ylim(min(ztL) - 0.02, max(ztL) + 0.02)
    fig.tight_layout()
    out = os.path.join(FIGDIR, "fig8_convergence.png")
    fig.savefig(out, dpi=200)

    np.savez(os.path.join(ROOT, "data", "convergence.npz"),
             dEs=np.array(dEs), zt300=np.array(zt300), zt100=np.array(zt100),
             lengths=np.array(lengths), ztL=np.array(ztL))
    rel300 = abs(zt300[-1] - zt300[-2]) / zt300[-1] * 100
    print(f"\nRelative change of peak ZT(300K) from dE=0.005 -> 0.0025: {rel300:.2f}%")
    print(f"Length spread of peak ZT: {max(ztL)-min(ztL):.4f} (should be ~0 for pristine)")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
