#!/usr/bin/env python
"""Parameter-sensitivity sweep: how robust is the peak ZT to the fitted SK parameters?

Vary each tight-binding parameter (and the exchange splitting) by +/-10% about the fitted values,
recompute the peak ZT of the zigzag N=14 ribbon at 300 K (ballistic kappa_ph), and report the
spread. Produces a tornado plot (fig7_sensitivity.png) and prints the numbers.

Run:  ~/venvs/crn-te/bin/python scripts/sensitivity.py
"""
import dataclasses
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
os.makedirs(DATADIR, exist_ok=True)

E_GRID = np.linspace(-0.5, 0.9, 201)
MU = np.linspace(-0.1, 0.5, 121)
T0 = 300.0
PARAMS = ["eps_dz2", "eps_pi", "eps_pz", "pdpi", "t_zz", "delta_ex"]
LABELS = {"eps_dz2": r"$\varepsilon_{d_{z^2}}$", "eps_pi": r"$\varepsilon_\pi$",
          "eps_pz": r"$\varepsilon_{p_z}$", "pdpi": r"$V_{pd\pi}$",
          "t_zz": r"$t_{zz}$", "delta_ex": r"$\Delta_{ex}$"}


def peak_zt(p):
    tag = "sens_" + "_".join(f"{k}{getattr(p,k):+.4f}" for k in PARAMS)
    cache = os.path.join(DATADIR, "sens_cache.npz") if False else None  # per-config below
    key = os.path.join(DATADIR, tag.replace(".", "p") + ".npz")
    if os.path.exists(key):
        dd = np.load(key)
        Tu, Td = dd["Tu"], dd["Td"]
    else:
        Tu = transmission(build_ribbon_sk("zigzag", 14, p, +1), E_GRID)
        Td = transmission(build_ribbon_sk("zigzag", 14, p, -1), E_GRID)
        np.savez(key, Tu=Tu, Td=Td)
    up = th.sweep_mu(E_GRID, Tu, MU, T0)
    dn = th.sweep_mu(E_GRID, Td, MU, T0)
    zt = th.ZT(th.combine_spins(up, dn), T0, th.kappa_ph_ballistic(T0))
    i = int(np.argmax(zt))
    return zt[i], MU[i]


def main():
    base = SKParams()
    z0, mu0 = peak_zt(base)
    print(f"baseline peak ZT = {z0:.3f} at mu-E_F={mu0:+.2f} eV\n")

    results = {}
    allz = [z0]
    for par in PARAMS:
        v = getattr(base, par)
        row = []
        for fac in (0.9, 1.1):
            p = dataclasses.replace(base, **{par: v * fac})
            z, mu = peak_zt(p)
            row.append(z)
            allz.append(z)
            print(f"  {par:9s} x{fac:.1f} ({v:+.3f}->{v*fac:+.3f}):  peak ZT = {z:.3f}  "
                  f"(dZT = {z-z0:+.3f}, {100*(z-z0)/z0:+.1f}%)")
        results[par] = row
    zmin, zmax = min(allz), max(allz)
    print(f"\nOverall peak-ZT spread over all +/-10% variations: "
          f"[{zmin:.3f}, {zmax:.3f}]  (baseline {z0:.3f}; "
          f"{100*(zmin-z0)/z0:+.0f}% .. {100*(zmax-z0)/z0:+.0f}%)")

    # tornado plot
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    order = sorted(PARAMS, key=lambda k: abs(results[k][1] - results[k][0]))
    y = np.arange(len(order))
    for i, par in enumerate(order):
        lo, hi = results[par]
        ax.barh(i, hi - z0, left=z0, color="C0", alpha=0.55,
                label="+10%" if i == 0 else None)
        ax.barh(i, lo - z0, left=z0, color="C3", alpha=0.55,
                label="-10%" if i == 0 else None)
    ax.axvline(z0, color="k", lw=1.2, label="baseline")
    ax.set_yticks(y)
    ax.set_yticklabels([LABELS[k] for k in order])
    ax.set_xlabel("peak ZT (300 K, zigzag N=14)")
    ax.set_title(r"Sensitivity of peak ZT to $\pm10\%$ parameter variation")
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    fig.tight_layout()
    out = os.path.join(FIGDIR, "fig7_sensitivity.png")
    fig.savefig(out, dpi=200)
    print(f"wrote {out}")

    with open(os.path.join(DATADIR, "sensitivity.txt"), "w") as fh:
        fh.write(f"baseline peak ZT = {z0:.3f} at mu-E_F={mu0:+.2f} eV\n")
        for par in PARAMS:
            fh.write(f"{par}  -10%: {results[par][0]:.3f}  +10%: {results[par][1]:.3f}\n")
        fh.write(f"overall spread [{zmin:.3f}, {zmax:.3f}]\n")


if __name__ == "__main__":
    main()
