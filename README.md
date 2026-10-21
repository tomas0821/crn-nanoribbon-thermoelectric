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
- `crnte/` — package: extended SK model (`monolayer_sk.py`: d+p_z manifold + two effective
  conduction orbitals `c1`, `c2` fitted to the traced majority conduction bands CB1/CB2 and
  their anticrossing), Kwant ribbons (`ribbon_sk.py`), spinful domain-wall junctions
  (`valve.py`), Onsager thermoelectrics (`thermo.py`), phonon-Landauer κ_ph (`phonon.py`),
  mean-field edge magnetism + LKAG exchange (`scf.py`), digitized reference targets
  (`kuklin_targets.py`).
- `scripts/` — `run_all_transmissions.py` (regenerates every production T(E) on one 5-meV
  grid), `digitize_cb2.py` + `fit_cb2.py` (band tracing and the two-orbital fit), one script
  per manuscript figure, plus `verify.py`, `sensitivity.py`, `sensitivity_armchair8.py`,
  `pistar_pinned.py`, `polarization_margin.py`, `phonon_floor3.py`, `ptype_scan.py`,
  `convergence.py`, `edge_exchange_run.py`; `regenerate_all.sh` runs the whole pipeline.
- `figures/`, `data/` — generated figures and data: the text outputs quoted in the paper
  (`data/*.txt`) are tracked; the transmission caches (`data/*.npz`) are git-ignored and regenerable.
- `manuscript/` — Elsevier `elsarticle` LaTeX (self-contained; class + bst bundled), highlights,
  cover letter.
- `derivations/` — `derivations.tex`: step-by-step derivation of every formula (geometry,
  Slater–Koster selection rules, the effective conduction orbital, Onsager coefficients +
  units, Mott / Wiedemann–Franz, two-spin combination incl. the bipolar κ term, the
  phonon-Landauer κ_ph, mean-field magnetism + LKAG exchange).

## Status (2026-10-21): submission-ready
**Model:** extended 6-orbital SK (Cr d_z², d_xz, d_yz + effective conduction orbitals c1, c2 |
N p_z). The reduced d+p_z manifold misses Kuklin's majority conduction bands, leaves the
majority channel empty between +0.19 eV and the minority edge, and overestimates ZT fivefold
(0.33 → 0.063, zigzag N=14); the paper quantifies this as a methodological caution
(`fig_manifold.png`).

**Results (300 K, phonon-Landauer κ_ph):** peak ZT = 0.06–0.15. Every global optimum lies
inside the fully spin-polarized window: on subband edges of the second conduction band
(μ−E_F ≈ +0.47 to +0.71 eV) for five geometries, and at −0.34 eV for armchair N=8, the best case
(0.145). The claim survives lowering the minority edge by 0.2 eV (P_G ≥ 99.6 %); a ±10 %
parameter sweep moves peak heights by about a factor of 2, and only Δ_ex −10 % yields a partly
polarized optimum (`data/polarization_margin.txt`). The ribbons are outstanding spin filters
(minority gap [−3.2, +1.0] eV). Edge magnetism: interior moment 2.64 μ_B, edges +6–8%;
zigzag intra-edge exchange J1 = +59 meV (FM), J2 = +0.8 meV.

**Thermally driven spin valve & domain walls:** the antiparallel (collinear, abrupt-wall)
configuration gives an exact OFF state over the whole half-metallic window
(`fig_spinvalve.png`). A full noncollinear domain-wall calculation shows continuous walls leak
well before that: half-transparency already at $\lambda_{1/2}\approx9$~\AA
(`fig_wall.png`). The published exchange and anisotropy scales (Modarresi 2019, the DMRG
paper) place the intrinsic wall width at $\lambda_{\rm int}\approx2.4$–$3$~nm, where a wall transmits
95–99 % of the parallel conductance at E_F (70–76 % at +0.5 eV) and sits $\sim$3$\times$ above $\lambda_{1/2}$ — so geometrically
constrained or spacer-separated junctions are required for a working OFF state, not merely
preferred.

**Review history:** three rounds of same-model referee-panel review
(`referee_report_2026-07-29.md`, `referee_report_2026-08-04.md`, round 3 logged in
`00_Master_Notebook.md`) and two cross-model panels (`cross_model_review_2026-08-25.md`,
`cross_model_review_2026-10-21.md`); all verified majors resolved.
