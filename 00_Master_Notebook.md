# 📓 Lab Notebook — CrN Nanoribbon Thermoelectric

**Started:** 2026-07-14
**Author:** Tomas Rojas

---

## 📥 AI Handoff & Next Actions

- [x] **Repo made public + tagged (2026-08-25):** GitHub repo `tomas0821/crn-nanoribbon-thermoelectric`
      switched to public and tagged `v1.0-submission` (pushed). **M1 blocker from round 3 is
      now resolved** — the Data and code availability statement is accurate. Also removed two
      genuinely-unused legacy scripts (`fig2_monolayer_bands.py`, `fig3_transmission.py`) and
      dead code (`crnte.thermo.kappa_ph_ballistic`) as a public-repo footgun cleanup — verified
      via `scripts/verify.py` (Wiedemann-Franz + monolayer/ribbon consistency, both pass) that
      `crnte/monolayer.py` and `crnte/ribbon.py` are NOT dead (they're live imports of
      `monolayer_sk.py`/`ribbon_sk.py`) so those were restored after an initial wrong deletion.
      README refreshed to 2026-08-25 status (spin valve, λ_int, referee history added).
- [x] **Cross-model referee panel (2026-08-25):** first non-same-model review — Kimi,
      Antigravity, DeepSeek-reasoner (via opencode), Codex, all read-only against
      manuscript.tex → `cross_model_review_2026-08-25.md`. Kimi timed out mid-verification
      (10 min) without emitting a formatted report; its one fully-reasoned finding (phonon
      mode-count) is credited via independent convergence with DeepSeek. Verdict: minor
      revisions. 3 genuinely new catches missed by all 3 same-model rounds: (1) quoted
      T_AP≈0.7 at λ≈1 Å didn't match `data/wall_sweep.txt` (actually ≈0.62); (2) Fig. 3's
      caption claimed "100% spin polarized throughout the accessible doping window" while its
      own plotted range extends past the point (+1.0 eV) where §3.6 says polarization is
      already lost; (3) the μ-scan window defining every "global optimum" claim
      (`MU=linspace(-0.6,1.2,...)` in `fig6_width_edge_vacancy.py`) was never disclosed in the
      text. Also surfaced a real open physics question (phonon.py's 4-gapless-mode floor is a
      3D-beam result; a strictly 2D sheet should have 3 acoustic branches — not fixed, flagged
      as an explicit caveat pending a possible follow-up recomputation) and a genuine
      SOC-vs-"exact"-OFF-state internal-consistency point. Several other MAJORs raised by
      Antigravity/Codex turned out to already be explicit numbered caveats in the manuscript's
      own Scope section (T_C≈209K, rigid-band/no-screening) — downgraded, not fresh gaps; one
      (c-orbital "unphysical scattering artifacts" at edges/walls) was refuted on a mirror-
      symmetry argument. **All surviving findings fixed same day** in manuscript.tex: wall
      value corrected (0.7→0.6, both occurrences), Fig. 3 caption bounded to the actual
      polarized window, μ-scan domain disclosed + CB2-unresolved-region caveat added near
      Table 2, abstract ZT-floor clause added for the π*-pinned degradation, SOC caveat added
      to §3.7, phonon 4-mode-floor caveat added to §2.5 (code/data NOT changed — this is a
      disclosed open question, not a confirmed bug, and changing the floor would require
      regenerating every cached κ_ph/ZT number), LKAG J2-sign wording fixed (§3.8 +
      Conclusions), Fig. 6(d) caption reworded to match the §2.3 100K convergence caveat,
      κ_ph-bracket ordering standardized to ascending. Recompiled clean: 28 pp, 0 undefined
      refs, overfulls ≤5.8 pt (unchanged, pre-existing). Also deleted two stale build logs
      (`manuscript/build.log`, `build_last.log`) flagged as clutter by the pre-review audit.

