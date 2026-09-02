"""Quantify the phonon gapless-mode-floor caveat (Sec. 2.5): 4 modes (Rego-Kirczenow 3D beam,
production) vs 3 modes (strictly 2D sheet: LA, TA, ZA).

Uses the cached production T(E) (data/*_TE.npz); only kappa_ph is recomputed. Reports
kappa_ph(300 K, W) for both floors and the resulting Table-2 peak ZT (global optimum over the
production mu window and best value inside the polarized window mu-E_F < +1.0 eV).

Run:  ~/venvs/crn-te/bin/python scripts/phonon_floor3.py   ->  data/phonon_floor3.txt
"""
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from crnte import thermo as th  # noqa: E402
from crnte import phonon as ph  # noqa: E402
from crnte.monolayer_sk import SKParams  # noqa: E402

DATADIR = os.path.join(ROOT, "data")
MU = np.linspace(-0.6, 1.2, 361)          # production scan window (fig6_width_edge_vacancy.py)
T0 = 300.0
GEOS = [("zigzag", 8), ("zigzag", 14), ("zigzag", 20), ("armchair", 8), ("armchair", 14), ("armchair", 20)]


def peaks(E, Tu, Td, W, kph):
    up = th.sweep_mu(E, Tu, MU, T0)
    dn = th.sweep_mu(E, Td, MU, T0)
    zt = th.ZT(th.combine_spins(up, dn, T0), T0, kph)
    i = int(np.argmax(zt))
    pol = MU < 1.0
    j = int(np.argmax(np.where(pol, zt, -1.0)))
    return zt[i], MU[i], zt[j], MU[j]


def main():
    a = SKParams().a
    lines = ["# Phonon mode-floor check: kappa_ph(300 K) and Table-2 peak ZT with a 4-mode (production) vs 3-mode floor",
             "# edge N W(A) | kph4(nW/K) kph3(nW/K) dk(%) | ZT4_glob(mu) ZT3_glob(mu) dZT(%) | ZT4_pol(mu) ZT3_pol(mu) dZT(%)"]
    print("\n".join(lines))
    for edge, N in GEOS:
        d = np.load(os.path.join(DATADIR, f"{edge}_N{N}_TE.npz"))
        E, Tu, Td = d["E"], d["T_up"], d["T_dn"]
        W = ph.ribbon_width(edge, N, a)
        ph.N_FLOOR = 4.0
        k4 = ph.kappa_ph(T0, W)
        z4g, m4g, z4p, m4p = peaks(E, Tu, Td, W, k4)
        ph.N_FLOOR = 3.0
        k3 = ph.kappa_ph(T0, W)
        z3g, m3g, z3p, m3p = peaks(E, Tu, Td, W, k3)
        ph.N_FLOOR = 4.0
        row = (f"{edge:8s} {N:2d} {W:5.1f} | {k4*1e9:6.3f} {k3*1e9:6.3f} {100*(k3-k4)/k4:+5.1f} | "
               f"{z4g:.4f}({m4g:+.2f}) {z3g:.4f}({m3g:+.2f}) {100*(z3g-z4g)/z4g:+5.1f} | "
               f"{z4p:.4f}({m4p:+.2f}) {z3p:.4f}({m3p:+.2f}) {100*(z3p-z4p)/z4p:+5.1f}")
        print(row)
        lines.append(row)
    # low-T check: the floor dominates as T -> 0; report kappa/kappa_0 at 5 K for W = 18.6 A
    W = ph.ribbon_width("zigzag", 14, a)
    k0 = np.pi**2 * ph.KB**2 * 5.0 / (3.0 * 2 * np.pi * ph.HBAR)
    ph.N_FLOOR = 4.0; r4 = ph.kappa_ph(5.0, W) / k0
    ph.N_FLOOR = 3.0; r3 = ph.kappa_ph(5.0, W) / k0
    ph.N_FLOOR = 4.0
    tail = f"# low-T limit (5 K, zigzag N=14): kappa/kappa_0 = {r4:.3f} (floor 4), {r3:.3f} (floor 3)"
    print(tail)
    lines.append(tail)
    with open(os.path.join(DATADIR, "phonon_floor3.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("wrote data/phonon_floor3.txt")


if __name__ == "__main__":
    main()
