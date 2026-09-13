"""Trace the majority (spin-up) bands of Kuklin et al. Fig. 2(d) from the 300-dpi page render,
using the SAME calibration as the hand digitization of CB1 (crnte/kuklin_targets.py):
E_F dashed line at page-y 1091 px, 66.2 px/eV; k columns Gamma=646, M=750, K=853, Gamma'=957.

Outputs
  data/kuklin_fig2d_traces.npz : all dark-pixel band points (s, E) and per-column clusters
  figures/digitize_cb2_check.png : traces coloured by track id, CB1_DIGITIZED (red) and the
                                   fitted single c band (blue) overlaid -> calibration check
Run:  ~/venvs/crn-te/bin/python scripts/digitize_cb2.py
"""
import os
import sys

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from crnte.kuklin_targets import CB1_DIGITIZED, CB1_FIT  # noqa: E402
from crnte.monolayer_sk import SKParams, lattice_geometry, cr_shells  # noqa: E402

PNG = os.path.join(ROOT, "data", "kuklin_p4_300dpi-04.png")
Y_EF, PX_PER_EV = 1091.0, 66.2
X_G, X_M, X_K, X_G2 = 646, 750, 853, 957
E_MIN, E_MAX = -0.8, 2.8          # trace window (conduction bands + top of VB)


def s_of_x(x):
    if x <= X_M:
        return (x - X_G) / (X_M - X_G)
    if x <= X_K:
        return 1.0 + (x - X_M) / (X_K - X_M)
    return 2.0 + (x - X_K) / (X_G2 - X_K)


def c_band(s, fit, a):
    """Fitted single effective band eps_c + sum t_cn S_n along the path coordinate s."""
    a1, a2, _, b1, b2 = lattice_geometry(a)
    frac = [np.array([0.0, 0.0]), np.array([0.5, 0.0]), np.array([2 / 3, 1 / 3]), np.array([0.0, 0.0])]  # = FRAC of fig2_sk_bands.py
    seg = min(int(np.floor(s)), 2)
    f = frac[seg] + (s - seg) * (frac[seg + 1] - frac[seg])
    k = f[0] * b1 + f[1] * b2
    sh = cr_shells(a1, a2)
    S = lambda vecs: float(np.real(sum(np.exp(1j * k @ v) for v in vecs)))
    return fit["eps_c"] + fit["t_c1"] * S(sh[0]) + fit["t_c2"] * S(sh[1]) + fit["t_c3"] * S(sh[2])


def main():
    im = np.asarray(Image.open(PNG).convert("RGB")).astype(int)
    y_top = int(Y_EF - E_MAX * PX_PER_EV)
    y_bot = int(Y_EF - E_MIN * PX_PER_EV)
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    dark = (R < 110) & (G < 110) & (B < 110)
    # remove the dashed E_F line rows (bands crossing it are bridged by the tracker)
    dark[int(Y_EF) - 3:int(Y_EF) + 4, :] = False

    cols = {}
    for x in range(X_G + 2, X_G2 - 1):
        ys = np.where(dark[y_top:y_bot, x])[0] + y_top
        if ys.size == 0:
            continue
        # cluster consecutive rows
        runs, start = [], ys[0]
        for i in range(1, len(ys)):
            if ys[i] != ys[i - 1] + 1:
                runs.append((start, ys[i - 1])); start = ys[i]
        runs.append((start, ys[-1]))
        cols[x] = [0.5 * (a + b) for a, b in runs if (b - a) <= 12]   # skip blobs (labels)

    # greedy tracking: link nearest cluster in the next column within 6 px
    tracks = []  # list of lists of (x, y)
    active = []
    for x in sorted(cols):
        used = set()
        new_active = []
        for tr in active:
            xl, yl = tr[-1]
            if x - xl > 4:
                tracks.append(tr); continue
            cands = [(abs(y - yl), j) for j, y in enumerate(cols[x]) if j not in used and abs(y - yl) <= 6]
            if cands:
                _, j = min(cands); used.add(j); tr.append((x, cols[x][j])); new_active.append(tr)
            else:
                new_active.append(tr)
        for j, y in enumerate(cols[x]):
            if j not in used:
                new_active.append([(x, y)])
        active = new_active
    tracks += active
    tracks = [t for t in tracks if len(t) >= 15]

    pts = [(s_of_x(x), (Y_EF - y) / PX_PER_EV, i) for i, t in enumerate(tracks) for x, y in t]
    arr = np.array(pts)
    np.savez(os.path.join(ROOT, "data", "kuklin_fig2d_traces.npz"), s=arr[:, 0], E=arr[:, 1], track=arr[:, 2])

    fig, ax = plt.subplots(figsize=(7, 6))
    for i, t in enumerate(tracks):
        s = [s_of_x(x) for x, _ in t]; e = [(Y_EF - y) / PX_PER_EV for _, y in t]
        ax.plot(s, e, ".", ms=2, label=f"track {i} ({len(t)})")
        ax.text(s[len(s) // 2], e[len(e) // 2], str(i), fontsize=7)
    cb = np.array(CB1_DIGITIZED)
    ax.plot(cb[:, 0], cb[:, 1], "ro", ms=5, mfc="none", label="CB1_DIGITIZED (hand)")
    ss = np.linspace(0, 3, 300)
    ax.plot(ss, [c_band(s, CB1_FIT, SKParams().a) for s in ss], "b-", lw=1, label="fitted c band")
    ax.axhline(0, color="k", ls="--", lw=0.5)
    for xv in (1, 2):
        ax.axvline(xv, color="r", lw=0.5)
    ax.set_xticks([0, 1, 2, 3]); ax.set_xticklabels(["G", "M", "K", "G"])
    ax.set_ylim(E_MIN, E_MAX); ax.set_ylabel("E - E_F (eV)")
    ax.legend(fontsize=6, ncol=2)
    out = os.path.join(ROOT, "figures", "digitize_cb2_check.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"{len(tracks)} tracks; wrote {out}")
    for i, t in enumerate(tracks):
        s0, s1 = s_of_x(t[0][0]), s_of_x(t[-1][0])
        e = [(Y_EF - y) / PX_PER_EV for _, y in t]
        print(f"  track {i:2d}: s {s0:.2f}->{s1:.2f}  E {min(e):+.2f}..{max(e):+.2f}  n={len(t)}")


if __name__ == "__main__":
    main()
