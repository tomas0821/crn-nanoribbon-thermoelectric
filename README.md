# CrN nanoribbon thermoelectric

Tight-binding + Landauer–Büttiker thermoelectric transport of hexagonal (honeycomb) CrN
nanoribbons. Theory/modelling paper for *Physica E*. **No DFT** — the TB model is parametrized
to published h-CrN band structures. See `paper_plan_crn-nanoribbon-thermoelectric.md` for the
full plan and `NOVELTY_CHECK.md` for the (re-verified) novelty position.

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
- `crnte/` — package: TB model, bands, transport + thermoelectric integrals.
- `scripts/` — one script per manuscript figure (`fig1_*` … `fig7_*`), plus `verify.py`,
  `sensitivity.py`, `convergence.py`.
- `figures/` — generated figures.
- `manuscript/` — Elsevier `elsarticle` LaTeX (self-contained; class + bst bundled).
- `derivations/` — `derivations.tex`: complete step-by-step derivation of every formula
  (geometry, Slater–Koster selection rules, Onsager coefficients + units, ZTₑ identity, Mott /
  Wiedemann–Franz, two-spin combination incl. the bipolar κ term, phonon quantum).

## Status
Provisional **effective** honeycomb model (Cr/N sublattices, spin-split Cr, one NN hopping),
tuned to the Kuklin et al. *Nanoscale* 9, 621 (2017) targets (a = 3.258 Å, 3.9 eV minority gap).
Full TB -> Kwant -> transport pipeline validated end-to-end.
- Fig 2 provisional (`scripts/fig2_monolayer_bands.py`) — cartoon 2-band bands (superseded).
- Fig 3 (`scripts/fig3_transmission.py`) — zigzag/armchair Landauer transmission T(E) (on cartoon).

### Faithful monolayer model (current)
`crnte/monolayer_sk.py` — reduced 4-orbital Slater-Koster model (Cr d_z2/d_xz/d_yz + N p_z),
fitted to the digitized Kuklin targets (`crnte/kuklin_targets.py`). See `scripts/fig2_sk_bands.py`.
Reproduces the half-metal (majority metallic, minority gapped, E_F inside the gap) and the
near-E_F features to within ~0.2-0.3 eV (digitization precision). The reduced out-of-plane
manifold passed the residual test -> no need for the full Cr-5d + N-3p set.
### Faithful ribbon transport (current)
`crnte/ribbon_sk.py` — zigzag/armchair CrN ribbons on the fitted SK model (multi-orbital Kwant:
Cr 3 orbitals, N 1). `scripts/fig3_sk_transmission.py` → spin-resolved T(E). Half-metallic
filtering (majority conducts at E_F, minority gapped ~[-3.2,+1.0] eV); sharp majority transmission
edge at E_F (promising for a large Seebeck).
### Thermoelectrics (current — headline result)
`crnte/thermo.py` (Onsager/Cutler-Mott, validated vs Mott) + `scripts/fig45_thermoelectric.py`
→ Figs 4-5. Zigzag N≈14: peak power factor at the sharp majority band edge (μ−E_F≈+0.19 eV);
**peak ZT≈0.48 at 300 K** (ballistic κ_ph, bracketed 0.26–0.85), rising with T. ZT peaks at the
half-metallic band edge (steep dT/dE). κ_ph→0 ZT_e is reported only as an upper bound (diverges
in the gap).
- **Next:** (a) self-consistent mean-field U for the inequivalent ribbon-EDGE Cr sites (spin
  Seebeck / edge magnetism; cross-check DMRG J1/J2); (b) width sweep N = 8, 14, 20; (c) armchair
  thermoelectrics; (d) edge-vacancy ZT enhancement.
