#!/usr/bin/env python
"""Fig 2 (SK model): reduced multi-orbital h-CrN bands vs digitized Kuklin targets."""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crnte.monolayer_sk import SKParams, build_H, bands_along_path  # noqa: E402
from crnte import kuklin_targets as kt  # noqa: E402

FIGDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(FIGDIR, exist_ok=True)

FRAC = [(0.0, 0.0), (0.5, 0.0), (2.0 / 3, 1.0 / 3), (0.0, 0.0)]
LABELS = [r"$\Gamma$", "M", "K", r"$\Gamma$"]


def sanity_checks(p):
    rng = np.random.default_rng(0)
    for _ in range(20):
        k = rng.normal(size=2)
        for spin in (+1, -1):
            H = build_H(k, p, spin)   # orbital order: d_z2, d_xz, d_yz, c | p_z
            assert np.allclose(H, H.conj().T), "H not Hermitian"
            assert abs(H[0, 4]) < 1e-12, "d_z2 should be non-bonding w.r.t. p_z"
            assert abs(H[3, 4]) < 1e-12, "c should be decoupled from p_z"
    print("sanity: Hermitian OK, d_z2/c - p_z decoupling OK")


def main():
    p = SKParams()
    sanity_checks(p)

    fig, ax = plt.subplots(figsize=(5.6, 4.6))
    ticks = None
    for spin, style in ((+1, dict(color="k", lw=1.6, label=r"majority $\uparrow$")),
                        (-1, dict(color="m", lw=1.4, ls="--", label=r"minority $\downarrow$"))):
        x, e, ticks = bands_along_path(FRAC, p, spin)
        for b in range(e.shape[1]):
            ax.plot(x, e[:, b], **(style if b == 0 else {kk: v for kk, v in style.items()
                                                         if kk != "label"}))

    # digitized Kuklin Fig. 2d points (spin-up): conduction band CB1 and valence band VB1.
    # s in [0,3] is the equal-segment path coordinate Gamma-M-K-Gamma -> map to plot x.
    def s_to_x(s):
        seg = min(int(s), 2)
        return ticks[seg] + (s - seg) * (ticks[seg + 1] - ticks[seg])
    for pts, lab in ((kt.CB1_DIGITIZED, "digitized Kuklin CB1/VB1"),
                     (kt.VB1_DIGITIZED, None)):
        xs = [s_to_x(s) for s, _ in pts]
        es = [E for _, E in pts]
        ax.plot(xs, es, "o", ms=4, mfc="none", mec="C0", mew=1.2,
                label=lab if pts is kt.CB1_DIGITIZED else None)
    ax.axhline(0.0, color="0.5", lw=0.7, ls=":")
    ax.axhline(kt.MINORITY["vbm"], color="C3", lw=0.6, ls=":")
    ax.axhline(kt.MINORITY["cbm"], color="C3", lw=0.6, ls=":")
    ax.text(ticks[-1], 0.05, " $E_F$", fontsize=8, color="0.4", va="bottom")
    ax.text(ticks[-1], kt.MINORITY["cbm"] + 0.05, " min. CBM", fontsize=7, color="C3", va="bottom")
    ax.text(ticks[-1], kt.MINORITY["vbm"] + 0.05, " min. VBM", fontsize=7, color="C3", va="bottom")

    ax.set_xticks(ticks)
    ax.set_xticklabels(LABELS)
    for t in ticks:
        ax.axvline(t, color="0.9", lw=0.5, zorder=0)
    ax.set_xlim(ticks[0], ticks[-1])
    ax.set_ylim(-5.5, 3.0)
    ax.set_ylabel(r"$E - E_F$ (eV)")
    ax.set_title("h-CrN extended SK model vs digitized Kuklin bands")
    ax.legend(frameon=False, fontsize=9, loc="upper right")

    out = os.path.join(FIGDIR, "fig2_sk_bands.png")
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    _report(p)
    print(f"wrote {out}")


def _report(p):
    """Print model features vs targets."""
    feats = {}
    for spin, name in ((+1, "maj"), (-1, "min")):
        x, e, _ = bands_along_path(FRAC, p, spin, n_per_seg=400)
        feats[name] = e
    # majority: highest band max (VBM touching E_F?) and its value; K-point CBM
    maj = feats["maj"]
    print(f"  majority band-edge nearest E_F: max over bands/k below+above 0 = "
          f"[{maj.min():.2f}, {maj.max():.2f}] eV")
    mn = feats["min"]
    # minority gap: largest gap straddling E_F -> find occupied max (<0) and empty min (>0)
    below = mn[mn < 0]
    above = mn[mn > 0]
    if below.size and above.size:
        print(f"  minority VBM={below.max():+.2f} (target {kt.MINORITY['vbm']:+.1f}), "
              f"CBM={above.min():+.2f} (target {kt.MINORITY['cbm']:+.1f}), "
              f"gap={above.min() - below.max():.2f} (target {kt.MINORITY_GAP})")


if __name__ == "__main__":
    main()
