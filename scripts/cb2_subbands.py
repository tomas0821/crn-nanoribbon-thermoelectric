#!/usr/bin/env python
"""Where do the second-conduction-band (c2) subbands enter each ribbon? (Sec. 2.1, 3.3)

For every Table-2 geometry, take the pristine majority lead and, on a 10 meV grid from +0.30
to +0.80 eV, count the right-moving propagating modes and how many of them are c2-dominated
(more than half of the mode weight on the c2 orbitals). The c2 entry energy is the first grid
energy with a c2-dominated mode. The total mode count equals the pristine T_up(E), which gives
the zigzag N=14 3 -> 9 jump quoted in Sec. 3.3.

Run:  ~/venvs/crn-te/bin/python scripts/cb2_subbands.py  ->  data/cb2_subbands.txt
"""
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from crnte.monolayer_sk import SKParams  # noqa: E402
from crnte.ribbon_sk import build_ribbon_sk  # noqa: E402

DATADIR = os.path.join(ROOT, "data")
GEOS = [("zigzag", 8), ("zigzag", 14), ("zigzag", 20), ("armchair", 8), ("armchair", 14), ("armchair", 20)]
ENERGIES = np.round(np.arange(0.30, 0.805, 0.01), 2)
C1, C2 = 3, 4                          # orbital slots on Cr sites: d_z2, d_xz, d_yz, c1, c2


def mode_character(lead, E):
    """Number of right-moving modes at E and how many of them are c2-dominated."""
    off, c2 = 0, []
    for s in lead.sites[:lead.cell_size]:
        if s.family.norbs == 5:
            c2.append(off + C2)
        off += s.family.norbs
    modes, _ = lead.modes(energy=E)
    nprop = modes.wave_functions.shape[1] // 2
    if nprop == 0:
        return 0, 0
    w = np.abs(modes.wave_functions[:, nprop:]) ** 2    # outgoing (right-moving) half
    w /= w.sum(axis=0)
    return nprop, int(np.sum(w[c2].sum(axis=0) > 0.5))


def main():
    p = SKParams()
    out = ["# c2 subband entry per ribbon (majority lead, 10 meV grid, c2-dominated = c2 weight > 1/2)",
           "# geometry | c2 entry (eV) | modes / c2-modes at E = " + " ".join(f"{E:+.2f}" for E in ENERGIES[::5])]
    detail = []
    for edge, N in GEOS:
        lead = build_ribbon_sk(edge, N, p, +1).leads[0]
        counts = [mode_character(lead, float(E)) for E in ENERGIES]
        entry = next((E for E, (_, k) in zip(ENERGIES, counts) if k > 0), np.nan)
        out.append(f"{edge:8s} {N:2d} | {entry:+.2f} | " +
                   " ".join(f"{n}/{k}" for n, k in counts[::5]))
        detail.append(f"## {edge} N={N}: E modes c2-modes")
        detail += [f"{E:+.2f} {n:2d} {k:2d}" for E, (n, k) in zip(ENERGIES, counts)]
    text = "\n".join(out + [""] + detail) + "\n"
    print("\n".join(out))
    with open(os.path.join(DATADIR, "cb2_subbands.txt"), "w") as fh:
        fh.write(text)
    print("wrote data/cb2_subbands.txt")


if __name__ == "__main__":
    main()