- [x] **Cross-model panel extended to 6 model families (2026-08-25, same day):** skill updated
      to add Qwen Code and GLM (glm-4.6, via opencode). Ran both against the already-revised
      manuscript from the entry above → merged into `cross_model_review_2026-08-25.md`. Qwen's
      first attempt failed (free-tier quota exhausted, confirmed via `qwen -c` retry: `403`);
      user reported the quota reset and it was re-run successfully. GLM: 8 MAJOR + 3 MINOR.
      Qwen: 4 MAJOR + 4 MINOR, with an outlier overall "reject" recommendation (every other
      referee across both rounds converged on "minor revisions"). **0 of 12 combined MAJOR
      findings survived verification** — checked twice per finding (my own read + an
      independently-briefed Fable 5 subagent explicitly tasked to refute, per the skill's new
      optional Step 3b, opted into by the user for this run). Dominant pattern: both models
      quoted the manuscript's own already-added caveats/disclosures from the entry above back
      as if they were unaddressed (e.g. one finding quoted the exact μ-scan disclosure sentence
      while claiming the window was "never disclosed"). One finding (Qwen, phonon 4-mode floor
      "underestimates κ_ph and inflates ZT") contained a clear physics-direction error, caught
      independently by both verification passes: an extra spurious mode *over*-estimates κ_ph,
      which makes reported ZT *lower*/conservative, not inflated. **No manuscript changes made**
      — this round is a clean validation of the prior round's fixes, not a source of new ones.

- [x] **Referee panel round 3 (2026-08-14):** re-review of the round-2-fixed draft, focused
      on the new §3.7 λ_int (intrinsic domain-wall width) addition never previously refereed.
      1 new MAJOR confirmed: both comparison factors in "$\lambda_{\rm int}$...lands a factor
      of $\sim$3 above the full-transparency scale...and a factor of $\sim$30 above
      $\lambda_{1/2}$" were wrong by roughly one rung on the scale ladder — λ_int (24–30 Å) is
      actually *comparable to* (0.8–1.0×) the ~3 nm full-transparency scale and only ~3× (not
      ~30×) above λ_1/2 = 9 Å. **Fixed same day** in §3.7 and Conclusions (iii): reworded to
      "comparable to (0.8–1.0×) the full-transparency scale...factor of ~3 above λ_1/2" and
      "transmits at least T_AP≈0.95 T_P at the lower end...reaching the exact adiabatic limit
      at the upper end" — the physical conclusion (constriction/spacer required) is unchanged
      and still supported. Recompiled clean: 0 undefined refs, no overfull hboxes >10pt.
      **M1 (repo public + tagged release) still unresolved** — URL and tags API both 404 as of
      2026-08-14; this remains the only blocker before submission. R2/R3 verification passes
      hit the session token limit mid-run; re-run if a full round-3 report is wanted before
      submitting.

- [x] Full pre-submission audit (2026-07-17): every calculation, claim, reference and the
      cluster checked. Found one MAJOR flaw (missing majority conduction band) + κ_ph concern +
      a list of smaller issues. All fixed the same day (see the two run entries below).
- [x] **Model extension:** effective conduction orbital `c` fitted to the digitized Kuklin CB1
      (electron pocket at K). All transport rerun on a unified 5 meV grid. *(2026-07-17)*
- [x] **Phonon Landauer κ_ph** anchored to the digitized Modarresi (PRApplied 2019) Fig. 4(a)
      monolayer phonon dispersion → `crnte/phonon.py`; width- and T-dependent. *(2026-07-17)*
- [x] **Manuscript rewritten** around the honest results + methodological caution; CRediT,
      funding, data statements added; HPC acknowledgement removed (nothing ran on HPC);
      highlights + cover letter updated. *(2026-07-17)*
- [x] **Pipeline adoption (2026-07-27):** both source papers converted to
      `papers_md/` — [[kuklinTwodimensionalHexagonalCrN2017]] and
      [[modarresiLateralSpinValve2019]] (Modarresi Table I hand-restored; see
      `papers_md/CONVERSION_NOTES.md`). Final novelty re-check re-run: **CLEAN**
      (Crossref + OpenAlex + Semantic Scholar; arXiv checked separately after rate-limit).
