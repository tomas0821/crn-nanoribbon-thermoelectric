#!/usr/bin/env python
"""Domain-wall leakage of the spin-valve OFF state: T(wall width) for zigzag N=14.

Spinful noncollinear calculation (crnte.valve): Walker wall of width lambda = pi*delta between
antiparallel leads. Limits validated: lambda -> 0 reproduces the exact collinear OFF state
(T = 0); lambda -> infinity reaches the adiabatic limit T -> T_P (spin tracks the texture).
The crossover scale is set by the spin-mistracking length ell_mt ~ hbar v_F / Delta_ex.

Writes data/wall_sweep.npz and figures/fig_wall.png; prints hbar*v_F and the crossover width.

Run:  ~/venvs/crn-te/bin/python scripts/fig_wall.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from crnte.monolayer_sk import SKParams  # noqa: E402
from crnte.valve import wall_transmission  # noqa: E402

DATADIR, FIGDIR = os.path.join(ROOT, "data"), os.path.join(ROOT, "figures")
DELTAS = np.array([0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0,
                   8.5, 10.0, 12.0, 15.0, 20.0, 30.0, 50.0])
ENERGIES = [0.0, 0.5]


def fermi_velocity(p):
    """Max majority band velocity at E_F from the pristine zigzag N=14 lead (eV * Angstrom)."""
    import kwant
    from crnte.ribbon_sk import build_ribbon_sk
    lead = build_ribbon_sk("zigzag", 14, p, +1).leads[0]
    bands = kwant.physics.Bands(lead)
    ks = np.linspace(-np.pi, np.pi, 801)
    evs = np.array([bands(k) for k in ks])
    period = 2 * p.a
    vmax = 0.0
    for b in range(evs.shape[1]):
        e = evs[:, b]
        cross = np.where(np.sign(e[:-1]) != np.sign(e[1:]))[0]
        for i in cross:
            # ks is the Bloch phase over one period: dE/dk_real = dE/dphase * period
            v = abs((e[i + 1] - e[i]) / (ks[i + 1] - ks[i])) * period   # dE/dk in eV*A
            vmax = max(vmax, v)
    return vmax


def main():
    p = SKParams()
    cache = os.path.join(DATADIR, "wall_sweep.npz")
    if os.path.exists(cache):
        d = np.load(cache)
        T = d["T"]
    else:
        T = np.array([wall_transmission("zigzag", 14, p, float(dl), ENERGIES)
                      for dl in DELTAS])
        np.savez(cache, deltas=DELTAS, lambdas=np.pi * DELTAS, energies=np.array(ENERGIES), T=T)

    lam = np.pi * DELTAS
    TP = {0.0: 8.0, 0.5: 5.0}
    hbar_vF = fermi_velocity(p)
    ell_mt = hbar_vF / p.delta_ex
    # crossover: lambda where T = T_P/2 at E_F
    i_half = np.argmin(np.abs(T[:, 0] - 0.5 * TP[0.0]))
    lam_half = np.interp(0.5 * TP[0.0], T[:, 0], lam)
    print(f"hbar v_F (max, majority, E_F) = {hbar_vF:.2f} eV*A -> ell_mt = {ell_mt:.2f} A")
    print(f"half-transparency wall width lambda_1/2 = {lam_half:.1f} A (grid pt {lam[i_half]:.1f})")

    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.8))
    for j, (E, col) in enumerate(zip(ENERGIES, ("C0", "C2"))):
        axs[0].plot(lam, T[:, j], "o-", color=col, lw=1.8, ms=5,
                    label=fr"$E-E_F={E:+.1f}$ eV")
        axs[0].axhline(TP[E], color=col, lw=0.8, ls=":")
    axs[0].set_xlabel("wall width $\\lambda = \\pi\\delta$ (Å)")
    axs[0].set_ylabel(r"total transmission $T_{\rm AP}$")
    axs[0].set_title("(a) OFF-state leakage vs wall width")
    axs[0].legend(frameon=False, fontsize=9)

    Tlog = np.where(T[:, 0] > 1e-16, T[:, 0], 1e-16)
    axs[1].semilogy(lam, Tlog, "o-", color="C0", lw=1.8, ms=5)
    axs[1].axhline(8.0, color="C0", lw=0.8, ls=":")
    axs[1].axvline(lam_half, color="0.5", lw=0.8, ls="--")
    axs[1].text(lam_half + 1.5, 1e-4, f"$\\lambda_{{1/2}}\\simeq{lam_half:.0f}$ Å",
                fontsize=9, color="0.35")
    axs[1].set_xlim(-2, 50)
    axs[1].set_xlabel("wall width $\\lambda$ (Å)")
    axs[1].set_ylabel(r"$T_{\rm AP}(E_F)$")
    axs[1].set_title("(b) same, log scale (collinear limit: $T=0$)")

    fig.tight_layout()
    out = os.path.join(FIGDIR, "fig_wall.png")
    fig.savefig(out, dpi=200)
    print(f"wrote {out}")
    with open(os.path.join(DATADIR, "wall_sweep.txt"), "w") as fh:
        fh.write(f"hbar_vF_eVA {hbar_vF:.3f}\nell_mt_A {ell_mt:.3f}\nlambda_half_A {lam_half:.2f}\n")
        for dl, row in zip(DELTAS, T):
            fh.write(f"delta {dl:6.2f}  lambda {np.pi*dl:7.2f}  " +
                     "  ".join(f"T({E:+.1f})={t:.4e}" for E, t in zip(ENERGIES, row)) + "\n")


if __name__ == "__main__":
    main()
