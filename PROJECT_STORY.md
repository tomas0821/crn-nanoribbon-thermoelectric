# PROJECT_STORY — CrN nanoribbon thermoelectric

*Re-immersion narrative, written 2026-08-03 (walkthrough session). Reading this should take
~10 minutes and restore full context. Companion files: `00_Master_Notebook.md` (the spine,
run-by-run), `referee_report_2026-07-29.md` (round-1 panel), `NOVELTY_CHECK.md` (claim
provenance). Figures referenced by filename live in `figures/`.*

---

## Phase 1 — The gap and the bet (2026-07-14)

The project began as publication strategy, not physics: a lit-gap analysis of *Physica E*
found that the nanoribbon-thermoelectric template (transmission → Seebeck, power factor, ZT
versus gate/width/edge) is densely populated for graphene, silicene, phosphorene, SiC — and
empty for CrN, despite CrN being an established thin-film thermoelectric and 2D h-CrN being an
actively studied half-metal. The novelty check surfaced exactly one adjacent work: Kupczyński
et al., PRB 107, 205418 (2023), DFT+DMRG magnetism of zigzag h-CrN nanoribbon edges. A
recorded correction matters here: that paper *does* compute transport (semiclassical Boltzmann,
perfect spin filtering) — so our claim is "first **thermoelectric** / first **phase-coherent
Landauer**" study, never "first transport". Two structural bets were locked in: **no fresh
DFT** (parametrize everything from published first-principles data: bands from Kuklin 2017,
phonons from Modarresi 2019 — the lightweight-analytics register is the genre and the
differentiation), and the DMRG paper recast as an asset — its width convention, its J₁/J₂, and
its half-metallic edges became validation targets.

## Phase 2 — Building the machine, and its first wrong answer (2026-07-14/15)

Mirror symmetry of the planar sheet decouples out-of-plane from in-plane orbitals, and
Kuklin's projected DOS puts the states at E_F in the out-of-plane set — so the "natural"
minimal basis is Cr d_z², d_xz, d_yz + N p_z with exact Slater–Koster selection rules
(N p_z ↔ d_xz/d_yz via V_pdπ only; d_z² non-bonding, dispersing via t_zz). Magnetism enters
as a rigid Stoner splitting Δ_ex = 3.6 eV fixed by the reported minority conduction edge.
Three separate modules: Hamiltonian/Kwant transport (`crnte/ribbon_sk.py`), Onsager integrals
(`crnte/thermo.py`), self-consistent site-resolved mean-field magnetism + LKAG exchange
(`crnte/scf.py`). The magnetism results are still current in the paper: edge Cr moments
enhanced ~5–8% width-independently (`fig_edgemag.png`), zigzag intra-edge J₁ = +59 meV FM with
|J₁| ≫ |J₂| — same sign and hierarchy as DMRG (J₁ ≈ 10–12 meV), overestimated ~5×, as an
analytic model should honestly expect. Two errors were made. Caught immediately: the width
convention (a "N=14" zigzag was actually 29 rows, manufacturing a spurious "zigzag beats
armchair" rule; fixed 07-15, all rerun). Not caught: the reduced manifold produced a sharp
majority band edge at +0.2 eV and on it a headline ZT ≈ 0.23–0.33 that a full ±10%
sensitivity sweep declared robust. Manuscript v1 was drafted on those numbers — reasonable
with what was known then; sensitivity-within-a-basis is blind to what the basis omits.

## Phase 3 — The audit crisis and the honest model (2026-07-17)

A full pre-submission audit re-read Kuklin's Fig. 2(d) against the model and found the flaw:
the reference band structure has a **majority conduction band with an electron pocket at K**
(CBM −0.2 eV) whose orbital weight (Cr d_xy/d_x²−y²/s) lies *outside* the out-of-plane
manifold. The model's sharp majority edge at +0.2 eV — and the ZT ≈ 0.33 built on it — was a
basis-truncation artifact. The fix stayed inside the no-DFT rules: digitize CB1 from a 300-dpi
render (18 path points, ±0.1 eV in the transport window; `crnte/kuklin_targets.py`), add one
effective conduction orbital c on the Cr sublattice (symmetry-decoupled from N p_z) with
weighted-least-squares hoppings ε_c = 0.915, t_c1 = 0.285, t_c2 = −0.028, t_c3 = 0.030 eV.
Simultaneously κ_ph was upgraded from the flat 4κ₀T guess to a real ballistic phonon-Landauer
mode count anchored to Modarresi's DFPT dispersion (`crnte/phonon.py`; ZA quadratic with
α ≈ 44 THz Å², sine-form branches, κ_ph(300 K) = 0.6–1.7 nW/K for W = 10–32 Å). On the
extended model the honest landscape (`data/`, Table 2, `fig5_zt.png`, `fig6_designrules.png`):
peak ZT = 0.040 (zigzag N=14) to 0.145 (armchair N=8) at 300 K, global optima pinned to the
minority conduction edge at μ ≈ +1.05–1.09 eV — except **armchair N=8, whose optimum
(ZT = 0.145 at μ = −0.34 eV, S = −114 μV/K) lies inside the 100%-polarized window**
(`fig_armchair8.png`). The collapse 0.33 → 0.040 with sensitivity analysis unable to detect it
became a *contribution* of the paper (`fig_manifold.png`), and the manuscript was rewritten
around the honest numbers plus the spin-filter story (minority gap [−3.2, +1.0] eV; P_G = 100%
for any gating below +1 eV; T↑(E_F) = 8 for zigzag N=14).

