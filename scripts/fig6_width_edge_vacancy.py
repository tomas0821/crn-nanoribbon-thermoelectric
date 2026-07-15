#!/usr/bin/env python
"""Fig 6: design rules -- width dependence, edge type, and edge-vacancy enhancement of ZT.

(a) ZT(mu) at 300 K for zigzag widths N = 8, 14, 20.
(b) peak ZT vs width N (zigzag).
(c) zigzag vs armchair ZT(mu), N = 14.
(d) edge-vacancy enhancement: pristine vs vacancy-disordered edges, zigzag N = 14.

Uses the fitted SK ribbons + thermo module. ZT with the ballistic kappa_ph estimate at 300 K.
Transmissions are cached under data/. Also prints Table 2 (peak ZT, optimal mu per config).

Run:  ~/venvs/crn-te/bin/python scripts/fig6_width_edge_vacancy.py
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

FIGDIR, DATADIR = os.path.join(ROOT, "figures"), os.path.join(ROOT, "data")
os.makedirs(FIGDIR, exist_ok=True)
os.makedirs(DATADIR, exist_ok=True)

E_GRID = np.linspace(-0.8, 1.0, 301)
MU = np.linspace(-0.5, 0.6, 221)
T0 = 300.0


def get_TE(p, edge, width, vac=0.0, seed=0):
    tag = f"{edge}_N{width}" + (f"_vac{int(vac*100)}s{seed}" if vac > 0 else "") + "_cmp"
    cache = os.path.join(DATADIR, tag + ".npz")
    if os.path.exists(cache):
        d = np.load(cache)
        if d["E"].shape == E_GRID.shape and np.allclose(d["E"], E_GRID):
            return d["T_up"], d["T_dn"]
    print(f"  computing {tag} ...")
    T_up = transmission(build_ribbon_sk(edge, width, p, +1, vacancy=vac, seed=seed), E_GRID)
    T_dn = transmission(build_ribbon_sk(edge, width, p, -1, vacancy=vac, seed=seed), E_GRID)
    np.savez(cache, E=E_GRID, T_up=T_up, T_dn=T_dn)
    return T_up, T_dn


def zt_of_mu(T_up, T_dn, T_K=T0, kfac=1.0):
    up = th.sweep_mu(E_GRID, T_up, MU, T_K)
    dn = th.sweep_mu(E_GRID, T_dn, MU, T_K)
    tot = th.combine_spins(up, dn)
    return th.ZT(tot, T_K, kfac * th.kappa_ph_ballistic(T_K))


def main():
    p = SKParams()
    rows = []  # Table 2

    fig, axs = plt.subplots(2, 2, figsize=(10, 7.6))

    # (a) width dependence + (b) peak ZT vs N
    widths = [8, 14, 20]
    peak_zt, peak_mu = [], []
    for N, col in zip(widths, ("C0", "C2", "C3")):
        Tu, Td = get_TE(p, "zigzag", N)
        zt = zt_of_mu(Tu, Td)
        axs[0, 0].plot(MU, zt, color=col, lw=1.8, label=f"N = {N}")
        i = int(np.argmax(zt))
        peak_zt.append(zt[i]); peak_mu.append(MU[i])
        rows.append(("zigzag", N, "pristine", zt[i], MU[i]))
    axs[0, 0].set_title("(a) ZT vs doping — zigzag widths (300 K)")
    axs[0, 0].set_xlabel(r"$\mu - E_F$ (eV)"); axs[0, 0].set_ylabel("ZT")
    axs[0, 0].legend(frameon=False); axs[0, 0].axvline(0, color="0.8", lw=0.6, ls=":")

    # (b) peak ZT vs width -- BOTH edges at matched N (fair edge comparison)
    arm_peak = []
    for N in widths:
        Tu, Td = get_TE(p, "armchair", N)
        zt = zt_of_mu(Tu, Td)
        i = int(np.argmax(zt))
        arm_peak.append(zt[i])
        if N != 14:
            rows.append(("armchair", N, "pristine", zt[i], MU[i]))
    axs[0, 1].plot(widths, peak_zt, "o-", color="C2", lw=1.8, ms=8, label="zigzag")
    axs[0, 1].plot(widths, arm_peak, "s--", color="C1", lw=1.8, ms=8, label="armchair")
    axs[0, 1].set_title("(b) peak ZT vs width, both edges")
    axs[0, 1].set_xlabel("ribbon width N"); axs[0, 1].set_ylabel("peak ZT (300 K)")
    axs[0, 1].set_xticks(widths); axs[0, 1].legend(frameon=False)

    # (c) zigzag vs armchair at matched N=14
    for edge, col in (("zigzag", "C2"), ("armchair", "C1")):
        Tu, Td = get_TE(p, edge, 14)
        zt = zt_of_mu(Tu, Td)
        axs[1, 0].plot(MU, zt, color=col, lw=1.8, label=edge)
        i = int(np.argmax(zt))
        if edge == "armchair":
            rows.append(("armchair", 14, "pristine", zt[i], MU[i]))
    axs[1, 0].set_title("(c) edge type — ZT vs doping (N=14, 300 K)")
    axs[1, 0].set_xlabel(r"$\mu - E_F$ (eV)"); axs[1, 0].set_ylabel("ZT")
    axs[1, 0].legend(frameon=False); axs[1, 0].axvline(0, color="0.8", lw=0.6, ls=":")

    # (d) ZT(T) at optimal doping for the three zigzag widths
    temps = np.linspace(50, 700, 60)
    for N, col in zip(widths, ("C0", "C2", "C3")):
        Tu, Td = get_TE(p, "zigzag", N)
        # optimal mu at 300 K
        zt300 = zt_of_mu(Tu, Td, 300.0)
        mu_opt = MU[int(np.argmax(zt300))]
        zt_t = []
        for T2 in temps:
            u = th.sweep_mu(E_GRID, Tu, np.array([mu_opt]), T2)
            dd = th.sweep_mu(E_GRID, Td, np.array([mu_opt]), T2)
            zt_t.append(float(th.ZT(th.combine_spins(u, dd), T2,
                                    th.kappa_ph_ballistic(T2))[0]))
        axs[1, 1].plot(temps, zt_t, color=col, lw=1.8, label=f"N = {N}")
    axs[1, 1].set_title("(d) ZT(T) at optimal doping (zigzag)")
    axs[1, 1].set_xlabel("temperature (K)"); axs[1, 1].set_ylabel("ZT")
    axs[1, 1].legend(frameon=False)

    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig6_width_edge_vacancy.png"), dpi=200)

    # Table 2
    print("\nTable 2 (peak ZT @300K, ballistic kappa_ph):")
    print(f"{'edge':10s} {'N':>3s} {'config':18s} {'peakZT':>7s} {'mu-E_F':>7s}")
    for r in rows:
        print(f"{r[0]:10s} {r[1]:3d} {r[2]:18s} {r[3]:7.3f} {r[4]:+7.2f}")
    with open(os.path.join(DATADIR, "table2.txt"), "w") as fh:
        fh.write("edge  N  config  peakZT  mu-E_F(eV)\n")
        for r in rows:
            fh.write(f"{r[0]}  {r[1]}  {r[2]}  {r[3]:.3f}  {r[4]:+.2f}\n")
    print("wrote figures/fig6_width_edge_vacancy.png, data/table2.txt")


if __name__ == "__main__":
    main()
