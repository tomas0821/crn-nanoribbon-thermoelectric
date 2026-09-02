"""Extend the chemical-potential scan into the p-type side of the half-metallic window.

The production grid is E in [-1.2, +1.5] eV and the Table-2 scan is mu-E_F in [-0.6, +1.2] eV
(Sec. 3.5). Here T(E) is extended down to -2.0 eV (only the new energies are computed; the
cached production T(E) is reused verbatim) and mu is scanned over [-1.5, +1.2] eV at 300 K, so
that the Fermi window (+/-10 k_BT = 0.26 eV) is fully inside the grid down to mu = -1.5 eV.

Reports, per geometry: the global optimum over the extended window, the best fully polarized
optimum (mu-E_F < +1.0 eV), and whether either differs from the production values.

Run:  ~/venvs/crn-te/bin/python scripts/ptype_scan.py  ->  data/*_TE_ext.npz, data/ptype_scan.txt
"""
import os
import sys
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from crnte import thermo as th  # noqa: E402
from crnte.monolayer_sk import SKParams  # noqa: E402
from crnte.phonon import kappa_ph, ribbon_width  # noqa: E402
from crnte.ribbon_sk import build_ribbon_sk, transmission  # noqa: E402

DATADIR = os.path.join(ROOT, "data")
E_LOW = np.linspace(-2.0, -1.205, 160)     # dE = 5 meV, ends just below the production grid start
MU_EXT = np.linspace(-1.5, 1.2, 541)
MU_PROD = np.linspace(-0.6, 1.2, 361)
T0 = 300.0
GEOS = [("zigzag", 8), ("zigzag", 14), ("zigzag", 20), ("armchair", 8), ("armchair", 14), ("armchair", 20)]


def extended_TE(edge, N, p):
    prod = np.load(os.path.join(DATADIR, f"{edge}_N{N}_TE.npz"))
    path = os.path.join(DATADIR, f"{edge}_N{N}_TE_ext.npz")
    if os.path.exists(path):
        d = np.load(path)
        return d["E"], d["T_up"], d["T_dn"]
    t0 = time.time()
    Tu = transmission(build_ribbon_sk(edge, N, p, +1), E_LOW)
    Td = transmission(build_ribbon_sk(edge, N, p, -1), E_LOW)
    E = np.concatenate([E_LOW, prod["E"]])
    Tu = np.concatenate([Tu, prod["T_up"]])
    Td = np.concatenate([Td, prod["T_dn"]])
    np.savez(path, E=E, T_up=Tu, T_dn=Td)
    print(f"  computed {edge} N={N} low-E extension ({time.time()-t0:.0f} s)", flush=True)
    return E, Tu, Td


def scan(E, Tu, Td, W, MU):
    up = th.sweep_mu(E, Tu, MU, T0)
    dn = th.sweep_mu(E, Td, MU, T0)
    tot = th.combine_spins(up, dn, T0)
    zt = th.ZT(tot, T0, kappa_ph(T0, W))
    return zt, tot["S"] * 1e6, up, dn


def main():
    p = SKParams()
    out = ["# p-type extension of the mu scan: mu-E_F in [-1.5,+1.2] eV (production: [-0.6,+1.2]), 300 K, production kappa_ph(W)",
           "# edge N | prod_glob ZT(mu) | ext_glob ZT(mu) S(uV/K) | prod_pol ZT(mu) | ext_pol ZT(mu) S(uV/K) | best ZT with mu<-0.6: ZT(mu) S"]
    print("\n".join(out))
    for edge, N in GEOS:
        E, Tu, Td = extended_TE(edge, N, p)
        W = ribbon_width(edge, N, p.a)
        zt, S, up, dn = scan(E, Tu, Td, W, MU_EXT)
        ztp, _, _, _ = scan(E, Tu, Td, W, MU_PROD)
        ig = int(np.argmax(zt)); ipg = int(np.argmax(ztp))
        pol = MU_EXT < 1.0; polp = MU_PROD < 1.0
        ip = int(np.argmax(np.where(pol, zt, -1))); ipp = int(np.argmax(np.where(polp, ztp, -1)))
        new = MU_EXT < -0.6
        inew = int(np.argmax(np.where(new, zt, -1)))
        row = (f"{edge:8s} {N:2d} | {ztp[ipg]:.4f}({MU_PROD[ipg]:+.2f}) | {zt[ig]:.4f}({MU_EXT[ig]:+.2f}) {S[ig]:+6.0f} | "
               f"{ztp[ipp]:.4f}({MU_PROD[ipp]:+.2f}) | {zt[ip]:.4f}({MU_EXT[ip]:+.2f}) {S[ip]:+6.0f} | "
               f"{zt[inew]:.4f}({MU_EXT[inew]:+.2f}) {S[inew]:+6.0f}")
        print(row, flush=True)
        out.append(row)
    with open(os.path.join(DATADIR, "ptype_scan.txt"), "w") as fh:
        fh.write("\n".join(out) + "\n")
    print("wrote data/ptype_scan.txt")


if __name__ == "__main__":
    main()