- [x] **Full bibliography → Zotero (2026-07-27):** all 27 manuscript references imported into
      the CrN-nanoribbon-TE collection (doi.org BibTeX → connector; Datta book from refs.bib).
      Collection now mirrors `manuscript/refs.bib` 1:1 — see `papers_md/INDEX.md`.
- [x] **papers_md batch 2 (2026-07-27):** the duplicate-merges surfaced 10 PDF attachments;
      all converted — incl. [[kupczynskiDMRGAnalysisMagnetic2023]] (J₁ = 10–12 meV,
      J₂ = −2…0 meV, anisotropy 0.73 meV all verified verbatim — the J cross-check targets),
      [[liebingTunnelingMagnetothermopowerMagnetic2011]] (Table I intact), and five old APS
      OCR scans (readable prose, don't trust symbols — see `papers_md/CONVERSION_NOTES.md`).
      12 of 26 papers now converted; the other 14 have no PDF (manual retrieval).
- [x] **Referee panel round 1 (2026-07-29 → implemented 2026-08-01):** 4-referee adversarial
      review + verification → `referee_report_2026-07-29.md` (verdict: major revisions; 20
      numbered majors + 27 minors, 2 raised findings refuted). **All fixes implemented
      2026-08-01** — manuscript.tex substantially revised (see run entry below): κ_ph-bracket
      numeric error fixed (0.030–0.047, not "0.02–0.08"), abstract/table contradiction fixed,
      wall OFF-state criterion restated honestly (collapse, not threshold), new
      `fig_armchair8` figure + armchair-N8 ±10% sweep ([0.13, 0.28] one-sided,
      `data/sensitivity_armchair8.txt`), π*-pinned systematic variant
      (`scripts/pistar_pinned.py`, `data/pistar_pinned.txt`), full methods completeness
      (fit targets, digitization, U_eff = 1.346 eV SCF spec, ZA branch, LKAG contour, real
      convergence numbers, wall-region convergence ≤3×10⁻⁵), spin-caloritronics prior art
      cited (Bauer 2012, Zeng 2011, Song 2020 *Physica E*, Ghanbari 2018 *Physica E*), T_C ≈
      209 K caveat (Modarresi RPA), Fig 4 dropped + Fig 5 trimmed, conclusions rewritten as
      four explicit claims, title extended, abstract ≤~200 words, 6 new refs in refs.bib.
      NOTE: venv + TeX Live had vanished (WSL image rebuilt) — venv rebuilt per memory recipe,
      TinyTeX installed (`~/.TinyTeX`, PATH: `$HOME/.TinyTeX/bin/x86_64-linux`).
- [x] **Re-immersion walkthrough (2026-08-03):** full-story walkthrough delivered; narrative
      persisted in `PROJECT_STORY.md` (phase-by-phase + synthesis — read that first when
      returning to the project). NotebookLM notebook synced (sources: PROJECT_STORY,
      notebook, manuscript PDF; ID in `.notebooklm`) with video overviews in `overviews/`.
- [x] **Referee panel round 2 (2026-08-04):** re-review of the revised draft against the
      round-1 report → `referee_report_2026-08-04.md`. **Verdict: minor revisions** (up from
      major). Scorecard: 18/21 round-1 majors resolved, 2 partially (c-orbital weight values;
      figure count), 1 unresolved = the user-side repo/tag blocker. 2 NEW majors, both
      confirmed and both introduced by the revision: (a) §3.1 "qualitative landscape intact"
      contradicts data/pistar_pinned.txt (pinned global optima relocate into the window for
      4/6 geometries — also undermines §3.5 rule (i)); (b) Table 2 bracket columns overflow
      the text block by 102 pt. Plus 12 deduplicated minors (wording precision vs data files,
      2 stale cross-refs, float order, abstract still 213 words). Not yet implemented.
- [x] **Round-2 fixes implemented — done 2026-08-04:** both majors fixed (§3.1 pinned-variant
      results moved to §3.5 and restated honestly — "global optimum relocates into the window
      for 4/6 geometries", rule (i) hedged; Table 2 overfull 102 pt → 0 via \footnotesize +
      tabcolsep 2pt + shorter headers) and all 12 minors (exact factors 2.3×/56%, \ref{sec:te}
      cross-ref, "0.19 eV error in energy as well as k", ZA min(quad,sine) stated, wall check
      per-λ with absolute+fractional numbers, Fig 6(d) now starts at 100 K + caption note,
      Zeng/Song/Ghanbari characterized separately, Modarresi "proposed, from first
      principles", abstract 198 words with split opener, "strongly asymmetric" spread,
      fig_spinseebeck float moved to §3.4 + armchair8/designrules envs swapped for citation
      order). Rebuilt clean: 26 pp, 0 undefined refs, remaining overfulls ≤5.8 pt (cosmetic,
      incl. the pre-existing Eq. (1) matrix). Still pending: repo public + tag (user), then
      cite the tag name in the data statement.
- [x] **λ_int closed with zero DFT (2026-08-04):** the planned MAE run's target number was in
      our own cited literature all along — Modarresi 2019 reports K = Δ = 0.73 meV/Cr (U=3;
      0.47 at U=0, easy axis out-of-plane), the same value the DMRG paper reuses as its
      single-ion anisotropy. λ_int = πa√(J₁/2K) ≈ 2.4–3 nm (J₁ = 7.8–12 meV) ≫ λ_1/2 = 9 Å →
      intrinsic walls fully transparent; constriction/spacer designs are REQUIRED by
      published numbers. Manuscript §3.7 "unreported" sentence (wrong, missed by both
      panels) fixed; conclusions claim (iii) strengthened. If any DFT is ever run for this
      line of work, the best target is now the monolayer PBE+U band structure (kills the
      digitization/π* systematic — post-submission insurance or follow-up seed), not the MAE.
- [ ] **User GUI step (remaining):** regenerate the still-pinned `Author_Year` citekeys
      (17 items incl. Kuklin, Modarresi, Liechtenstein — the rest got clean keys via your
      merges), add the missing year `1974` to the Cabrera item, then verify the three
      predicted-key folders (`kuklinTwodimensionalHexagonalCrN2017`,
      `modarresiLateralSpinValve2019`, `liechtensteinLocalSpinDensity1987`) match and rename
      if they differ.
- [x] **Repo public + tagged (2026-08-25):** done — see entry at the top. The only remaining
      pre-submission step is uploading to Editorial Manager with highlights.txt + cover letter.
- [ ] **Before submission:** upload to Editorial Manager with highlights.txt + cover letter.

### Still open (future work, stated in the paper)
- [ ] Second conduction band + CB1/CB2 anticrossing above +0.5 eV (single effective band now).
- [ ] Site-dependent exchange fed back into transport (edge moments differ by only 6–8%).
- [ ] Explicit phonon-transport calculation (edge disorder / anharmonicity) — the
      phonon-engineering route to higher ZT.
- [ ] Self-consistent screening for the heavily gated (μ ≈ +1 eV) operating point.

---

## Project Overview

Theory/modelling paper for **Physica E**: thermoelectric transport + spin filtering of
**hexagonal (honeycomb) CrN nanoribbons** via **tight-binding + Landauer–Büttiker** (Kwant).
Deliberately **no fresh DFT** — everything parametrized from published first-principles data:
electronic bands from Kuklin et al., *Nanoscale* 9, 621 (2017)
([[kuklinTwodimensionalHexagonalCrN2017]]; digitized, incl. the majority conduction pocket),
phonons from Modarresi et al., *PRApplied* 11, 064015 (2019)
([[modarresiLateralSpinValve2019]]; digitized).

**Novelty (re-verified 2026-07-16, 4 databases):** first **thermoelectric** (S, PF, ZT),
**phase-coherent Landauer** study of CrN nanoribbons. The adjacent DMRG paper (PRB 107, 205418
(2023)) does DFT+DMRG+Boltzmann spin filtering — no thermoelectric quantities. Claim is "first
*thermoelectric*/Landauer", NOT "first transport".

**Environment:** isolated Kwant venv at `~/venvs/crn-te` (Python 3.12, numpy<2). System Python
3.14 cannot build Kwant. Run code with `~/venvs/crn-te/bin/python`. See `requirements.txt`.

**Honest headline (2026-07-17, extended model):**
- Pristine CrN nanoribbons are **modest thermoelectrics**: peak ZT = 0.04–0.15 at 300 K
  (phonon-Landauer κ_ph), global optimum pinned to the **minority band edge** (μ−E_F ≈ +1.05 eV).
- They are **outstanding spin filters**: minority channel gapped over [−3.2, +1.0] eV → 100%
  spin-polarized transport for any gating below +1 eV.
- **Armchair N=8** is special: best ZT (0.145 at −0.34 eV) *inside* the polarized window.
- **Methodological caution (a paper contribution):** the minimal d+p_z manifold misses the
  majority conduction pocket and fabricates ZT ≈ 0.33 — an ~8× artifact that parameter
  sensitivity cannot detect.

---

## Simulation Logs

### Run: wall_leakage_spinful — 2026-07-18 ⭐ KEY QUANTIFICATION (supersedes the "robust to
wall details" wording of the first valve entry)

`crnte/valve.py`: FULL SPINFUL noncollinear calculation (Cr 4 orb × 2 spins, N p_z × 2; Walker
wall θ(x)=2 arctan e^{(x−x0)/δ}, width λ=πδ; exchange (Δ/2)(1−n̂·σ) on Cr orbitals).
**Corrected a lead-placement bug** (Kwant attaches a lead on the side its symmetry vector
points toward — the θ=0 lead sat on the wrong side, faking an OFF state at ALL wall widths;
caught by the 1D-chain textbook test + uniform-rotation invariance check T=8.000000).
Honest result (`data/wall_sweep.npz/.txt`, `fig_wall.png`): OFF state survives only for
atomically sharp reversals — **λ_1/2 ≈ 9 Å at E_F; λ ≳ 3 nm walls are fully transparent**
(T→T_P exactly, adiabatic limit; both limits validated). Mistracking scale ħv_F/Δ_ex ≈ 0.4 Å
(ħv_F = 1.35 eV·Å from the lead bands). Literature anchors (all Crossref-verified, added to
refs.bib): Cabrera–Falicov 1974, Tatara–Fukuyama PRL 1997, van Hoof et al. PRB 1999 (wide
walls transparent), Bruno PRL 1999 (constrained walls atomically sharp), Coey PRL 1998 (CrO₂
grain-boundary MR), Mathur JAP 1999 (manganite DW resistance ≫ mistracking), Walter Nat.
Mater. 2011 + Liebing PRL 2011 (magneto-Seebeck readout exists). Substrate OFF window:
literature-direct from Kuklin composites (1.43/1.71 eV, 100% spin-polarized;
`data/substrate_window.txt`; our rigid-shift model CANNOT reproduce the narrowing — band
realignment — so the composite values are quoted, not modeled). **Planned (not run) DFT to fix
the one unbacked number:** single-unit-cell noncollinear DFT+U+SOC magnetocrystalline
anisotropy K of h-CrN (VASP/QE, few orientations, ~few hundred core-hours on HPC@UCR);
with exchange stiffness A from DMRG J1 → intrinsic wall width λ_int = π√(A/K), deciding
whether unconstrained walls exceed λ_1/2 (almost certainly yes → constriction/spacer designs
required, as the paper already prescribes).

### Run: thermal_spin_valve — 2026-07-18 ⭐ NEW RESULT

`build_spin_valve` (ribbon_sk): two-terminal ribbon with ANTIPARALLEL lead magnetizations
(collinear abrupt wall). Exact result: each spin species is majority in one lead and inside the
minority gap in the other → **T_AP(E) = 0 identically over the whole half-metallic window**
(numerics: machine zero on the full 5-meV grid, `data/zigzag_N14_valve.npz`). G_P(E_F) = 7.3
e²/h vs G_AP = 0 → thermally driven spin valve. Claim restricted to the OFF window (above
+1.0 eV the c-orbital decoupling makes the AP onset unquantitative). Figure `fig_spinvalve.png`
+ manuscript §"A thermally driven spin valve". Inter-edge P/AP mean-field ΔE was computed
(`data/spinvalve.txt`) but is NOT quoted in the paper — rigid-shift MF without charge
self-consistency is unreliable for that ΔE; the valve premise is external control (exchange
bias), standard for spin valves. Graphical abstract added (`graphical_abstract.png`, 1660×550).

### Run: honest_landscape_extended_model — 2026-07-17 ⭐ PRODUCTION

All transport regenerated on the extended model (5-orbital: d_z², d_xz, d_yz, c | p_z), unified
fine grid E ∈ [−1.2, +1.5] eV, dE = 5 meV, both edges, N = 8/14/20, plus the reduced-manifold
comparison (`zigzag_N14_TE_noc.npz`). κ_ph from `crnte.phonon` (see below).

| Config | W (Å) | κ_ph(300K) | peak ZT(300K) @ μ−E_F | polarized-window ZT @ μ | ZT(700K) |
|---|---|---|---|---|---|
| zigzag N=8 | 10.2 | 0.62 nW/K | 0.062 @ +1.08 | 0.040 @ +0.12 | 0.071 |
| zigzag N=14 | 18.6 | 1.03 nW/K | 0.040 @ +1.08 | 0.014 @ −0.12 | 0.065 |
| zigzag N=20 | 27.1 | 1.46 nW/K | 0.048 @ +1.09 | 0.017 @ +0.08 | 0.066 |
| armchair N=8 | 12.2 | 0.71 nW/K | **0.145 @ −0.34** | 0.145 @ −0.34 | 0.088 |
| armchair N=14 | 21.9 | 1.19 nW/K | 0.138 @ +1.05 | 0.047 @ −0.13 | 0.127 |
| armchair N=20 | 31.7 | 1.69 nW/K | 0.104 @ +1.07 | 0.029 @ −0.14 | 0.118 |

Key facts: T↑(E_F) = 8 (zigzag N=14), T↓ = 0 over the whole minority gap; at the minority-edge
optimum S↓ ≈ −150 μV/K vs S↑ ≈ +4 μV/K (P_G drops to ~50% at +1.05); in the metallic window
|S| ≲ 40 μV/K (multichannel background). **Manifold comparison (fig_manifold):** reduced
d+p_z gives peak ZT = 0.332; extended gives 0.040 — the sharp-edge artifact quantified.

Numerics hardening: `transmission()` now rejects unphysical smatrix results (one 9×10¹² spike
at a band edge caught); `thermo.coefficients` floors L0 ≤ 1e−9 as insulating. Convergence
(`data/convergence.npz`): dE 0.005→0.0025 changes peak ZT by 0.66%; length spread exactly 0.
Sensitivity: all 10 parameters ±10% (see `data/sensitivity.txt`, fig7).

### Run: phonon_landauer_kappa — 2026-07-17

`crnte/phonon.py`: ballistic phonon-Landauer mode count anchored to the digitized monolayer
phonon dispersion of Modarresi et al. Fig. 4(a) (green curves; calib 33.07 px/THz, 298 px/Å⁻¹).
Anchors: v_LA ≈ 8.5, v_TA ≈ 4.3 km/s; acoustic maxima ZA/TA/LA = 4.7/5.4/10.4 THz; optical
13.7→7.2, 13.2→10.8, 16.85→15.1 THz. Recovers 4κ₀T at low T (verified to 1%), grows ~linearly
with width, saturates above ~500 K. κ_ph(300 K) = 0.6–1.7 nW/K for W = 10–32 Å. Replaces the
old flat 4κ₀T estimate (which was coincidentally right at N≈14/300 K but wrong in width- and
T-dependence).

### Run: model_extension_conduction_pocket — 2026-07-17 ⚠ MAJOR CORRECTION

Pre-submission audit found the reduced d+p_z manifold **misses Kuklin's majority conduction
band** (electron pocket at K, CBM −0.2 eV; states fill +0.4…+1.2 eV) — the "sharp majority edge
at +0.2 eV" and everything built on it (ZT ≈ 0.23, doping design rule, ±100% polarization
switch) was a basis-truncation artifact. Fix: digitized CB1 from Kuklin Fig. 2d (300 dpi;
E_F-line + axis-label calibration; 18 path points, ±0.1 eV in the transport window) →
`crnte/kuklin_targets.py: CB1_DIGITIZED`; added effective Cr-sublattice orbital c with
1st–3rd-shell hoppings, weighted-LSQ fit: ε_c=0.915, t_c1=0.285, t_c2=−0.028, t_c3=0.030 eV
(pocket at K −0.197 vs −0.21 target; M saddle 0.58 vs 0.63; Γ 2.64 vs 2.41). Minority sector
unchanged (gap [−3.2, +1.0] = 4.2 eV vs reported 3.9). Pocket holds 0.067 e/cell. Zigzag lead
period doubled to 2a (hopping range). VB1 k-space misfit noted honestly (π* top at K +0.19 vs
DFT peak ~0 inside the Γ–M / K–Γ intervals). SCF magnetism module stays in the d+p_z manifold
(pocket adds ~0.07 e/Cr, negligible for moments); edge-magnetism results unchanged.

