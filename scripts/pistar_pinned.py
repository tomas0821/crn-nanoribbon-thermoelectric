#!/usr/bin/env python
"""pi*-pinned sensitivity case: what if the majority pi* valence-band top sat at the DFT value?

The fitted model places the majority pi* top at +0.19 eV (at K), whereas the DFT reference has
it at ~0 eV (inside the Gamma-M / K-Gamma intervals). The referee-relevant question: how much do
the IN-WINDOW (fully polarized) thermoelectric optima depend on those extra +0-0.19 eV majority
states?  Variant: eps_pi -> eps_pi - 0.19 eV together with delta_ex -> delta_ex + 0.19 eV, which
lowers the majority pi* manifold by 0.19 eV (pinning its top to ~0) while keeping the minority
pi edge (eps_pi + delta_ex = +1.0 eV) - i.e. the half-metallic window - fixed. (The minority
d_z2 flat level moves +1.3 -> +1.49 eV; both are above the window edge.)

Recomputes the polarized-window and global optima for all six ribbons at 300 K.

Run:  ~/venvs/crn-te/bin/python scripts/pistar_pinned.py
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
E_GRID = np.linspace(-0.8, 1.5, 461)
MU = np.linspace(-0.6, 1.2, 361)
T0 = 300.0
SHIFT = 0.19


def optima(edge, N, p, tag):
    key = os.path.join(DATADIR, f"pistar_{tag}_{edge}_N{N}.npz")
    if os.path.exists(key):
        dd = np.load(key)
        Tu, Td = dd["Tu"], dd["Td"]
    else:
        Tu = transmission(build_ribbon_sk(edge, N, p, +1), E_GRID)
        Td = transmission(build_ribbon_sk(edge, N, p, -1), E_GRID)
        np.savez(key, Tu=Tu, Td=Td)
    W = ribbon_width(edge, N, p.a)
    up = th.sweep_mu(E_GRID, Tu, MU, T0)
    dn = th.sweep_mu(E_GRID, Td, MU, T0)
    tot = th.combine_spins(up, dn, T0)
    zt = th.ZT(tot, T0, kappa_ph(T0, W))
    ig = int(np.argmax(zt))
    mask = MU < 1.0
    ip = int(np.argmax(np.where(mask, zt, -1.0)))
    return (zt[ig], MU[ig]), (zt[ip], MU[ip])


def main():
    base = SKParams()
    pinned = dataclasses.replace(base, eps_pi=base.eps_pi - SHIFT,
                                 delta_ex=base.delta_ex + SHIFT)
    lines = ["edge N | baseline global (mu) | pinned global (mu) | "
             "baseline polarized (mu) | pinned polarized (mu)"]
    print(lines[0], flush=True)
    for edge in ("zigzag", "armchair"):
        for N in (8, 14, 20):
            (g0, mg0), (p0, mp0) = optima(edge, N, base, "base")
            (g1, mg1), (p1, mp1) = optima(edge, N, pinned, "pinned")
            line = (f"{edge:9s}{N:3d} | {g0:.4f} ({mg0:+.2f}) | {g1:.4f} ({mg1:+.2f}) | "
                    f"{p0:.4f} ({mp0:+.2f}) | {p1:.4f} ({mp1:+.2f})")
            lines.append(line)
            print(line, flush=True)
    with open(os.path.join(DATADIR, "pistar_pinned.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("wrote data/pistar_pinned.txt")


if __name__ == "__main__":
    main()
