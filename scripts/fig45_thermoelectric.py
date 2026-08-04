#!/usr/bin/env python
"""Fig 5: thermoelectric response of a zigzag CrN nanoribbon (extended SK model).

Fig 5 - power factor and ZT vs mu at 300 K (kappa_ph bracket).
Referee round 1 tightening: the old Fig 4 (S(mu) at 100/300/500 K) and the old Fig 5(c)
(ZT(T) at the optimum) were dropped -- S(mu) lives in fig_spinseebeck(a) and ZT(T) in
fig6(d); the 100 K curve also used the production 5 meV grid, unconverged at that T.

Uses the unified fine T_sigma(E) cache (scripts/run_all_transmissions.py, dE = 0.005 eV) and
the phonon-Landauer kappa_ph anchored to the published h-CrN phonon dispersion (crnte.phonon).

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
from crnte.phonon import kappa_ph, ribbon_width  # noqa: E402

FIGDIR = os.path.join(ROOT, "figures")
DATADIR = os.path.join(ROOT, "data")
os.makedirs(FIGDIR, exist_ok=True)

EDGE, WIDTH = "zigzag", 14
CACHE = os.path.join(DATADIR, f"{EDGE}_N{WIDTH}_TE.npz")


def main():
    p = SKParams()
    d = np.load(CACHE)
    E, T_up, T_dn = d["E"], d["T_up"], d["T_dn"]
    mu = np.linspace(-0.6, 1.2, 361)
    W = ribbon_width(EDGE, WIDTH, p.a)

    # ---------- Fig 5: PF and ZT (with kappa_ph bracket) vs mu ----------
    T_K = 300.0
    up = th.sweep_mu(E, T_up, mu, T_K)
    dn = th.sweep_mu(E, T_dn, mu, T_K)
    tot = th.combine_spins(up, dn, T_K)
    kph = kappa_ph(T_K, W)

    fig, axs = plt.subplots(1, 2, figsize=(8.2, 3.6))
    axs[0].plot(mu, tot["PF"] * 1e12, color="C4", lw=1.8)   # pW/K^2
    axs[0].set_ylabel(r"power factor $S^2G$ (pW/K$^2$)")
    axs[0].set_title("Power factor (300 K)")

    brackets = [(0.5 * kph, "C2", "-", r"$0.5\,\kappa_{ph}$"),
                (kph, "C0", "-", r"$\kappa_{ph}$ (phonon Landauer)"),
                (2.0 * kph, "C3", "-", r"$2\,\kappa_{ph}$")]
    for kp, col, ls, lab in brackets:
        axs[1].plot(mu, th.ZT(tot, T_K, kappa_ph=kp), color=col, ls=ls, lw=1.6, label=lab)
    axs[1].set_ylabel(r"$ZT$")
    axs[1].set_title("ZT vs doping (300 K)")
    axs[1].legend(frameon=False, fontsize=7.5, loc="upper left")

    for a in axs[:2]:
        a.set_xlabel(r"$\mu - E_F$ (eV)")
        a.axvline(0, color="0.7", lw=0.6, ls=":")

    ZT_300 = th.ZT(tot, T_K, kappa_ph=kph)
    mu_opt = mu[int(np.argmax(ZT_300))]

    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig5_zt.png"), dpi=200)

    # ---------- report ----------
    ipf = int(np.argmax(tot["PF"]))
    iS = int(np.argmax(np.abs(tot["S"])))
    imax = int(np.argmax(ZT_300))
    print(f"W = {W:.1f} A, kappa_ph(300K) = {kph*1e9:.3f} nW/K")
    print(f"peak |S| (300K)          = {tot['S'][iS]*1e6:+.1f} uV/K at mu-E_F={mu[iS]:+.2f} eV")
    print(f"peak PF  (300K)          = {tot['PF'][ipf]*1e12:.3f} pW/K^2 at mu-E_F={mu[ipf]:+.2f} eV")
    print(f"peak ZT  (300K)          = {ZT_300[imax]:.4f} at mu-E_F={mu[imax]:+.2f} eV")
    zt700 = None
    u = th.sweep_mu(E, T_up, np.array([mu_opt]), 700.0)
    dd = th.sweep_mu(E, T_dn, np.array([mu_opt]), 700.0)
    zt700 = float(th.ZT(th.combine_spins(u, dd, 700.0), 700.0, kappa_ph(700.0, W))[0])
    print(f"ZT(700K) at same doping  = {zt700:.4f}")
    print("wrote figures/fig4_seebeck.png, figures/fig5_zt.png")


if __name__ == "__main__":
    main()
