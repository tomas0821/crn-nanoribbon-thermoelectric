#!/usr/bin/env python
"""Compute and cache the intra-edge exchange constants J1, J2 (LKAG magnetic-force theorem).

Runs crnte.scf.edge_exchange for the zigzag and armchair N=14 ribbons and stores the results
in data/edge_exchange.txt (the numbers quoted in the manuscript's edge-magnetism section).

Run:  ~/venvs/crn-te/bin/python scripts/edge_exchange_run.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from crnte.monolayer_sk import SKParams  # noqa: E402
from crnte.scf import edge_exchange  # noqa: E402


def main():
    p = SKParams()
    lines = []
    for edge in ("zigzag", "armchair"):
        r = edge_exchange(edge, 14, p)
        line = (f"{edge} N=14: J1={r['J_lkag'][1]:+.2f} meV, J2={r['J_lkag'][2]:+.2f} meV "
                f"(Heisenberg J1/S^2={r['J_heis'][1]:+.2f}, J2/S^2={r['J_heis'][2]:+.2f}; "
                f"S={r['S']:.3f}, m_edge={r['m_edge']:.3f})")
        print(line)
        lines.append(line)
    with open(os.path.join(ROOT, "data", "edge_exchange.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("wrote data/edge_exchange.txt")


if __name__ == "__main__":
    main()