### Run: N-convention correction — 2026-07-15 ⚠ (superseded numbers)

`width` was not the atomic-row count (29-row "N=14" zigzag vs 15-row armchair). Fixed so
width = N rows exactly; reran everything. This corrected the spurious "zigzag 2× armchair"
edge rule. (Numbers from this run are themselves superseded by the 2026-07-17 model extension.)

### Runs: 2026-07-14/15 (superseded)

Initial cartoon model → reduced SK model, first transport + thermoelectrics, sensitivity,
convergence, edge magnetism (fig_edgemag; SCF in d+p_z manifold — still current), LKAG J1/J2
(still current; see `data/edge_exchange.txt`), manuscript v1. The headline ZT ≈ 0.23 and the
"+0.2 eV band-edge design rule" from these runs were artifacts of the reduced manifold — kept
here for the record; see `fig_manifold.png` for the quantified comparison.

---

## Manuscript & repository

- **Manuscript:** `manuscript/manuscript.tex` — elsarticle, *Physica E*; 18 pp, 10 figures,
  2 tables. Title: "Thermoelectric transport and spin filtering in hexagonal CrN nanoribbons:
  a tight-binding Landauer study". Abstract 238 words (limit 250). CRediT + funding + data
  statements included. Compiles clean (no undefined refs).
