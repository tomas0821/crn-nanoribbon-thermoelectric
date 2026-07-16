#!/usr/bin/env python
"""Self-consistent edge magnetism of CrN nanoribbons (mean-field, reduced SK model).

Per-site Cr magnetic moment m_i across the ribbon width, from crnte.scf.ribbon_scf: the interior
recovers the bulk moment while the reduced-coordination EDGE Cr atoms carry enhanced moments --
the microscopic origin of the magnetic edges reported (by DMRG) for hexagonal CrN nanoribbons.

Run:  ~/venvs/crn-te/bin/python scripts/fig_edgemag.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from crnte.monolayer_sk import SKParams  # noqa: E402
from crnte import scf  # noqa: E402

FIGDIR = os.path.join(ROOT, "figures")
os.makedirs(FIGDIR, exist_ok=True)


def main():
    p = SKParams()
    configs = [("zigzag", 14, "C2", "o"), ("zigzag", 20, "C0", "s"), ("armchair", 14, "C1", "^")]

    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    for edge, N, col, mk in configs:
        r = scf.ribbon_scf(edge, N, p, nk=60)
        rows, m = r["rows"], r["m"]
        o = np.argsort(rows)
        # centre and normalise transverse coordinate to [0, N-1] site index
        x = np.arange(len(rows))
        ax.plot(x, m[o], mk + "-", color=col, lw=1.6, ms=6,
                label=f"{edge} N={N}  (edge {r['m_edge']:.2f}, bulk {r['m_interior']:.2f})")
        print(f"{edge} N={N}: interior m={r['m_interior']:.3f}, max edge m={r['m_edge']:.3f} "
              f"mu_B  ({100*(r['m_edge']/r['m_interior']-1):+.1f}% edge enhancement, {r['iters']} it)")

    ax.axhline(2.674, color="0.6", lw=0.8, ls=":", label="bulk monolayer (2.67)")
    ax.set_xlabel("Cr site index across the ribbon (edge → interior → edge)")
    ax.set_ylabel(r"self-consistent Cr moment $m_i$ ($\mu_B$)")
    ax.set_title("Edge magnetism: self-consistent Cr moments across CrN ribbons")
    ax.legend(frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    out = os.path.join(FIGDIR, "fig_edgemag.png")
    fig.savefig(out, dpi=200)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
