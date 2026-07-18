#!/usr/bin/env python
"""Regenerate ALL production transmissions on the unified fine grid (dE = 0.005 eV).

Every cached T(E) used by the manuscript comes from this one grid, so every quoted number is
grid-consistent. Also computes the reduced-manifold (no effective c orbital) comparison data
for the zigzag N=14 ribbon, used by the orbital-manifold caution figure.

Run:  ~/venvs/crn-te/bin/python scripts/run_all_transmissions.py
"""
import dataclasses
import os
import sys
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from crnte.monolayer_sk import SKParams  # noqa: E402
from crnte.ribbon_sk import build_ribbon_sk, transmission  # noqa: E402

DATADIR = os.path.join(ROOT, "data")
os.makedirs(DATADIR, exist_ok=True)
E_GRID = np.linspace(-1.2, 1.5, 541)      # unified production grid, dE = 0.005 eV


def compute(tag, p, edge, width):
    path = os.path.join(DATADIR, tag + ".npz")
    if os.path.exists(path):
        d = np.load(path)
        if d["E"].shape == E_GRID.shape and np.allclose(d["E"], E_GRID):
            print(f"cached  {tag}")
            return
    t0 = time.time()
    Tu = transmission(build_ribbon_sk(edge, width, p, +1), E_GRID)
    Td = transmission(build_ribbon_sk(edge, width, p, -1), E_GRID)
    np.savez(path, E=E_GRID, T_up=Tu, T_dn=Td)
    print(f"wrote   {tag}  ({time.time()-t0:.0f} s)")


def main():
    p = SKParams()
    for edge in ("zigzag", "armchair"):
        for N in (8, 14, 20):
            compute(f"{edge}_N{N}_TE", p, edge, N)
    # reduced-manifold comparison (c orbital pushed out of the window -> old 4-orbital model)
    p_nc = dataclasses.replace(p, eps_c=50.0, t_c1=0.0, t_c2=0.0, t_c3=0.0)
    compute("zigzag_N14_TE_noc", p_nc, "zigzag", 14)


if __name__ == "__main__":
    main()
