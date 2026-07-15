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
