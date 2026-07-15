#!/usr/bin/env python
"""Figs 4-5: thermoelectric response of a zigzag CrN nanoribbon (fitted SK model).

Fig 4 - Seebeck S(mu) at several temperatures (spin-resolved + total).
Fig 5 - power factor, electronic ZT vs mu at fixed T; and ZT(T) at the optimal mu.

Computes a FINE T_sigma(E) near E_F once (cached to data/), then evaluates the Onsager
integrals (crnte.thermo). ZT here is the electronic bound (kappa_ph -> 0); a kappa_ph bracket
is added later per the plan.

Run:  ~/venvs/crn-te/bin/python scripts/fig45_thermoelectric.py
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
from crnte.ribbon_sk import build_ribbon_sk, transmission  # noqa: E402

FIGDIR = os.path.join(ROOT, "figures")
DATADIR = os.path.join(ROOT, "data")
os.makedirs(FIGDIR, exist_ok=True)
os.makedirs(DATADIR, exist_ok=True)

WIDTH = 14
EDGE = "zigzag"
E_GRID = np.linspace(-1.2, 1.5, 541)     # fine grid near E_F (0.005 eV spacing)
CACHE = os.path.join(DATADIR, f"{EDGE}_N{WIDTH}_TE.npz")


def get_transmission(p):
    """Fine T_up(E), T_dn(E); cached to data/."""
    if os.path.exists(CACHE):
        d = np.load(CACHE)
        if d["E"].shape == E_GRID.shape and np.allclose(d["E"], E_GRID):
            print(f"loaded cached transmission {CACHE}")
            return d["E"], d["T_up"], d["T_dn"]
    print("computing fine transmission (cache miss)...")
    T_up = transmission(build_ribbon_sk(EDGE, WIDTH, p, +1), E_GRID)
    T_dn = transmission(build_ribbon_sk(EDGE, WIDTH, p, -1), E_GRID)
    np.savez(CACHE, E=E_GRID, T_up=T_up, T_dn=T_dn)
    return E_GRID, T_up, T_dn


def main():
    p = SKParams()
    E, T_up, T_dn = get_transmission(p)
    mu = np.linspace(-0.6, 0.6, 241)

    # ---------- Fig 4: Seebeck S(mu) ----------
    fig, ax = plt.subplots(figsize=(5.6, 4.2))
    for T_K, c in ((100, "C0"), (300, "C2"), (500, "C3")):
        up = th.sweep_mu(E, T_up, mu, T_K)
        dn = th.sweep_mu(E, T_dn, mu, T_K)
        tot = th.combine_spins(up, dn, T_K)
        ax.plot(mu, tot["S"] * 1e6, color=c, lw=1.8, label=f"{T_K} K")
    ax.axhline(0, color="k", lw=0.6, ls=":")
    ax.axvline(0, color="0.7", lw=0.6, ls=":")
    ax.set_xlabel(r"$\mu - E_F$ (eV)")
    ax.set_ylabel(r"Seebeck $S$ ($\mu$V/K)")
    ax.set_title(f"{EDGE} CrN ribbon (N$\\approx${WIDTH}) — Seebeck")
    ax.legend(frameon=False, title="temperature")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig4_seebeck.png"), dpi=200)

    # ---------- Fig 5: PF and ZT (with kappa_ph bracket) vs mu, and ZT(T) ----------
    T_K = 300.0
    up = th.sweep_mu(E, T_up, mu, T_K)
    dn = th.sweep_mu(E, T_dn, mu, T_K)
    tot = th.combine_spins(up, dn, T_K)
    kph = th.kappa_ph_ballistic(T_K)     # ballistic estimate at 300 K

    fig, axs = plt.subplots(1, 3, figsize=(11, 3.6))
    axs[0].plot(mu, tot["PF"] * 1e12, color="C4", lw=1.8)   # pW/K^2
    axs[0].set_ylabel(r"power factor $S^2G$ (pW/K$^2$)")
    axs[0].set_title("Power factor (300 K)")

    # ZT with a kappa_ph bracket; the kappa_ph->0 bound is shown clipped (it diverges in the gap)
    brackets = [(0.0, "C1", ":", r"$\kappa_{ph}\to0$ (bound)"),
                (0.5 * kph, "C2", "-", r"$0.5\,\kappa_{ph}^{bal}$"),
                (kph, "C0", "-", r"$\kappa_{ph}^{bal}$ ($4\kappa_0$)"),
                (2.0 * kph, "C3", "-", r"$2\,\kappa_{ph}^{bal}$")]
    for kp, col, ls, lab in brackets:
        axs[1].plot(mu, th.ZT(tot, T_K, kappa_ph=kp), color=col, ls=ls, lw=1.6, label=lab)
    axs[1].set_ylabel(r"$ZT$")
    axs[1].set_title("ZT vs doping (300 K)")
    axs[1].set_ylim(0, 3.0)
    axs[1].legend(frameon=False, fontsize=7.5, loc="upper left")

    for a in axs[:2]:
        a.set_xlabel(r"$\mu - E_F$ (eV)")
        a.axvline(0, color="0.7", lw=0.6, ls=":")

    # ZT(T) at the mu that maximizes the (physical) ballistic-kappa_ph ZT at 300 K
    ZT_bal_300 = th.ZT(tot, T_K, kappa_ph=kph)
    mu_opt = mu[int(np.argmax(ZT_bal_300))]
    temps = np.linspace(50, 700, 66)
    for factor, col, lab in ((0.5, "C2", r"$0.5\,\kappa_{ph}^{bal}$"),
                             (1.0, "C0", r"$\kappa_{ph}^{bal}$"),
                             (2.0, "C3", r"$2\,\kappa_{ph}^{bal}$")):
        zt_T = []
        for T2 in temps:
            u = th.sweep_mu(E, T_up, np.array([mu_opt]), T2)
            dd = th.sweep_mu(E, T_dn, np.array([mu_opt]), T2)
            zt_T.append(float(th.ZT(th.combine_spins(u, dd, T2), T2,
                                    factor * th.kappa_ph_ballistic(T2))[0]))
        axs[2].plot(temps, zt_T, color=col, lw=1.7, label=lab)
    axs[2].set_xlabel("temperature (K)")
    axs[2].set_ylabel(r"$ZT$")
    axs[2].set_title(f"ZT(T) at $\\mu-E_F$={mu_opt:+.2f} eV")
    axs[2].legend(frameon=False, fontsize=7.5)

    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig5_zt.png"), dpi=200)

    # ---------- report ----------
    ipf = int(np.argmax(tot["PF"]))
    iS = int(np.argmax(np.abs(tot["S"])))
    imax = int(np.argmax(ZT_bal_300))
    print(f"peak |S| (300K)          = {tot['S'][iS]*1e6:+.1f} uV/K at mu-E_F={mu[iS]:+.2f} eV")
    print(f"peak PF  (300K)          = {tot['PF'][ipf]*1e12:.2f} pW/K^2 at mu-E_F={mu[ipf]:+.2f} eV")
    print(f"kappa_ph^bal(300K)       = {kph*1e9:.2f} nW/K")
    print(f"peak ZT (ballistic,300K) = {ZT_bal_300[imax]:.3f} at mu-E_F={mu[imax]:+.2f} eV")
    print(f"wrote figures/fig4_seebeck.png, figures/fig5_zt.png")


if __name__ == "__main__":
    main()
