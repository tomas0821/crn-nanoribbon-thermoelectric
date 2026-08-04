---
type: referee-report
round: 2
draft: manuscript/manuscript.tex (revised 2026-08-01)
previous: referee_report_2026-07-29.md
date: 2026-08-04
verdict: minor revisions
---

# Referee report — CrN nanoribbon thermoelectric (round 2)

Same panel design as round 1 (R1 methods, R2 novelty, R3 results/figures, R4 journal fit),
but each referee's first job was to adjudicate its own round-1 points against the revised
draft, quoting the revised text as evidence; disputed adjudications and all new MAJOR
findings went through the independent refutation pass (this round, verifiers also recompiled
the manuscript and recomputed numbers from `data/`). 49 round-1 points adjudicated; 2 new
majors raised, both **confirmed**; 0 refuted; 17 new minors (deduplicated below).

## Summary assessment

The revision did what it claimed. Every honesty-of-numbers defect from round 1 is fixed and
verified against the data files (the κ_ph bracket, the abstract/Table-2 contradiction, the
wall criterion, the flagship's uncertainty and figure); the methods section is now
reproducible to the panel's satisfaction, with the arithmetic of the newly stated
specifications independently checked (U_eff = 3.6/2.674 = 1.346 eV ✓; minority edges
ε_pz = −3.2, ε_π + Δ_ex = +1.0 ✓; convergence numbers match `convergence.npz` ✓); and the
positioning gaps are closed. Two new majors exist, and both are artifacts *of the revision
itself*: the §3.1 sentence "leaves the qualitative landscape intact" is contradicted by the
revision's own π*-pinned data (the global optimum *relocates off the minority edge* for four
of the five geometries that had it there — which also undermines design rule (i) of §3.5),
and the new Table 2 bracket columns overflow the text block by 102 pt (~3.6 cm into the
margin — reproduced by independent compilation). Both are afternoon fixes, as are the 12
deduplicated minors (mostly wording precision against the new data files and two stale
cross-references). The one standing blocker is unchanged and outside the manuscript: the
repository is still private and untagged, and the revision has *increased* how much the
paper promises to find there. Verdict: **minor revisions** — fix the two new majors and the
minors, make the repo public with the promised tag, and this is submittable.

## Round-1 scorecard

| Round-1 point | Status | Note |
|---|---|---|
| M1 repo/data statement false | **UNRESOLVED (user-side)** | URL still 404, `git tag -l` empty; revision added *more* repo promises (digitized points, fit script, convergence data, LKAG script) |
| M2 κ_ph bracket error | resolved | text now 0.047–0.030, matches Fig. 5(b); brackets separated from sensitivity spread |
| M3 abstract vs Table 2 | resolved | abstract now states the armchair-N=8 exception |
| M4 wall "~1 nm" criterion | resolved | restated as collapse; T≈0.7 at 1 Å, λ½ = 9 Å; caption fixed |
| M5 bare flagship 0.145 | resolved | κ_ph bracket [0.082–0.235] + ±10% sweep quoted |
| M6 no armchair figure | resolved | new `fig_armchair8` (T, S, ZT, window shaded, optimum starred) |
| M7 few-k_BT dismissal | resolved | replaced by the π*-pinned variant with per-geometry numbers |
| M8 spin-caloritronics prior art | resolved | Bauer/Zeng/Song/Ghanbari cited in intro + §3.7 |
| M9 unattributed spin-filter headline | resolved | abstract now "confirm, and quantify in the phase-coherent limit" |
| M10 ZA branch | resolved | α ≈ 44 THz Å², anchors for all six branches (matches `phonon.py`) |
| M11 d+p_z fit procedure | resolved | explicit target list, hand-fit stated |
| M12 c-orbital fit spec | **partially** | digitization/residuals/uncertainty now stated; weight *values* still qualitative; deposit contingent on M1 |
| M13 Δ_ex calibration | resolved | explicit edge relations; targeted quantity; μ-uncertainty propagated |
| M14 Hubbard spec | resolved | U_eff, convention, filling, tolerance/mixing all stated; arithmetic verified |
| M15 convergence claims | resolved | real grid numbers (verified vs `convergence.npz`); pristine check reframed; wall-region margin quantified |
| M16 ±10% honesty | resolved | "uniform convention, not a propagated error bar" + caption note |
| M17 Curie temperature | resolved | T_C ≈ 209 K (RPA) caveat in Scope |
| M18 edge disorder | resolved | via the report's scope-statement option (ratio argument in §3.4) |
| M19 "small, standard computation" | resolved | deleted; reframed as future work with the constriction/spacer lead |
| M20 structure/"twofold" | **partially** | four-claim conclusions ✓, named duplications gone ✓; still 12 figures (armchair figure replaced two cuts — defensible, but edge-magnetism + log-wall panel remain candidates for supplementary) |
| Minors (27) | 24 resolved | partially: abstract length (213 words, 44-word opener remains), Fig. 1 row annotation (caption defines N, rows still unnumbered), tagged release (promised but no tag exists — folds into M1) |

Both "partially" adjudications on majors were independently verified and upheld.

## New major points (both verified CONFIRMED)

