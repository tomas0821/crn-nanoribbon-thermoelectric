"""Two effective conduction orbitals (c1, c2) on the Cr triangular sublattice, fitted jointly to
the traced majority conduction bands CB1 and CB2 of Kuklin et al. Fig. 2(d)
(data/kuklin_fig2d_traces.npz from scripts/digitize_cb2.py; same calibration as CB1_DIGITIZED).

Model (both orbitals even under the sheet mirror plane -> still decoupled from N p_z):
    H_cc(k) = [[e1 + sum_n t1n S_n(k),  v12            ],
               [v12,                    e2 + sum_n t2n S_n(k)]]
with S_n the 1st..3rd Cr-Cr shell sums and a k-independent inter-orbital coupling v12 that
opens the CB1/CB2 anticrossing. Bands are assigned by ENERGY ORDER at each path coordinate s
(lower eigenvalue <-> lowest traced conduction band, upper <-> next), so no band-character
bookkeeping is needed through the anticrossing.

Outputs: data/cb2_fit.txt, figures/fit_cb2_check.png
Run:  ~/venvs/crn-te/bin/python scripts/fit_cb2.py
"""
import os
import sys

import numpy as np
from scipy.optimize import least_squares

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from crnte.kuklin_targets import CB1_DIGITIZED, CB1_FIT  # noqa: E402
from crnte.monolayer_sk import SKParams, lattice_geometry, cr_shells  # noqa: E402

PATH = [np.array([0.0, 0.0]), np.array([0.5, 0.0]), np.array([2 / 3, 1 / 3]), np.array([0.0, 0.0])]  # = FRAC of fig2_sk_bands.py
CONDUCTION_TRACKS = {0, 2, 4, 5, 6, 8, 9}   # from digitize_cb2.py output (1, 3, 7 are valence)
S_BIN = 0.05


def k_of_s(s, b1, b2):
    seg = min(int(np.floor(s)), 2)
    f = PATH[seg] + (s - seg) * (PATH[seg + 1] - PATH[seg])
    return f[0] * b1 + f[1] * b2


def shell_sums(k, sh):
    return [float(np.real(sum(np.exp(1j * k @ v) for v in vecs))) for vecs in sh]


def two_band(x, ssums):
    e1, t11, t12, t13, e2, t21, t22, t23, v12 = x
    s1, s2, s3 = ssums
    h = np.array([[e1 + t11 * s1 + t12 * s2 + t13 * s3, v12],
                  [v12, e2 + t21 * s1 + t22 * s2 + t23 * s3]])
    return np.linalg.eigvalsh(h)


def build_targets():
    d = np.load(os.path.join(ROOT, "data", "kuklin_fig2d_traces.npz"))
    s, E, tr = d["s"], d["E"], d["track"].astype(int)
    m = np.isin(tr, list(CONDUCTION_TRACKS))
    s, E, tr = s[m], E[m], tr[m]
    lower, upper = [], []
    for b in np.arange(0.0, 3.0, S_BIN):
        sel = (s >= b) & (s < b + S_BIN)
        if not sel.any():
            continue
        # one representative energy per track in this bin, then order by energy
        vals = sorted(float(np.median(E[sel & (tr == t)])) for t in np.unique(tr[sel]))
        sc = b + S_BIN / 2
        lower.append((sc, vals[0]))
        if len(vals) > 1:
            upper.append((sc, vals[1]))
    return np.array(lower), np.array(upper)


