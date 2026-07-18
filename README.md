# CrN nanoribbon thermoelectric

Tight-binding + Landauer–Büttiker thermoelectric transport and spin filtering of hexagonal
(honeycomb) CrN nanoribbons. Theory/modelling paper for *Physica E*. **No fresh DFT** — the TB
model is parametrized entirely from published first-principles data: electronic bands digitized
from Kuklin et al., *Nanoscale* 9, 621 (2017), phonons digitized from Modarresi et al.,
*Phys. Rev. Applied* 11, 064015 (2019). See `NOVELTY_CHECK.md` for the (re-verified) novelty
position and `00_Master_Notebook.md` for the full lab log.

## Environment
Kwant does not build on the system Python 3.14. Use an isolated venv (see `requirements.txt`):
```bash
export PATH="$HOME/.local/bin:$PATH"
uv venv ~/venvs/crn-te --python 3.12
uv pip install --python ~/venvs/crn-te/bin/python -r requirements.txt
uv pip install --python ~/venvs/crn-te/bin/python --no-build-isolation kwant
```
Run everything with `~/venvs/crn-te/bin/python`.

## Layout
- `crnte/` — package: extended SK model (`monolayer_sk.py`: d+p_z manifold + effective
  conduction orbital `c` fitted to the digitized majority conduction pocket), Kwant ribbons
  (`ribbon_sk.py`), Onsager thermoelectrics (`thermo.py`), phonon-Landauer κ_ph (`phonon.py`),
  mean-field edge magnetism + LKAG exchange (`scf.py`), digitized reference targets
  (`kuklin_targets.py`).
- `scripts/` — `run_all_transmissions.py` (regenerates every production T(E) on one 5-meV
  grid), one script per manuscript figure, plus `verify.py`, `sensitivity.py`,
  `convergence.py`, `edge_exchange_run.py`.
- `figures/`, `data/` — generated figures and cached data (data is git-ignored; regenerable).
- `manuscript/` — Elsevier `elsarticle` LaTeX (self-contained; class + bst bundled), highlights,
  cover letter.
- `derivations/` — `derivations.tex`: step-by-step derivation of every formula (geometry,
  Slater–Koster selection rules, the effective conduction orbital, Onsager coefficients +
  units, Mott / Wiedemann–Franz, two-spin combination incl. the bipolar κ term, the
  phonon-Landauer κ_ph, mean-field magnetism + LKAG exchange).

## Status (2026-07-18): manuscript complete
**Model:** extended 5-orbital SK (Cr d_z², d_xz, d_yz + effective conduction orbital c | N p_z).
The reduced d+p_z manifold misses Kuklin's majority conduction pocket at K and fabricates a
sharp transmission edge → ~8× overestimated ZT; the paper quantifies this as a methodological
caution (`fig_manifold.png`).

**Honest results (300 K, phonon-Landauer κ_ph):** peak ZT = 0.04–0.15 with the global optimum
at the minority band edge (μ−E_F ≈ +1.05 eV); armchair N=8 uniquely combines its best ZT
(0.145, at −0.34 eV) with 100% spin polarization. The ribbons are outstanding spin filters
(minority gap [−3.2, +1.0] eV). Edge magnetism: interior moment 2.64 μ_B, edges +6–8%;
zigzag intra-edge exchange J1 = +59 meV (FM), J2 = +0.8 meV.
