#!/usr/bin/env python
"""Fig 6: width, edge and temperature dependence of the thermoelectric response.

(a) ZT(mu) at 300 K for zigzag widths N = 8, 14, 20 (each with ITS OWN phonon-Landauer
    kappa_ph(W), so the width trend includes the growth of the phonon background).
(b) peak ZT vs width N for both edges at matched N.
(c) zigzag vs armchair ZT(mu), N = 14.
(d) ZT(T) at the 300-K optimal doping for the three zigzag widths.

Uses the unified fine T(E) caches (scripts/run_all_transmissions.py). Prints/writes Table 2.

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
from crnte.phonon import kappa_ph, ribbon_width  # noqa: E402

FIGDIR, DATADIR = os.path.join(ROOT, "figures"), os.path.join(ROOT, "data")
MU = np.linspace(-0.6, 1.2, 361)
T0 = 300.0


def get_TE(edge, width):
    d = np.load(os.path.join(DATADIR, f"{edge}_N{width}_TE.npz"))
    return d["E"], d["T_up"], d["T_dn"]


def zt_of_mu(E, T_up, T_dn, W, T_K=T0, kfac=1.0):
    up = th.sweep_mu(E, T_up, MU, T_K)
    dn = th.sweep_mu(E, T_dn, MU, T_K)
    tot = th.combine_spins(up, dn, T_K)
    return th.ZT(tot, T_K, kfac * kappa_ph(T_K, W))


def main():
    p = SKParams()
    rows = []  # Table 2

    fig, axs = plt.subplots(2, 2, figsize=(10, 7.6))

    widths = [8, 14, 20]
    peak_zt = {"zigzag": [], "armchair": []}
    for edge in ("zigzag", "armchair"):
        for N in widths:
            E, Tu, Td = get_TE(edge, N)
            W = ribbon_width(edge, N, p.a)
            zt = zt_of_mu(E, Tu, Td, W)
            i = int(np.argmax(zt))
            peak_zt[edge].append(zt[i])
            rows.append((edge, N, W, zt[i], MU[i]))
            if edge == "zigzag":
                col = {8: "C0", 14: "C2", 20: "C3"}[N]
                axs[0, 0].plot(MU, zt, color=col, lw=1.8, label=f"N = {N}")
    axs[0, 0].set_title("(a) ZT vs doping — zigzag widths (300 K)")
    axs[0, 0].set_xlabel(r"$\mu - E_F$ (eV)"); axs[0, 0].set_ylabel("ZT")
    axs[0, 0].legend(frameon=False); axs[0, 0].axvline(0, color="0.8", lw=0.6, ls=":")

    axs[0, 1].plot(widths, peak_zt["zigzag"], "o-", color="C2", lw=1.8, ms=8, label="zigzag")
    axs[0, 1].plot(widths, peak_zt["armchair"], "s--", color="C1", lw=1.8, ms=8, label="armchair")
    axs[0, 1].set_title("(b) peak ZT vs width, both edges")
    axs[0, 1].set_xlabel("ribbon width N"); axs[0, 1].set_ylabel("peak ZT (300 K)")
    axs[0, 1].set_xticks(widths); axs[0, 1].legend(frameon=False)

    for edge, col in (("zigzag", "C2"), ("armchair", "C1")):
        E, Tu, Td = get_TE(edge, 14)
        W = ribbon_width(edge, 14, p.a)
        axs[1, 0].plot(MU, zt_of_mu(E, Tu, Td, W), color=col, lw=1.8, label=edge)
    axs[1, 0].set_title("(c) edge type — ZT vs doping (N=14, 300 K)")
    axs[1, 0].set_xlabel(r"$\mu - E_F$ (eV)"); axs[1, 0].set_ylabel("ZT")
    axs[1, 0].legend(frameon=False); axs[1, 0].axvline(0, color="0.8", lw=0.6, ls=":")

    temps = np.linspace(50, 700, 60)
    for N, col in zip(widths, ("C0", "C2", "C3")):
        E, Tu, Td = get_TE("zigzag", N)
        W = ribbon_width("zigzag", N, p.a)
        zt300 = zt_of_mu(E, Tu, Td, W, 300.0)
        mu_opt = MU[int(np.argmax(zt300))]
        zt_t = []
        for T2 in temps:
            u = th.sweep_mu(E, Tu, np.array([mu_opt]), T2)
            dd = th.sweep_mu(E, Td, np.array([mu_opt]), T2)
            zt_t.append(float(th.ZT(th.combine_spins(u, dd, T2), T2, kappa_ph(T2, W))[0]))
        axs[1, 1].plot(temps, zt_t, color=col, lw=1.8, label=f"N = {N}")
    axs[1, 1].set_title("(d) ZT(T) at optimal doping (zigzag)")
    axs[1, 1].set_xlabel("temperature (K)"); axs[1, 1].set_ylabel("ZT")
    axs[1, 1].legend(frameon=False)

    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig6_width_edge_vacancy.png"), dpi=200)

    print("\nTable 2 (peak ZT @300K, phonon-Landauer kappa_ph(W)):")
    print(f"{'edge':10s} {'N':>3s} {'W(A)':>6s} {'peakZT':>8s} {'mu-E_F':>7s}")
    for r in rows:
        print(f"{r[0]:10s} {r[1]:3d} {r[2]:6.1f} {r[3]:8.4f} {r[4]:+7.2f}")
    with open(os.path.join(DATADIR, "table2.txt"), "w") as fh:
        fh.write("edge  N  W(A)  peakZT  mu-E_F(eV)\n")
        for r in rows:
            fh.write(f"{r[0]}  {r[1]}  {r[2]:.1f}  {r[3]:.4f}  {r[4]:+.2f}\n")
    print("wrote figures/fig6_width_edge_vacancy.png, data/table2.txt")


if __name__ == "__main__":
    main()