## Phase 4 — The thermal spin valve and the wall (2026-07-18)

Looking for functionality stronger than filtering: put the two halves of a ribbon (and leads)
in **collinear antiparallel** magnetization. Each spin species is then majority on one side but
sits inside the minority gap on the other — no propagating states to transmit into — so
T_AP(E) = 0 *identically* over the whole half-metallic window. This is an exact lead-spectrum
zero (numerics: machine zero; `fig_spinvalve.png`), not a large-but-finite suppression: a
thermally driven spin valve in a single material. The honesty question: how sharp must the
reversal be? A fully spinful noncollinear calculation (`crnte/valve.py`, Walker profile,
exchange field rotating on Cr orbitals) answered — after a lead-placement bug was caught
(Kwant attaches a lead on the side its symmetry vector points toward; the θ=0 lead sat on the
wrong side and faked an OFF state at ALL widths; caught by a 1D textbook test and a
uniform-rotation invariance check). Honest result (`fig_wall.png`): the exact zero exists only
at λ = 0; the sharpest finite texture (~1 Å) already leaks T_AP ≈ 0.7 (ON/OFF ~10); half
transparency at λ_1/2 ≈ 9 Å; walls ≳3 nm fully transparent (adiabatic limit reached exactly).
So the device needs junctions with *no continuous texture*: geometrically constrained walls
(Bruno 1999) or a nonmagnetic spacer — precisely the CrN/P/CrN geometry of Modarresi 2019.
Eight literature anchors were Crossref-verified and added (Cabrera–Falicov, Tatara, van Hoof,
Bruno, Coey, Mathur, Walter, Liebing). The one unbacked number — the intrinsic wall width
λ_int = π√(A/K) — needs the magnetocrystalline anisotropy K of h-CrN (spin-orbit, unreported);
a noncollinear DFT+U+SOC calculation of K was *planned and deliberately not run* (validation
would be future work; the paper's methodology stays TB+Landauer).

## Phase 5 — Pipeline adoption and novelty hygiene (2026-07-27)

Infrastructure, not physics: the project was retrofitted into the research pipeline
(Portfolio-Base YAML in CLAUDE.md; Zotero collection CrN-nanoribbon-TE mirroring refs.bib
1:1; 12 of 26 papers converted to `papers_md/` with per-paper verification — including the
DMRG paper, whose citable numbers J₁ = 10–12 meV / J₂ = −2…0 meV / anisotropy 0.73 meV
survived conversion verbatim). The final pre-submission novelty re-check ran the recorded
queries across all four databases: **CLEAN** — the only CrN-nanoribbon paper in existence
remains the DMRG one we cite and differentiate.

## Phase 6 — The referee panel and the round-1 revision (2026-07-29 → 2026-08-01)

Before paying three months for a real referee round, a four-referee adversarial panel (methods,
novelty, results/figures, journal-fit) read the full draft; every MAJOR finding faced an
independent refutation agent. Outcome (`referee_report_2026-07-29.md`): verdict *major
revisions*; 21 of 23 majors survived verification (two were killed — one by recomputation from
cached data), 27 minors. What survived attack: the priority claim (independent duplication
test), the formalism, the collinear AP zero, the manifold caution, Table-2↔figure consistency.
The real defects clustered in three groups: honesty-of-numbers (a κ_ph bracket in the text,
"0.02–0.08", contradicted the paper's own figure — it was a copy of the *sensitivity* spread;
the abstract contradicted Table 2 about where the largest response sits; the flagship 0.145
had no uncertainty and no figure; the "~1 nm" wall criterion misread `fig_wall`),
reproducibility (methods underspecified: fit targets, digitization protocol, U_eff, ZA branch,
LKAG contour, convergence evidence), and positioning (nanoribbon spin-caloritronics prior art
uncited; abstract sold prior-art spin filtering without attribution; T_C never mentioned).
All fixes were implemented 2026-08-01, including two new computations. (1) The armchair-N=8
±10% sweep: one-sided spread [0.13, 0.28] — the flagship never falls below 0.13
(`data/sensitivity_armchair8.txt`). (2) The **π*-pinned variant** (ε_π → ε_π − 0.19 eV,
Δ_ex → Δ_ex + 0.19 eV: majority π* top pinned to the DFT value, half-metallic window
unchanged): minority-edge global optima drop by factors 1.2–4 and the zigzag in-window optima
at +0.12/+0.08 eV — which sat on the spurious π* states — vanish, **but the armchair N=8
optimum is untouched, 0.145 → 0.145** (`data/pistar_pinned.txt`). The paper's most promoted
number is robust against its known systematic; the rest are declared order-of-magnitude.
Also: T_C ≈ 209 K (Modarresi RPA) now caveats all T ≥ 300 K results; title extended to name
the thermal spin valve; conclusions rewritten as four explicit claims; six references added
(Bauer 2012, Zeng 2011, Song 2020 and Ghanbari 2018 — both *Physica E* — Eklund 2016, Sabeer
2021); manuscript rebuilds clean at 26 pp. (Environment note: the WSL image had been rebuilt —
the Kwant venv and TeX Live were gone; venv rebuilt per the memory recipe, TinyTeX installed.)

---

## The story in five sentences

A journal-gap analysis showed that the standard nanoribbon-thermoelectric template had never
been applied to CrN, so we built a deliberately DFT-free Slater–Koster + Landauer model of
half-metallic h-CrN ribbons, validated against published bands, phonons, and the adjacent
DMRG paper's edge magnetism. The minimal orbital manifold that symmetry suggests produced
ZT ≈ 0.33 and passed every sensitivity check — and was wrong, because it missed the majority
conduction pocket; restoring it collapsed ZT eightfold, and that failure mode (invisible to
parameter sensitivity) became one of the paper's contributions. The honest landscape is
modest thermoelectrics (ZT ≈ 0.04–0.15 at 300 K) but outstanding spin physics: 100%
spin-polarized transport over a ~4 eV window, with the narrow armchair N=8 ribbon uniquely
combining its best ZT with full polarization. The same gap yields a thermal spin valve with an
exact collinear OFF state, which any continuous domain wall destroys (half transparency at
9 Å) — so constrained-wall or spacer junctions are the working geometries. An adversarial
referee panel then hardened the manuscript: numeric and honesty defects were fixed, methods
made reproducible, prior art positioned, and the flagship result shown robust against the
model's one known systematic.

## The three load-bearing results

1. **Armchair N=8: ZT = 0.145 inside the fully polarized window** (μ = −0.34 eV,
   `fig_armchair8.png`, Table 2). Caveat: κ_ph bracket alone spans 0.08–0.24, and the ±10%
   sweep [0.13, 0.28] — the *value* is factor-2 semi-quantitative; its *location and
   robustness* (π*-pinned: unchanged) are the solid part.
2. **Exact thermal-spin-valve OFF state + its fragility** (`fig_spinvalve.png`,
   `fig_wall.png`): T_AP ≡ 0 over the window for collinear AP junctions; any continuous wall
   leaks, λ_1/2 ≈ 9 Å. Caveat: coherent adiabatic limit — experiment (Coey, Mathur) suggests
   real leakage is smaller, so the OFF claim is conservative but the model has no disorder.
3. **The manifold caution** (`fig_manifold.png`): reduced basis ZT = 0.33 vs honest 0.040 with
   ±10% sensitivity unable to detect it. Caveat: demonstrated for one geometry (zigzag N=14);
   the abstract states the matched comparison only.

## What is still open (from the notebook)

- User-only: make the GitHub repo public + tag a release (data statement promises it); Zotero
  citekey regeneration (17 pinned keys, Cabrera year); Editorial Manager upload.
- Stated future work: second conduction band/anticrossing above +0.5 eV; site-dependent
  exchange fed back into transport; explicit phonon transport through disorder (the
  enhancement route); self-consistent screening at μ ≈ +1 eV; first-principles K of h-CrN →
  intrinsic wall width λ_int.
- Session changes are uncommitted in git as of 2026-08-03.

## Understanding risks (kind but honest)

- The **π*-pinned variant's side effect** (minority d_z² rises 0.19 eV with Δ_ex) is easy to
  forget when defending why minority-edge optima dropped — the drop is partly *that*, not only
  the majority π* repositioning; the manuscript says so in §3.1.
- The **two different brackets** (κ_ph ½×/2× vs parameter-sensitivity spread) were conflated
  once already in the draft; keep them separate when talking to referees.
- The **N convention** (N counts alternating Cr and N atomic rows; N=14 = 7 Cr + 7 N rows,
  DMRG paper's convention) was the source of one bug and one referee minor; it is now defined
  in the Fig. 1 caption.
