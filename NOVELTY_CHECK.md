# Novelty check log — CrN nanoribbon thermoelectric

**Date:** 2026-07-14 · **Tool:** `lit-gap-toolkit/check_novelty.py` (Crossref + OpenAlex + arXiv;
Semantic Scholar was HTTP-429 rate-limited, so verdict rests on the other three, which agreed).

## Queries run (minimal, most-specific first)
- `CrN nanoribbon thermoelectric`
- `CrN nanoribbon Seebeck transport Landauer`
- `CrN nanoribbon thermoelectric figure of merit`
- `CrN armchair nanoribbon Landauer`
- `CrN nanoribbon tight-binding`

## Verdict: CLEAN (method+material combination unpublished)
- The nanoribbon-Seebeck/Landauer template is **densely populated for other materials** —
  graphene, zigzag graphene (vacancy-enhanced ZT), silicene, phosphorene, borophene, SiC,
  biphenylene ribbons — confirming it is a welcome, standard format.
- **No CrN nanoribbon transport/thermoelectric paper exists** in any of the three databases.
- CrN thermoelectric prior art is **experimental thin-film only**: e.g. "Influence of Ammonia
  Annealing on CrN Thin Films and Their Thermoelectric Properties" and a 2025 Linköping
  licentiate thesis on CrN alloy thin films. Neither is low-dimensional transport theory.

## The one adjacent paper (cite, don't collide)
- **"DMRG Analysis of Magnetic Order in the Zigzag Edges of Hexagonal CrN Nanoribbons"**
  (arXiv:2408.06754, 2024-08-13; published Phys. Rev. B). Method: **DFT + DMRG**, MLWF Wannier
  interpolation.
  → Use it to (a) justify the hexagonal CrN nanoribbon geometry, (b) validate that edges are
  magnetic, (c) differentiate this work on *property* (thermoelectric response) and *method*
  (analytical mean-field TB + phase-coherent Landauer, not DFT+DMRG+Boltzmann).

### ⚠ CORRECTION (verified 2026-07-14 from the abstract) — do NOT claim "first transport"
The earlier note that this paper is "magnetism, not transport" is **too strong**. It **does**
compute transport: **spin-dependent semiclassical Boltzmann** transport (via MLWF), and reports
zigzag CrN edges act as a **perfect spin filter** under electron and hole doping. What it does
**NOT** do — and where our gap survives:
- **No thermoelectric quantities**: no Seebeck S, no power factor, no κ, no ZT.
- **No phase-coherent Landauer/Green's-function** transport (they use diffusive Boltzmann).
- **No tight-binding / Slater–Koster** model — only a **1D Heisenberg spin model**
  (J₁ ≈ 10–12 meV, J₂ ≈ −2 to 0 meV/Cr for zigzag) plus Wannier interpolation.
- Confirms a **half-metallic 2D monolayer** and half-metallic zigzag edge (spin-down gap
  reduced by localized edge states).

**Defensible novelty claim:** *first **thermoelectric** transport study (S, PF, ZT) of CrN
nanoribbons, in the **phase-coherent Landauer** regime, from a lightweight TB + mean-field
model.* Bonuses: their J₁/J₂ give a **cross-check target** for our mean-field magnetism; their
half-metallic monolayer anchors the **TB parametrization target**. Read the full paper (esp. any
supplement with the Wannier/TB Hamiltonian) before fixing ribbon widths and the pitch wording.

## Before drafting/submission
Re-run: `python3 /home/tomas/mnt/gdrive/Research/Current/lit-gap-toolkit/check_novelty.py \
  --query "CrN nanoribbon thermoelectric" --query "CrN nanoribbon Landauer"`
and re-check Semantic Scholar once it is not rate-limited.

---

## Deeper re-verification — 2026-07-15 · VERDICT: STILL CLEAN
Re-ran the toolkit (Crossref + OpenAlex + arXiv; Semantic Scholar again HTTP-429) with 5 expanded
queries, plus three targeted web searches. All sources agree: **no CrN nanoribbon thermoelectric
or transport paper exists.**
- **CrN thermoelectric prior art remains thin-film / bulk / alloy only** — e.g. epitaxial CrN
  (Quintela), a new **2026 RSC** p-type-via-oxygen CrN *film* study, CrN/Cr₂N films, Fe-nanoparticle
  CrN films, bulk CrN (ZT≈0.1), CrN alloy-film Linköping thesis. None low-dimensional/ribbon.
- **2D CrN hits** are nanosheets (Cr₂O₃/CrN FETs), nanoparticles, the Modarresi spin valve, or a
  *different* compound (CrSi₂N₄ monolayer). Not CrN nanoribbon thermoelectrics.
