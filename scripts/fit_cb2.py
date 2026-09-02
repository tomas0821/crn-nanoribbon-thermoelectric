"""READY-TO-RUN SCAFFOLD (next work item): second effective conduction band CB2 + anticrossing.

Why: five of the six Table-2 global optima sit at mu-E_F = +1.05..1.09 eV, inside the window
where the single effective band c does not resolve CB2 (min ~+0.6 eV near M, Kuklin Fig. 2d)
or the CB1/CB2 anticrossing (the digitized CB1 dip to +0.37 eV at s = 0.75). Adding CB2 lets
those optima be quoted unconditionally (Sec. 3.4 observation (i)).

Model: two effective orbitals c1, c2 on the Cr triangular sublattice (both even under the
sheet mirror plane, hence still decoupled from N p_z), each with on-site + 1st..3rd-shell
hoppings, plus an on-site-diagonal inter-orbital coupling V_12 (k-independent, first
approximation) that opens the anticrossing:
    H_cc(k) = [[e1 + sum_n t1n S_n(k),  V12            ],
               [V12,                    e2 + sum_n t2n S_n(k)]]
Minority replicas shifted by delta_c (assumed = Delta_ex, as for c1).

Steps (each is small; total ~1 day):
 1. Digitize CB2 from data/kuklin_p4_300dpi-04.png with the SAME calibration as CB1
    (kuklin_targets.py header: E_F line y = 1091 px, 66.2 px/eV; k-columns Gamma = 646,
    M = 750, K = 853, Gamma' = 957 px) -> CB2_DIGITIZED below (s, E-E_F). ~15 points; make
    sure the two bands are assigned consistently through the anticrossing (follow band
    character/continuity, not energy ordering).
 2. Run this script: joint weighted LSQ of the lower/upper eigenvalues of H_cc to
    CB1_DIGITIZED + CB2_DIGITIZED (weights favouring E < 1.2 eV). Compare residuals with the
    single-band CB1_FIT; report V12 and the anticrossing gap.
 3. Wire into the model: SKParams gains eps_c2, t_c21..t_c23, v_c12; build_H -> 6x6
    (monolayer_sk.py); ribbon_sk.py adds the c2 sublattice orbital with the same shells and
    minority shift; scf.py untouched (c orbitals stay out of the moments loop).
 4. Regenerate: run_all_transmissions.py (tags *_TE.npz will be overwritten -- back up data/
    first), fig scripts, sensitivity.py (+4 params), pistar_pinned.py, fig_manifold_comparison.
 5. Manuscript: Sec. 2.1 (model), Table 1 (+5 rows), Sec. 3.4 (i) drop the CB2 caveat, Sec. 3.7
    Second, and every number in Table 2 / abstract / conclusions that moves.

Run:  ~/venvs/crn-te/bin/python scripts/fit_cb2.py
"""
import os
import sys

import numpy as np
from scipy.optimize import least_squares

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from crnte.kuklin_targets import CB1_DIGITIZED, CB1_FIT  # noqa: E402
from crnte.monolayer_sk import SKParams, lattice_geometry  # noqa: E402

# TODO(step 1): digitize CB2 (Kuklin Fig. 2d, second majority conduction band). Placeholder = empty.
CB2_DIGITIZED = [  # (s, E-E_F [eV])
]

# high-symmetry path Gamma-M-K-Gamma in fractional coords of (b1, b2) -- same as fig2_sk_bands.py
PATH = [np.array([0.0, 0.0]), np.array([0.5, 0.0]), np.array([1 / 3, 1 / 3]), np.array([0.0, 0.0])]


def k_of_s(s, b1, b2):
    seg = min(int(np.floor(s)), 2)
    f = PATH[seg] + (s - seg) * (PATH[seg + 1] - PATH[seg])
    return f[0] * b1 + f[1] * b2


def shells(a):
    a1, a2, _, _, _ = lattice_geometry(a)
    sh1 = [a1, a2, a2 - a1, -a1, -a2, a1 - a2]
    sh2 = [a1 + a2, 2 * a2 - a1, a2 - 2 * a1, -(a1 + a2), a1 - 2 * a2, 2 * a1 - a2]
    sh3 = [2 * v for v in sh1]
    return sh1, sh2, sh3


def S(k, vecs):
    return float(np.sum([np.cos(k @ v) for v in vecs]))


def two_band(k, x, sh):
    e1, t11, t12, t13, e2, t21, t22, t23, v12 = x
    s1, s2, s3 = (S(k, sh[0]), S(k, sh[1]), S(k, sh[2]))
    h = np.array([[e1 + t11 * s1 + t12 * s2 + t13 * s3, v12],
                  [v12, e2 + t21 * s1 + t22 * s2 + t23 * s3]])
    return np.linalg.eigvalsh(h)


def main():
    if not CB2_DIGITIZED:
        print("CB2_DIGITIZED is empty: do step 1 (digitize CB2 from data/kuklin_p4_300dpi-04.png) first.")
        print(f"CB1 single-band fit for reference: {CB1_FIT}")
        return
    p = SKParams()
    _, _, _, b1, b2 = lattice_geometry(p.a)
    sh = shells(p.a)
    pts = [(s, E, 0) for s, E in CB1_DIGITIZED] + [(s, E, 1) for s, E in CB2_DIGITIZED]

    def resid(x):
        r = []
        for s, E, band in pts:
            ev = two_band(k_of_s(s, b1, b2), x, sh)
            w = 3.0 if E < 1.2 else 1.0
            r.append(w * (ev[band] - E))
        return np.array(r)

    x0 = [CB1_FIT["eps_c"], CB1_FIT["t_c1"], CB1_FIT["t_c2"], CB1_FIT["t_c3"], 1.2, 0.2, 0.0, 0.0, 0.3]
    fit = least_squares(resid, x0)
    names = ["eps_c1", "t_c11", "t_c12", "t_c13", "eps_c2", "t_c21", "t_c22", "t_c23", "v_c12"]
    print("two-band fit:", {n: round(float(v), 4) for n, v in zip(names, fit.x)})
    print("rms residual (weighted):", float(np.sqrt(np.mean(fit.fun ** 2))))
    kK = k_of_s(2.0, b1, b2); kM = k_of_s(1.0, b1, b2); k75 = k_of_s(0.75, b1, b2)
    print("pocket at K:", two_band(kK, fit.x, sh), " M:", two_band(kM, fit.x, sh), " s=0.75:", two_band(k75, fit.x, sh))


if __name__ == "__main__":
    main()
