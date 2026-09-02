"""Sensitivity of the peak ZT to the one parameter outside the +/-10% sweep of Fig. 7: the
minority exchange shift of the effective conduction orbital, Delta^c_down (= delta_c, assumed
equal to Delta_ex = 3.6 eV in the model, Table 1).

Same protocol as sensitivity.py (zigzag N=14, 300 K, global optimum) plus the armchair N=8
in-window optimum (protocol of sensitivity_armchair8.py). delta_c x0.9 / x1.1 -> 3.24 / 3.96 eV.

Run:  ~/venvs/crn-te/bin/python scripts/sensitivity_delta_c.py  ->  data/sensitivity_delta_c.txt
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
T0 = 300.0
CASES = {  # geometry: (E grid, mu grid)  -- identical to the two production sensitivity scripts
    ("zigzag", 14): (np.linspace(-0.6, 1.5, 421), np.linspace(-0.4, 1.2, 321)),
    ("armchair", 8): (np.linspace(-0.8, 1.5, 461), np.linspace(-0.6, 1.2, 361)),
}


def peak_zt(edge, N, p, W, E_GRID, MU):
    key = os.path.join(DATADIR, f"sensdc_{edge}_N{N}_delta_c{p.delta_c:+.4f}".replace(".", "p") + ".npz")
    if os.path.exists(key):
        dd = np.load(key); Tu, Td = dd["Tu"], dd["Td"]
    else:
        Tu = transmission(build_ribbon_sk(edge, N, p, +1), E_GRID)
        Td = transmission(build_ribbon_sk(edge, N, p, -1), E_GRID)
        np.savez(key, Tu=Tu, Td=Td)
    up = th.sweep_mu(E_GRID, Tu, MU, T0)
    dn = th.sweep_mu(E_GRID, Td, MU, T0)
    zt = th.ZT(th.combine_spins(up, dn, T0), T0, kappa_ph(T0, W))
    i = int(np.argmax(zt))
    pol = MU < 1.0
    j = int(np.argmax(np.where(pol, zt, -1.0)))
    return zt[i], MU[i], zt[j], MU[j]


def main():
    base = SKParams()
    lines = ["# delta_c (= Delta^c_down) +/-10% sensitivity, 300 K: global peak ZT(mu) | polarized-window peak ZT(mu)"]
    print(lines[0])
    for (edge, N), (E_GRID, MU) in CASES.items():
        W = ribbon_width(edge, N, base.a)
        for fac in (1.0, 0.9, 1.1):
            p = dataclasses.replace(base, delta_c=base.delta_c * fac)
            zg, mg, zp, mp = peak_zt(edge, N, p, W, E_GRID, MU)
            row = f"{edge:8s} N={N:2d} delta_c={p.delta_c:.3f} (x{fac:.1f}): global {zg:.4f} ({mg:+.2f}) | polarized {zp:.4f} ({mp:+.2f})"
            print(row, flush=True)
            lines.append(row)
    with open(os.path.join(DATADIR, "sensitivity_delta_c.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("wrote data/sensitivity_delta_c.txt")


if __name__ == "__main__":
    main()
