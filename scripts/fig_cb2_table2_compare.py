"""Results figure: Table-2 peak ZT (300 K) per geometry, single-c model (4-orbital Cr) vs the
two-band c1+c2 model, with the optimum chemical potential annotated. Reads the current
production caches (data/*_TE.npz, c1+c2) and the backed-up single-band caches
(data_backup_4band/*_TE.npz) if present. Writes figures/fig_cb2_table2_compare.png.
"""
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from crnte import thermo as th  # noqa: E402
from crnte.monolayer_sk import SKParams  # noqa: E402
from crnte.phonon import kappa_ph, ribbon_width  # noqa: E402

MU = np.linspace(-0.6, 1.2, 361)
T0 = 300.0
GEOS = [("zigzag", 8), ("zigzag", 14), ("zigzag", 20), ("armchair", 8), ("armchair", 14), ("armchair", 20)]


def peak(path, W):
    d = np.load(path)
    up = th.sweep_mu(d["E"], d["T_up"], MU, T0)
    dn = th.sweep_mu(d["E"], d["T_dn"], MU, T0)
    zt = th.ZT(th.combine_spins(up, dn, T0), T0, kappa_ph(T0, W))
    i = int(np.argmax(zt))
    return zt[i], MU[i]


def main():
    a = SKParams().a
    new, old = [], []
    for edge, N in GEOS:
        W = ribbon_width(edge, N, a)
        new.append(peak(os.path.join(ROOT, "data", f"{edge}_N{N}_TE.npz"), W))
        pb = os.path.join(ROOT, "data_backup_4band", f"{edge}_N{N}_TE.npz")
        old.append(peak(pb, W) if os.path.exists(pb) else (np.nan, np.nan))
    x = np.arange(len(GEOS))
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.bar(x - 0.19, [o[0] for o in old], 0.38, color="0.7", label="single conduction orbital $c$ (previous)")
    ax.bar(x + 0.19, [n[0] for n in new], 0.38, color="C0", label="two conduction orbitals $c_1,c_2$ (CB1+CB2)")
    for xi, (o, n) in enumerate(zip(old, new)):
        if not np.isnan(o[0]):
            ax.text(xi - 0.19, o[0] + 0.003, f"{o[1]:+.2f}", ha="center", fontsize=7, color="0.35")
        ax.text(xi + 0.19, n[0] + 0.003, f"{n[1]:+.2f}", ha="center", fontsize=7, color="C0")
    ax.set_xticks(x); ax.set_xticklabels([f"{e[0]}\n$N$={n}" for e, n in GEOS])
    ax.set_ylabel("peak $ZT$ (300 K)")
    ax.set_title("Global optimum per geometry; labels: $\\mu-E_F$ (eV) of the optimum")
    ax.axhline(0, color="k", lw=0.5)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    out = os.path.join(ROOT, "figures", "fig_cb2_table2_compare.png")
    fig.savefig(out, dpi=200)
    print("wrote", out)
    for (e, n), o, nn in zip(GEOS, old, new):
        print(f"{e:8s} {n:2d}  old {o[0]:.3f} ({o[1]:+.2f})  new {nn[0]:.3f} ({nn[1]:+.2f})")


if __name__ == "__main__":
    main()