- **Companion derivations:** `derivations/derivations.tex` (9 pp) — every formula incl. the c
  orbital and the phonon-Landauer κ_ph.
- **Repo:** <https://github.com/tomas0821/crn-nanoribbon-thermoelectric> — **must be made
  public before submission** (the manuscript promises open code+data).
- **Rebuild everything:** `~/venvs/crn-te/bin/python scripts/run_all_transmissions.py`, then the
  fig scripts (fig1…fig7, fig_manifold, fig_spinseebeck, fig_edgemag, convergence, sensitivity,
  edge_exchange_run). All production data cached under `data/` (also convergence, edgemag,
  wide-window T(E), edge exchange — everything quoted in the paper is cached).

## Caveats kept honest (stated in the paper)

1. TB fitted to digitized published bands (±0.1–0.3 eV) → semi-quantitative; ±10% sensitivity
   checked, and the paper explicitly warns sensitivity cannot catch missing bands.
2. Single effective conduction band: CB2 + anticrossing above ~+0.5 eV unresolved; VB1 top
   misplaced in k (not in E).
3. κ_ph is a coherent ballistic estimate (½×–2× bracket); disorder/anharmonicity would lower
   κ_ph and raise ZT.
4. Transport uses uniform bulk exchange; edge-moment feedback (6–8%) omitted.
5. μ ≈ +1 eV operating point assumes rigid bands under heavy gating.