def main():
    p = SKParams()
    a1, a2, _, b1, b2 = lattice_geometry(p.a)
    sh = cr_shells(a1, a2)
    lower, upper = build_targets()
    print(f"targets: {len(lower)} lower-band points, {len(upper)} upper-band points")
    pts = [(s, E, 0) for s, E in lower] + [(s, E, 1) for s, E in upper]
    ssums = {s: shell_sums(k_of_s(s, b1, b2), sh) for s, _, _ in pts}

    def w(E):
        return 3.0 if E < 1.2 else 1.0

    def resid(x):
        return np.array([w(E) * (two_band(x, ssums[s])[band] - E) for s, E, band in pts])

    x0 = [CB1_FIT["eps_c"], CB1_FIT["t_c1"], CB1_FIT["t_c2"], CB1_FIT["t_c3"], 1.5, 0.25, 0.0, 0.0, 0.3]
    fit = least_squares(resid, x0)
    x = fit.x
    names = ["eps_c1", "t_c11", "t_c12", "t_c13", "eps_c2", "t_c21", "t_c22", "t_c23", "v_c12"]
    res = resid(x)
    rms_low = float(np.sqrt(np.mean([(two_band(x, ssums[s])[0] - E) ** 2 for s, E in lower])))
    rms_up = float(np.sqrt(np.mean([(two_band(x, ssums[s])[1] - E) ** 2 for s, E in upper])))
    win = [(s, E, b) for s, E, b in pts if E < 1.2]
    rms_win = float(np.sqrt(np.mean([(two_band(x, ssums[s])[b] - E) ** 2 for s, E, b in win])))
    # single-band reference on the same lower targets
    x_single = [CB1_FIT["eps_c"], CB1_FIT["t_c1"], CB1_FIT["t_c2"], CB1_FIT["t_c3"], 50.0, 0, 0, 0, 0.0]
    rms_single = float(np.sqrt(np.mean([(two_band(x_single, ssums[s])[0] - E) ** 2 for s, E in lower if E < 1.2])))

    def at(sv):
        return two_band(x, shell_sums(k_of_s(sv, b1, b2), sh))
    lines = ["# two-band fit of Kuklin Fig. 2(d) majority conduction bands (energies eV, rel. E_F)"]
    lines += [f"{n} = {v:.4f}" for n, v in zip(names, x)]
    lines += [f"rms residual lower band = {rms_low:.3f} eV; upper band = {rms_up:.3f} eV; transport window (E<1.2) = {rms_win:.3f} eV",
              f"single-band CB1_FIT rms on the same lower targets (E<1.2) = {rms_single:.3f} eV",
              f"lower/upper at Gamma = {at(0.0).round(3)}, at M = {at(1.0).round(3)}, at K = {at(2.0).round(3)}, at s=0.75 = {at(0.75).round(3)}",
              f"anticrossing gap min over s = {min(np.diff(at(sv))[0] for sv in np.linspace(0, 3, 601)):.3f} eV"]
    print("\n".join(lines))
    with open(os.path.join(ROOT, "data", "cb2_fit.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")

    ss = np.linspace(0, 3, 400)
    ev = np.array([at(sv) for sv in ss])
    fig, ax = plt.subplots(figsize=(7, 5.5))
    ax.plot(lower[:, 0], lower[:, 1], "k.", ms=4, label="traced CB1 (lower)")
    ax.plot(upper[:, 0], upper[:, 1], "g.", ms=4, label="traced CB2 (upper)")
    cb = np.array(CB1_DIGITIZED)
    ax.plot(cb[:, 0], cb[:, 1], "ro", ms=5, mfc="none", label="CB1_DIGITIZED (hand)")
    ax.plot(ss, ev[:, 0], "b-", lw=1.2, label="fit: lower")
    ax.plot(ss, ev[:, 1], "m-", lw=1.2, label="fit: upper")
    ax.plot(ss, [two_band(x_single, shell_sums(k_of_s(sv, b1, b2), sh))[0] for sv in ss], "b--", lw=0.8, label="single c band (current)")
    ax.axhline(0, color="k", ls="--", lw=0.5)
    for xv in (1, 2):
        ax.axvline(xv, color="r", lw=0.5)
    ax.set_xticks([0, 1, 2, 3]); ax.set_xticklabels(["G", "M", "K", "G"]); ax.set_ylim(-0.6, 3.0)
    ax.set_ylabel("E - E_F (eV)"); ax.legend(fontsize=7)
    fig.savefig(os.path.join(ROOT, "figures", "fit_cb2_check.png"), dpi=150, bbox_inches="tight")
    print("wrote data/cb2_fit.txt, figures/fit_cb2_check.png")


if __name__ == "__main__":
    main()
