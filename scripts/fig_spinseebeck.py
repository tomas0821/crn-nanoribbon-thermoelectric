#!/usr/bin/env python
"""Spin-caloritronic response of the zigzag CrN ribbon (spin-resolved thermoelectrics).

Because the minority channel is gapped around E_F, a temperature gradient drives a nearly 100%
spin-polarized thermoelectric current -- the ribbon is an intrinsic spin-Seebeck element.

(a) Per-spin Seebeck S_up, S_dn and the charge (total) Seebeck S_c vs mu.
(b) Per-spin power factor PF_up, PF_dn, and the spin polarization of the thermoelectric current
    P = (PF_up - PF_dn)/(PF_up + PF_dn), which is ~1 near E_F and drops when the minority
    channel activates (mu-E_F > ~1 eV).

Uses the cached fine transmission from fig45. Run:
  ~/venvs/crn-te/bin/python scripts/fig_spinseebeck.py
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
CACHE = os.path.join(DATADIR, "zigzag_N14_TE.npz")
T_K = 300.0
MU = np.linspace(-0.5, 1.3, 361)


def get_TE():
    if os.path.exists(CACHE):
        d = np.load(CACHE)
        return d["E"], d["T_up"], d["T_dn"]
    p = SKParams()
    E = np.linspace(-1.2, 1.5, 541)
    Tu = transmission(build_ribbon_sk("zigzag", 14, p, +1), E)
    Td = transmission(build_ribbon_sk("zigzag", 14, p, -1), E)
    np.savez(CACHE, E=E, T_up=Tu, T_dn=Td)
    return E, Tu, Td


def main():
    E, Tu, Td = get_TE()
    up = th.sweep_mu(E, Tu, MU, T_K)
    dn = th.sweep_mu(E, Td, MU, T_K)
    tot = th.combine_spins(up, dn, T_K)

    fig, axs = plt.subplots(1, 2, figsize=(9.4, 3.8))

    # (a) per-spin and charge Seebeck. Mask each spin channel where its own conductance is
    # negligible (deep in the gap S_sigma is exponentially activated and not meaningful).
    G0 = 3.874e-5      # e^2/h in S
    Sup = np.where(up["G"] > 1e-3 * G0, up["S"], np.nan)
    Sdn = np.where(dn["G"] > 1e-3 * G0, dn["S"], np.nan)
    axs[0].plot(MU, Sup * 1e6, color="C3", lw=1.8, label=r"$S_\uparrow$ (majority)")
    axs[0].plot(MU, Sdn * 1e6, color="C0", lw=1.8, ls="--", label=r"$S_\downarrow$ (minority)")
    axs[0].plot(MU, tot["S"] * 1e6, color="k", lw=1.3, ls=":", label=r"$S_c$ (charge)")
    axs[0].set_xlabel(r"$\mu - E_F$ (eV)"); axs[0].set_ylabel(r"Seebeck ($\mu$V/K)")
    axs[0].set_title("(a) spin-resolved Seebeck (300 K)")
    axs[0].axvline(0, color="0.8", lw=0.6, ls=":"); axs[0].legend(frameon=False, fontsize=9)
    axs[0].set_ylim(-450, 250)

    # (b) per-spin power factor + thermoelectric-current spin polarization
    ax = axs[1]
    ax.plot(MU, up["PF"] * 1e12, color="C3", lw=1.8, label=r"PF$_\uparrow$")
    ax.plot(MU, dn["PF"] * 1e12, color="C0", lw=1.8, ls="--", label=r"PF$_\downarrow$")
    ax.set_xlabel(r"$\mu - E_F$ (eV)"); ax.set_ylabel(r"power factor (pW/K$^2$)")
    ax.set_title("(b) spin-resolved power factor + polarization")
    ax.axvline(0, color="0.8", lw=0.6, ls=":")
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    # spin polarization on a twin axis; mask the "dead zone" where both PFs are negligible
    # (P is a 0/0 there: both spin power factors vanish at S-sign changes, hence the gaps)
    pf_tot = up["PF"] + dn["PF"]
    thr = 0.02 * pf_tot.max()
    P = np.where(pf_tot > thr, (up["PF"] - dn["PF"]) / np.where(pf_tot > thr, pf_tot, 1.0), np.nan)
    ax2 = ax.twinx()
    ax2.plot(MU, 100 * P, color="C2", lw=2.0, label=r"$P_{PF}$")
    # conductance polarization P_G: well defined everywhere the ribbon conducts, = 100%
    # over the whole half-metallic window (referee round 1: quoted in text, now plotted)
    Gtot = up["G"] + dn["G"]
    PG = np.where(Gtot > 1e-3 * 3.874e-5, (up["G"] - dn["G"]) / np.where(Gtot > 0, Gtot, 1.0),
                  np.nan)
    ax2.plot(MU, 100 * PG, color="C4", lw=1.4, ls="-.", label=r"$P_G$")
    ax2.set_ylabel("spin polarization (%)", color="C2")
    ax2.tick_params(axis="y", labelcolor="C2")
    ax2.set_ylim(-115, 115)
    ax2.axhline(0, color="C2", lw=0.5, ls=":")
    ax2.legend(frameon=False, fontsize=8, loc="center right")

    fig.tight_layout()
    out = os.path.join(FIGDIR, "fig_spinseebeck.png")
    fig.savefig(out, dpi=200)

    # report the spin-polarized window
    near = np.abs(MU) < 0.5
    print(f"thermocurrent spin polarization at E_F: {100*P[np.argmin(np.abs(MU))]:.1f}%")
    imx = int(np.argmax(dn["PF"]))
    print(f"minority PF activates near the minority CBM: peak {dn['PF'][imx]*1e12:.3f} pW/K^2 "
          f"at mu-E_F={MU[imx]:+.2f} eV")
    print(f"min polarization over window: {100*np.nanmin(P):.1f}%  (majority background persists)")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