1. **[R1 §3.1] "Qualitative landscape intact" is contradicted by the revision's own data** —
   "Recomputing every entry of Table 2 in this variant leaves the qualitative landscape
   intact but moves individual numbers substantially" — per `data/pistar_pinned.txt`, in the
   pinned variant the *global* optimum relocates off the minority edge and into the polarized
   window for four of the five geometries that had it at the edge (zz8 → +0.48 eV,
   zz14 → 0.00 eV, zz20 → +0.05 eV, ac20 → −0.17 eV; only ac14 stays at +1.04 eV). That is a
   qualitative change, and it undermines design rule (i) of §3.5 ("for most geometries the
   global optimum sits at the minority band edge") within the systematic's error bar.
   *Fix:* replace "leaves the qualitative landscape intact" with an honest statement — e.g.
   "preserves the order of magnitude and the armchair-N=8 exception, but demotes the
   minority-edge optima: in the pinned variant the global optimum moves into the polarized
   window for four of six geometries" — and add one hedging clause to §3.5 rule (i)
   ("in the baseline model; the π*-pinned variant weakens this rule, Sec. 3.1").

2. **[R4 §Table 2] The new bracket columns overflow the text block** — compiling yields
   `Overfull \hbox (102.29pt too wide)` at the Table 2 tabular: the paper's central results
   table sticks ~3.6 cm into the margin in the PDF. Introduced by the round-1 bracket fix.
   *Fix:* shrink (e.g. `\footnotesize` + shortened headers "peak ZT [½–2× κ_ph] (μ)"), or
   rotate to `table*`/sideways, or move the bracket values to a second row per entry.

## New minor points (deduplicated; raiser(s) in brackets)

- **[R1+R3+R4] "roughly double" overstates the pinned N=20 in-window change** — 0.0172→0.0269
  is ×1.56; only N=14 (×2.34) roughly doubles. Quote both factors or say "increase by 56–134%".
- **[R3+R4] Stale hardcoded cross-reference** — Scope says the disorder argument is "given in
  Sec. 3.5"; it lives at the end of §3.4. Use `\ref` to the actual subsection.
- **[R3+R4] "pinned at the correct edge energies" contradicts its own parenthesis** — a π* top
  at +0.19 eV where DFT has ~0 *is* an energy error; residual of round-1 M7(c). Reword ("its
  band edges lie within the stated digitization uncertainty, but the top sits at +0.19 eV…").
- **[R4] §3.1 pinned-variant sentence reads self-contradictory for zigzag N=20** — it both
  "disappears" and "roughly doubles" in one sentence; say explicitly that the peak *relocates*.
- **[R4] Structural misplacement** — the π*-pinned recomputation (a Table-2-wide ribbon
  result) sits inside the *monolayer* subsection §3.1, forward-referencing Table 2. Move the
  numbers to §3.5 (or a short §3.5 paragraph referencing the variant defined in §3.1).
- **[R4] "one-sided spread" overstates** — `sensitivity_armchair8.txt` gives [0.135, 0.276]
  about 0.145: the minimum is 7% below baseline. Say "strongly asymmetric" instead.
- **[R4] ZA sentence internally inconsistent** — "each branch is a monotone sine-form
  interpolation" is literally false for ZA (ν = αq², min(quad, sine) crossover). Say "each
  in-plane/optical branch…; ZA follows the quadratic form until it meets the sine curve."
- **[R1] Wall-region convergence check underspecified** — the ≤3×10⁻⁵ statement names no wall
  width (worst case is the widest wall) and no absolute/relative qualifier. State λ and units.
- **[R1] Fig. 6(d) plots ZT(T) from 50 K** on the production grid the methods declare
  unconverged below ~100 K. Start the plotted range at 100 K or state the caveat.
- **[R2] "large thermal magnetoresistance" mischaracterizes Song2020** — that paper reports
  thermally driven spin currents in BN-codoped ZGNRs, not a P/AP magnetoresistance figure of
  merit. Split the sentence: MR-type switching (Zeng) vs thermal spin currents (Song, Ghanbari).
- **[R2] "has since been used to construct lateral spin valves" reads as experiment** —
  Modarresi 2019 is a first-principles proposal. "…has been proposed as the basis of…"
- **[R3] §3.5 rule (i) attaches 0.15 to the minority-edge optima** — those span 0.040–0.138;
  the 0.15 endpoint is the in-window armchair-N=8 value introduced only in (iii). Quote 0.14.
- **[R4] Abstract still 213 words with a 44-word opener** — one more trim pass to land <200.
- **[R4] Out-of-order figure citation** — `fig:spin` is now cited first in §3.4 but floats in
  §3.6, so Fig. 8 is cited before Figs. 5–7 appear. Reorder floats or renumber.

## What was checked and found sound

- Every numeric fix from round 1 was re-verified at the source: Table 2 brackets vs
  `table2.txt` + recomputation, the κ_ph bracket vs Fig. 5(b), the armchair sweep spread vs
  `sensitivity_armchair8.txt`, the π*-pinned entries vs `pistar_pinned.txt`, grid convergence
  vs `convergence.npz`, U_eff and minority-edge arithmetic by hand.
- The six new references are real and correctly formed (spot-checked against Crossref).
- The new `fig_armchair8` supports every claim its caption makes (optimum position, S value,
  bracket, window shading); the revised `fig_spinseebeck` P_G curve matches the quoted 49%.
- The report's alternative-option fixes (disorder scope statement for M18; convention
  statement for M16) were accepted by the round-2 referees as satisfying a real referee.

---

### Verification log

2 new majors verified (both CONFIRMED — one by independent recompilation, one against
`pistar_pinned.txt`); 2 disputed "partially" adjudications verified (both upheld); nothing
refuted this round. The manuscript was not modified by the panel.

*Panel run 2026-08-04 (workflow wf_566a80ba-439, 8 agents). Round-1 baseline:
referee_report_2026-07-29.md (major revisions) → round 2: minor revisions.*
