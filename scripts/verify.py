#!/usr/bin/env python
"""Internal verification checks: Wiedemann-Franz + monolayer<->ribbon band consistency."""
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from crnte import thermo as th  # noqa: E402
from crnte.monolayer_sk import SKParams, bands_along_path  # noqa: E402
from crnte.ribbon_sk import build_ribbon_sk  # noqa: E402

p = SKParams()

# ---------- Check 1: Wiedemann-Franz in the metallic regime ----------
# Lorenz number L = kappa_e/(G T) should approach 2.44e-8 W.Ohm/K^2 where transport is metallic
# and T(E) is smooth (deep in the majority band, below E_F).
d = np.load(os.path.join(ROOT, "data", "zigzag_N14_TE.npz"))
E, Tu, Td = d["E"], d["T_up"], d["T_dn"]
L0_lorenz = 2.44e-8
print("Check 1 - Wiedemann-Franz (metallic majority region, T=300 K):")
for mu in (-0.6, -0.4, -0.2):
    c = th.coefficients(E, Tu, mu, 300.0)   # majority channel only
    if c["G"] > 0:
        L = c["kappa_e"] / (c["G"] * 300.0)
        print(f"  mu-E_F={mu:+.2f}: L = kappa_e/(G T) = {L:.3e}  "
              f"(Lorenz {L0_lorenz:.2e}; ratio {L/L0_lorenz:.3f})")

# ---------- Check 2: monolayer <-> ribbon bulk-band consistency ----------
# The Bloch bands of a WIDE ribbon's lead should span the same energy range and minority gap
# as the standalone monolayer Hamiltonian (two independent implementations).
FRAC = [(0.0, 0.0), (0.5, 0.0), (2.0 / 3, 1.0 / 3), (0.0, 0.0)]
print("\nCheck 2 - monolayer vs wide-ribbon energy range & minority gap:")
for spin, name in ((+1, "majority"), (-1, "minority")):
    # monolayer
    _, emono, _ = bands_along_path(FRAC, p, spin, n_per_seg=300)
    mono_lo, mono_hi = emono.min(), emono.max()
    # wide ribbon lead Bloch bands (kwant handles the rectangular inter-cell hopping)
    import kwant
    lead = build_ribbon_sk("zigzag", 40, p, spin).leads[0]
    bands = kwant.physics.Bands(lead)
    evs = np.array([bands(k) for k in np.linspace(-np.pi, np.pi, 200)])
    rib_lo, rib_hi = evs.min(), evs.max()
    print(f"  {name}: monolayer [{mono_lo:+.2f},{mono_hi:+.2f}] eV | "
          f"wide ribbon [{rib_lo:+.2f},{rib_hi:+.2f}] eV")
    if spin == -1:
        # minority gap straddling E_F=0
        below = evs[evs < 0].max() if (evs < 0).any() else float("nan")
        above = evs[evs > 0].min() if (evs > 0).any() else float("nan")
        print(f"  minority ribbon gap around E_F: [{below:+.2f},{above:+.2f}] "
              f"= {above - below:.2f} eV  (monolayer target ~4.2 eV)")
