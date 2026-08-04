#!/usr/bin/env python
"""Parameter-sensitivity sweep for the ARMCHAIR N=8 ribbon (the promoted geometry).

Same protocol as scripts/sensitivity.py (zigzag N=14): vary every fitted parameter by +/-10%,
recompute the peak ZT at 300 K (phonon-Landauer kappa_ph). The armchair N=8 optimum sits inside
the fully polarized window (mu-E_F ~ -0.34 eV), so this sweep attaches an uncertainty to the
paper's flagship ZT = 0.145. Writes data/sensitivity_armchair8.txt.

Run:  ~/venvs/crn-te/bin/python scripts/sensitivity_armchair8.py
"""
import dataclasses
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from crnte import thermo as th  # noqa: E402
from crnte.monolayer_sk import SKParams  # noqa: E402
from crnte.phonon import kappa_ph, ribbon_width  # noqa: E402
from crnte.ribbon_sk import build_ribbon_sk, transmission  # noqa: E402

DATADIR = os.path.join(ROOT, "data")
os.makedirs(DATADIR, exist_ok=True)

EDGE, N = "armchair", 8
E_GRID = np.linspace(-0.8, 1.5, 461)     # dE = 0.005 eV; covers the in-window optimum
MU = np.linspace(-0.6, 1.2, 361)
T0 = 300.0
PARAMS = ["eps_dz2", "eps_pi", "eps_pz", "pdpi", "t_zz", "delta_ex",
          "eps_c", "t_c1", "t_c2", "t_c3"]


def peak_zt(p, W):
    tag = "sensA8_" + "_".join(f"{k}{getattr(p, k):+.4f}" for k in PARAMS)
    key = os.path.join(DATADIR, tag.replace(".", "p") + ".npz")
    if os.path.exists(key):
        dd = np.load(key)
        Tu, Td = dd["Tu"], dd["Td"]
    else:
        Tu = transmission(build_ribbon_sk(EDGE, N, p, +1), E_GRID)
        Td = transmission(build_ribbon_sk(EDGE, N, p, -1), E_GRID)
        np.savez(key, Tu=Tu, Td=Td)
    up = th.sweep_mu(E_GRID, Tu, MU, T0)
    dn = th.sweep_mu(E_GRID, Td, MU, T0)
    zt = th.ZT(th.combine_spins(up, dn, T0), T0, kappa_ph(T0, W))
    i = int(np.argmax(zt))
    return zt[i], MU[i]


def main():
    base = SKParams()
    W = ribbon_width(EDGE, N, base.a)
    z0, mu0 = peak_zt(base, W)
    print(f"baseline peak ZT = {z0:.4f} at mu-E_F={mu0:+.2f} eV\n", flush=True)

    results = {}
    allz = [z0]
    for par in PARAMS:
        v = getattr(base, par)
        row = []
        for fac in (0.9, 1.1):
            p = dataclasses.replace(base, **{par: v * fac})
            z, mu = peak_zt(p, W)
            row.append((z, mu))
            allz.append(z)
            print(f"  {par:9s} x{fac:.1f} ({v:+.3f}->{v*fac:+.3f}):  peak ZT = {z:.4f} "
                  f"at mu={mu:+.2f}  (dZT = {z-z0:+.4f}, {100*(z-z0)/z0:+.1f}%)", flush=True)
        results[par] = row
    zmin, zmax = min(allz), max(allz)
    print(f"\nOverall peak-ZT spread over all +/-10% variations: "
          f"[{zmin:.4f}, {zmax:.4f}]  (baseline {z0:.4f})")

    with open(os.path.join(DATADIR, "sensitivity_armchair8.txt"), "w") as fh:
        fh.write(f"baseline peak ZT = {z0:.4f} at mu-E_F={mu0:+.2f} eV\n")
        for par in PARAMS:
            (zlo, mlo), (zhi, mhi) = results[par]
            fh.write(f"{par}  -10%: {zlo:.4f} (mu {mlo:+.2f})  +10%: {zhi:.4f} (mu {mhi:+.2f})\n")
        fh.write(f"overall spread [{zmin:.4f}, {zmax:.4f}]\n")
    print("wrote data/sensitivity_armchair8.txt")


if __name__ == "__main__":
    main()
