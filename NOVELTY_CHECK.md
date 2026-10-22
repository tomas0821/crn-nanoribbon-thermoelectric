# Novelty check log — CrN nanoribbon thermoelectric

**Status (2026-10-21): CLEAN-pending-full-text** — deep re-check, every source; no collision. Two low-risk CrN papers unread (paywalled, VPN down). See `## Re-check 2026-10-21` at the end.

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

---

## Final pre-submission re-check — 2026-07-27 · VERDICT: CLEAN (all four DBs)
Re-ran the toolkit with the recorded queries ("CrN nanoribbon thermoelectric",
"CrN nanoribbon Landauer"). Crossref, OpenAlex and Semantic Scholar (authenticated): clean —
every hit is the known non-colliding prior art (Quintela APL 2009; ammonia-annealed CrN films;
CrN alloy-film Linköping thesis 2025; nanoribbon-thermoelectric papers on *other* materials,
incl. two 2025 Physica E ones confirming the format is welcome; the DMRG PRB 107, 205418
(2023) paper we cite). The toolkit's arXiv leg timed out / rate-limited ("Rate exceeded" from
this IP even after 10 min of backoff), so arXiv was checked via the arxiv.org search UI
instead: **"CrN nanoribbon" → exactly 1 result** (arXiv:2408.06754, the DMRG paper);
**"CrN nanoribbon thermoelectric" → 0 results**. The "first thermoelectric / phase-coherent
Landauer study of CrN nanoribbons" claim stands on all four databases as of submission.

---

## Re-check 2026-10-21 · VERDICT: CLEAN-pending-full-text (deep, every source)

> First thermoelectric-transport study of hexagonal (honeycomb) CrN nanoribbons: tight-binding +
> Landauer (Kwant) Seebeck / power factor / ZT of half-metallic zigzag and armchair h-CrN ribbons,
> plus spin caloritronics (spin-resolved thermopower, thermally driven spin valve, domain-wall leakage).

**Keyword sweep** — `check_novelty.py --rows 10`, Crossref + OpenAlex + Semantic Scholar + arXiv
(arXiv lane worked this time; S2 returned HTTP 429 on the first query only):
`"CrN nanoribbon thermoelectric"`, `"CrN nanoribbon Landauer"`, `"CrN nanoribbon"`,
`"hexagonal CrN monolayer thermoelectric"`, `"CrN monolayer Seebeck"`,
`"CrN nanoribbon spin caloritronics"`. Every CrN-nanoribbon hit is the DMRG paper
(PRB 107, 205418; arXiv:2408.06754). CrN thermoelectrics = films/bulk only (Quintela 2009,
ammonia-annealed films 2024, Linköping alloy-film thesis 2025). Monolayer CrN hits are magnetism
only (Physica A 2023 ML spin model; Chin. Phys. B 2021; PRB 2025 flexomagnetism; Molecules 2024).
Nanoribbon spin caloritronics is populated for other materials only (graphene, silicene, MoS2,
antimonene — incl. Physica E 2020 — Janus MoSeTe 2025, silicene 2026).

**Semantic sweep — Exa** (`category: research paper`, 10 results each, total **$0.028**):
`"Thermoelectric transport in hexagonal CrN nanoribbons"`;
`"Spin-dependent Seebeck effect and figure of merit of half-metallic transition-metal nitride nanoribbons from tight-binding Landauer transport"`;
`"Thermoelectric properties of two-dimensional honeycomb chromium nitride monolayer"`;
`"Thermally driven spin valve in a half-metallic nanoribbon with a magnetic domain wall"`.
No collision. New format-adjacent 2026 work: h-NbN2H2 monolayer + nanoribbon spin
thermoelectrics (DFT+NEGF, JPCC 2026, 10.1021/acs.jpcc.6c01014); TB+NEGF electronic ZT of
Ti3C2O2/Sc3C2F2/Zr3C2O2 MXene nanoribbons (10.1016/j.chphma.2026.04.001). Neither is CrN.

**Independent second opinions.** FastTrack `run_duplication_test` (claim as scope, 15 NN + semantic
additions; all ~30 records screened): no CrN-ribbon or CrN-monolayer thermoelectric paper; surfaced
Muntini 2022 (below) and a TI-nanoribbon domain-wall thermoelectric PRB 2020 (10.1103/physrevb.102.245412).
FastTrack `check_gap_saturation("thermoelectric properties of CrN nanoribbons")`: 0 records 2016–2026.
Consensus `"thermoelectric properties of hexagonal chromium nitride CrN monolayer or nanoribbon"`:
3 hits, all CrN films. CORE `"CrN nanoribbon"`: only the DMRG paper (+ coatings noise).
scholar-search Google Scholar `"CrN nanoribbon" OR "CrN nanoribbons"`: empty (lane unreliable, as
on 2026-10-21 morning). WebSearch (extended) `CrN nanoribbon thermoelectric OR Seebeck OR "spin
caloritronics" 2026`: no CrN result. **Scopus: not checked** (APIKEY_INVALID off the UCR VPN).