- The **spin-thermoelectric nanoribbon format is well populated for OTHER materials** (graphene,
  graphitic carbon nitride g-C₃N₄/g-C₄N₃, BN, Heusler) — confirms the format is welcome, not a
  collision.
- Incidental useful ref (not a collision): *"Tight-binding parametrization for the chromium
  nitride: A NMTO study"* (arXiv 2012) — TB parametrization of **bulk rocksalt** CrN; could be
  cited in Methods.

Bottom line: the "first thermoelectric / phase-coherent Landauer study of CrN nanoribbons" claim
holds. Still advisable to do one final re-check immediately before submission.

**Semantic Scholar now checked too (2026-07-15).** The toolkit was given an S2 API key
(auto-throttled to 1 req/sec; key in `~/.config/lit-gap-toolkit/s2_api_key`, read via
env `SEMANTIC_SCHOLAR_API_KEY`). S2 no longer 429s and **also confirms CLEAN**.

### FULL four-database re-run (2026-07-15, 5 queries, Physica E ISSN filter) — VERDICT: CLEAN
No errors/429 on any source. Every CrN hit is non-colliding:
- CrN thermoelectric = thin-film/bulk/alloy/nanoparticle only (Ammonia-annealed CrN films;
  CrN alloy-film Linköping thesis 2025; "stoichiometric and hole-doped CrN" APL **2009**,
  DOI 10.1063/1.3120280; CrN nanoparticles).
- The only CrN *nanoribbon* paper is the DMRG *magnetism* one (which we cite/differentiate).
- "CRN: Camera Radar Net" is an unrelated CS acronym.
→ **No CrN + nanoribbon + thermoelectric/Landauer paper exists.** Confirmed across all four
databases (Crossref, OpenAlex, arXiv, Semantic Scholar).

**Citation fixes surfaced (resolves the two `%VERIFY` bib entries):**
- DMRG paper is published in **Physical Review B** (per OpenAlex), not only arXiv — but the DB
  year records conflict (PRB 2023 vs arXiv 2408.06754 = Aug 2024); confirm the exact vol/page/year.
- The Quintela CrN thermoelectric APL is **2009, DOI 10.1063/1.3120280** (our bib had 2014).

---

## Deepest re-verification — 2026-07-16 · VERDICT: CLEAN (all four DBs, S2 authenticated)
Ran the toolkit with **8 queries** across **Crossref + OpenAlex + arXiv + Semantic Scholar**
(S2 now uses an API key — no 429; all four returned for every query). No CrN nanoribbon
thermoelectric/Landauer paper exists.
- CrN thermoelectric prior art = bulk/film/ceramic only (Quintela APL 2009; oxygen-free CrN
  ceramics 2014; secondary-phase-suppressed CrN 2021; Fe-nanoparticle CrN films 2023; CrN alloy
  films Linköping 2025; ammonia-annealed CrN films).
- Low-dimensional CrN = **magnetism/spintronics only**: the DMRG nanoribbon paper and a NEW find,
  **Xiang et al., "Prediction of one-dimensional CrN nanostructure as a promising ferromagnetic
  half-metal," Chin. Phys. B 32 (2023), DOI 10.1088/1674-1056/acb200** — DFT prediction of a 1D
  CrN half-metal (Δs=1.58 eV, MAE, BN nanocable). NOT thermoelectric, different geometry (1D wire),
  heavy DFT → adjacent, not colliding. Now cited (`Xiang2023`) to strengthen the low-D CrN context.
- "CRN: Camera Radar Net" is an unrelated CS acronym.

Bottom line: the thermoelectric gap is if anything MORE glaring — low-D CrN is actively studied for
magnetism, yet no thermoelectric/Landauer study exists. The "first thermoelectric/Landauer study of
CrN nanoribbons" claim is solid, confirmed across all four databases. Do one last re-run just
before submission.

---

## Final pre-submission re-check — 2026-07-18 · VERDICT: CLEAN
Re-ran the toolkit ("CrN nanoribbon thermoelectric", "CrN nanoribbon Landauer"): Crossref,
OpenAlex and Semantic Scholar all clean (arXiv timed out on the broad query; the three
responding databases agree and all previous four-database checks were clean). The only CrN
nanoribbon paper remains the DMRG magnetism/Boltzmann one (PRB 107, 205418 (2023)), which we
cite and differentiate. The "first thermoelectric / phase-coherent Landauer study of CrN
nanoribbons" claim stands. NOTE (post-audit): the manuscript's headline is now the HONEST
result (extended model, ZT 0.04–0.15, spin-filter emphasis + manifold caution) — novelty claim
unchanged by the correction.
