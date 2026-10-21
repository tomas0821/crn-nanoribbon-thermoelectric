"""How robust is "every optimum lies inside the fully spin-polarized window"?

Two checks, both on cached transmissions (nothing is recomputed in Kwant):

1. Sensitivity variants. For every +/-10% variant of the zigzag N=14 and armchair N=8 sweeps
   (data/sens_*.npz, data/sensA8_*.npz, written by scripts/sensitivity*.py) report the global
   300 K optimum, its conductance polarization P_G (thermally smeared), and the best ZT among
   chemical potentials where the current is fully polarized (P_G > 99.9%).

2. Minority-edge margin. Shift the production minority transmission T_dn(E) of every Table-2
   geometry rigidly down by dE = 0.1/0.2/0.3 eV (mimicking a lower minority conduction edge,
   e.g. the reported +0.9 eV instead of the model's +1.0 eV) and report P_G at the baseline
   optimum (300 and 700 K) and the new global optimum. The rigid shift reproduces the explicit
   Delta_ex -10% variant (dE = 0.36 eV) to within 0.1% in P_G. Scan restricted to
   mu-E_F <= +1.0 eV so the shifted T_dn never needs data above the cached grid (+1.5 eV).

Run:  ~/venvs/crn-te/bin/python scripts/polarization_margin.py  ->  data/polarization_margin.txt
"""
import glob
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from crnte import thermo as th  # noqa: E402
from crnte.monolayer_sk import SKParams  # noqa: E402
from crnte.phonon import kappa_ph, ribbon_width  # noqa: E402

DATADIR = os.path.join(ROOT, "data")
T0 = 300.0
FULL = 0.999                              # "fully polarized": P_G > 99.9%
GEOS = [("zigzag", 8), ("zigzag", 14), ("zigzag", 20), ("armchair", 8), ("armchair", 14), ("armchair", 20)]

# grids of the two sensitivity scripts
SWEEPS = {
    "zigzag N=14": ("sens_*.npz", "zigzag", 14, np.linspace(-0.6, 1.5, 421), np.linspace(-0.4, 1.2, 321)),
    "armchair N=8": ("sensA8_*.npz", "armchair", 8, np.linspace(-0.8, 1.5, 461), np.linspace(-0.6, 1.2, 361)),
}
BASE = SKParams()
PARS = ["eps_dz2", "eps_pi", "eps_pz", "pdpi", "t_zz", "delta_ex", "eps_c", "t_c1", "t_c2", "t_c3",
        "eps_c2", "t_c21", "t_c22", "t_c23", "v_c12"]


def polarization(E, Tu, Td, mu, T):
    """Thermally smeared conductance polarization P_G at each chemical potential."""
    w = th.dfermi(E[None, :], np.atleast_1d(mu)[:, None], T)
    gu = np.trapz(w * Tu[None, :], E, axis=1)
    gd = np.trapz(w * Td[None, :], E, axis=1)
    return (gu - gd) / (gu + gd)


def minority_onset(E, Td):
    """First energy above E_F where the minority transmission exceeds 1/2."""
    return E[np.argmax((E > 0) & (Td > 0.5))]


def scan(E, Tu, Td, MU, T, kph):
    up = th.sweep_mu(E, Tu, MU, T)
    dn = th.sweep_mu(E, Td, MU, T)
    zt = th.ZT(th.combine_spins(up, dn, T), T, kph)
    pg = polarization(E, Tu, Td, MU, T)
    i = int(np.argmax(zt))
    j = int(np.argmax(np.where(pg > FULL, zt, -1.0)))
    return zt[i], MU[i], pg[i], zt[j], MU[j]


def variant_label(path):
    """Name the single parameter that differs from the baseline in a sensitivity file name."""
    tag = os.path.basename(path)[:-4]
    for par in PARS:
        m = re.search(rf"_{par}([+-]\d+p\d+)(?=_|$)", tag) or re.search(rf"^sens(?:A8)?_{par}([+-]\d+p\d+)", tag)
        if m is None:
            continue
        val = float(m.group(1).replace("p", "."))
        ref = getattr(BASE, par)
        if not np.isclose(val, ref, atol=5e-5):
            return f"{par} {'+' if abs(val) > abs(ref) else '-'}10%"
    return "baseline"


def main():
    a = BASE.a
    out = ["# Polarization robustness of the ZT optima (300 K unless stated; P_G thermally smeared)",
           f"# 'pol' = best ZT where P_G > {100 * FULL:.1f}%", ""]
    for name, (pat, edge, N, E, MU) in SWEEPS.items():
        kph = kappa_ph(T0, ribbon_width(edge, N, a))
        out.append(f"## sensitivity variants, {name}: variant | global ZT (mu) P_G | pol ZT (mu) | minority onset")
        rows = []
        for f in sorted(glob.glob(os.path.join(DATADIR, pat))):
            if pat.startswith("sens_") and os.path.basename(f).startswith("sensA8_"):
                continue
            if os.path.basename(f).startswith("sensdc_"):
                continue
            d = np.load(f)
            zg, mg, pg, zp, mp = scan(E, d["Tu"], d["Td"], MU, T0, kph)
            rows.append((variant_label(f), zg, mg, pg, zp, mp, minority_onset(E, d["Td"])))
        for lab, zg, mg, pg, zp, mp, eo in sorted(rows):
            flag = "" if pg > FULL else "   <-- not fully polarized"
            out.append(f"{lab:14s} | {zg:.4f} ({mg:+.3f}) {100 * pg:5.1f}% | {zp:.4f} ({mp:+.3f}) | {eo:+.3f}{flag}")
        pol = [r[4] for r in rows]
        out.append(f"spread of global optima [{min(r[1] for r in rows):.4f}, {max(r[1] for r in rows):.4f}];"
                   f" fully polarized optima [{min(pol):.4f}, {max(pol):.4f}]")
        out.append("")

    MU = np.linspace(-0.6, 1.0, 321)
    out.append("## minority edge shifted down by dE (rigid shift of T_dn), production T(E), mu <= +1.0 eV")
    out.append("# geometry | minority onset | base opt ZT (mu) | dE: P_G at base opt 300 K / 700 K ; new global ZT (mu) P_G")
    for edge, N in GEOS:
        d = np.load(os.path.join(DATADIR, f"{edge}_N{N}_TE.npz"))
        E, Tu, Td = d["E"], d["T_up"], d["T_dn"]
        kph = kappa_ph(T0, ribbon_width(edge, N, a))
        z0, m0, _, _, _ = scan(E, Tu, Td, MU, T0, kph)
        cells = []
        for dE in (0.1, 0.2, 0.3):
            Ts = np.interp(E + dE, E, Td)
            p300 = polarization(E, Tu, Ts, m0, 300.0)[0]
            p700 = polarization(E, Tu, Ts, m0, 700.0)[0]
            zg, mg, pg, _, _ = scan(E, Tu, Ts, MU, T0, kph)
            cells.append(f"{dE:.1f}: {100 * p300:6.2f}/{100 * p700:5.1f}% ; {zg:.4f} ({mg:+.2f}) {100 * pg:5.1f}%")
        out.append(f"{edge:8s} {N:2d} | {minority_onset(E, Td):+.3f} | {z0:.4f} ({m0:+.2f}) | " + " | ".join(cells))

    text = "\n".join(out) + "\n"
    print(text)
    with open(os.path.join(DATADIR, "polarization_margin.txt"), "w") as fh:
        fh.write(text)
    print("wrote data/polarization_margin.txt")


if __name__ == "__main__":
    main()