**Lineage probe (one hop, OpenAlex):**
- *Citations of Kuklin 2017* (W2552671966, 81 cites, all screened): magnetism / 2D-magnet reviews /
  CrN heterobilayers / CrP nanoribbon half-metal (PCCP 2023) / CrN-GaN spin valve — no transport
  or thermoelectric study of CrN ribbons.
- *Citations of the DMRG paper* (W4378214596): **0** in OpenAlex and 0 in Semantic Scholar — nobody
  has built on the CrN-nanoribbon line yet.
- *Citations of Modarresi 2019 CrN/P/CrN spin valve* (W2955332336, ~46): 2D spin valves / MTJs, none
  thermoelectric on CrN.
- *Citations of Muntini 2022* (W4200631183, 22): Prayitno/Hasdeo group 2D-magnet thermoelectrics
  (NiBr2, MBr2, MnF3, FeI2) — none CrN, none ribbon.

**Full text read (Step 5):**
- Muntini et al., PRMaterials 6, 064010 (2022), 10.1103/physrevmaterials.6.064010 — DFT + Boltzmann
  (energy-dependent τ) thermoelectrics of monolayer CrX, **X = P, As, Sb, Bi only**; antiparallel
  spin-valve setup raises ZT. Full text: no CrN, no nitride, no ribbon, no Landauer. *Not a
  collision — but the closest conceptual prior art for "half-metal + antiparallel spin valve +
  thermoelectric"; not cited in the manuscript.*
- Rahangiar et al., PRB 110, 035150 (2024), 10.1103/physrevb.110.035150 — model half-metal
  band-structure optimization of ZT and the spin-valve enhancement factor (Cahaya, Tretiakov & Bauer,
  IEEE Trans. Magn. 51 (2015)); conclusion: the spin valve helps only poor-TE gapless half-metals; a
  gap is needed for large ZT. Full text: no CrN, no ribbon, no Landauer. *Supports our "modest ZT"
  conclusion; not cited.*
- Both PDFs in `pdfs/` (git-ignored) and in Zotero collection `crn-nanoribbon-thermoelectric`.

**Verdict: CLEAN-pending-full-text.** No paper computes thermoelectric, Landauer or spin-caloritronic
transport of CrN nanoribbons (or of the h-CrN monolayer). The "first thermoelectric / phase-coherent
Landauer study of CrN nanoribbons" claim stands. Capped below plain CLEAN only by the two unread
papers below, both low risk by abstract.

**ASSUMED (unread, no OA copy; added to Zotero by DOI):**
- Gong, Tang & Yi, PRB 111, 094441 (2025), 10.1103/physrevb.111.094441 — assumed magnetism only
  (strain-gradient DMI, skyrmions, domain walls in monolayer CrN; no transport). Relevant to our
  wall paragraph (it reports DMI and domain-wall textures in monolayer CrN).
- Xue et al., 10.1063/5.0165709 (2023) — assumed DFT band-structure/DOS spin-valve analysis of a
  vertical CrN/GaN/CrN vdW stack; no thermoelectrics, no ribbons.
Close them with the UCR VPN (`/fetch-paper`), then upgrade to CLEAN.

**Citation gaps found (author's call):** Muntini 2022 and Cahaya 2015 (half-metal antiparallel
spin-valve thermoelectrics) belong in Sec. 3.5 next to the thermal spin valve, with the distinction
stated (they use the AP valve to raise ZT in diffusive Boltzmann transport; ours is a ballistic
ON/OFF switch of charge and heat). Rahangiar 2024 fits the "modest thermoelectric" conclusion.
Gong 2025 is a candidate for the wall-width paragraph (DMI in monolayer CrN).

**Query traps (new):** `"CrN nanoribbon Landauer"` on Crossref returns Gustav Landauer (anarchist)
literature; the scholar-search Google Scholar and arXiv lanes return empty even for the known DMRG
paper (use the toolkit's arXiv leg or arxiv.org directly); FastTrack gap saturation returns 0 for any
CrN-ribbon phrasing (over-specified, not evidence).
