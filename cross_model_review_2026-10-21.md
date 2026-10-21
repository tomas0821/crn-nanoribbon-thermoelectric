---
type: cross-model-review
draft: manuscript/manuscript.tex (+ highlights.txt, cover_letter.tex), commit ad296ec
scope: text changed by the two-conduction-band (CB2) rewrite since c32321b; other sections as context
date: 2026-10-21
referees: [kimi (Kimi Code CLI; model id not printed), antigravity (agy; model id not printed), deepseek-v4-pro (via opencode), codex (gpt-5.6-terra)]
skipped: [qwen, glm]
second_pass_verifier: fable-5
verdict: major revisions (all fixes are text-level except one figure regeneration; no new production runs needed)
---

# Cross-model review — CrN nanoribbon thermoelectric (CB2 version)

## Summary assessment

Four model families reviewed the two-band rewrite against the data files. All four agree the
numbers mostly carry over correctly. Table 2, the π*-pinned check, the CB2 fit, the
convergence figures, the phonon-floor and p-type checks, and the sensitivity spreads all match
`data/`. All four found the same leftover from the old story in §2.2: it still says the optimum
is pinned to the minority edge. The finding that matters most came from the data. With a 10 %
smaller exchange splitting Δ_ex, the minority edge drops below the +0.71 eV optimum. That makes
"still fully polarized" false for armchair N=8, and the top of the quoted zigzag N=14 spread
(0.114) is an optimum only about 56 % polarized. The headline survives once it is qualified:
with the minority edge anywhere within the paper's own 0.1–0.2 eV digitization uncertainty,
every optimum stays ≥ 99.6 % polarized at 300 K. Two further problems:

- §3.2 credits the spurious ZT = 0.33 to the wrong edge. This wording predates the rewrite and
  was missed by every earlier round.
- Fig. `fig_wall`(a) draws its +0.5 eV reference line at the old value of 5 instead of 9.

Codex, DeepSeek and Antigravity recommend major revisions; Kimi recommends minor revisions.
The verdict is "major" because the central claim needs a stated exception. The work is small:
text edits plus regenerating one figure.

## Major points

1. **[All four + orchestrator] §2.2 still tells the old story.** — "Of the two reported edges
   we target the conduction edge ($+0.9$~eV~\cite{Kuklin2017}), to which the thermoelectric
   optimum is pinned … Because the optimal doping tracks the minority conduction edge
   one-for-one, the quoted optimal $\mu$ values inherit the same $\sim$$0.1$--$0.2$~eV
   uncertainty" (lines 202–208).
   - *Verified:* the current optima sit at +0.47 to +0.71 eV and −0.34 eV. The Δ_ex −10 %
     variant leaves the polarized optimum of zigzag N=14 at +0.47 eV (ZT 0.0633), so nothing
     tracks the edge.
   - *Fix:* say the minority edge is targeted because it bounds the polarized window. The
     uncertainty of the optimal μ comes from the CB2 parameters (ε_c2, t_c22), not from the
     minority-edge digitization.

2. **[Orchestrator computation; Kimi independently; consistent with Codex/Antigravity
   robustness findings] "Every optimum fully polarized" fails under Δ_ex −10 %, and the paper
   says the opposite.** — "stays inside the polarized window for every variation (for
   $\Delta_{\rm ex}{-}10\%$ and $\varepsilon_{c_1}{+}10\%$ the second-conduction-band optimum
   at $\simeq+0.7$~eV overtakes it, still fully polarized)" (line 522–524); also the §3.7
   robustness sentence (line 756) and the Fig. 7 spread.

   Recomputed from the cached variant files, 300 K, production κ_ph:

   | Variant | Peak ZT @ μ−E_F | Minority onset | P_G at optimum |
   |---|---|---|---|
   | zigzag N=14, Δ_ex −10 % | 0.114 @ +0.71 | +0.665 | 56 % |
   | armchair N=8, Δ_ex −10 % | 0.209 @ +0.71 | +0.720 | 68 % (peak driven by the smeared minority onset) |
   | armchair N=8, ε_c1 +10 % | 0.148 @ +0.745 | +1.08 | 100 % (this half of the sentence is right) |

   All other large excursions (t_c22, t_c1, ε_c1) stay at 100 % polarization.

   Why it happens: −10 % of Δ_ex is 0.36 eV and moves the minority edge to +0.64 eV, 0.26 eV
   below Kuklin's +0.9 eV. The fully polarized optimum itself is still there (0.0633 at +0.47
   eV for zigzag N=14); a partly polarized minority-onset peak just overtakes it.

   Margin (second-pass rigid-shift estimate):

   | Minority edge shifted down by | P_G at the +0.7 eV optima, 300 K | P_G at 700 K |
   |---|---|---|
   | 0.10 eV (to the DFT value) | 99.99 % | 98.3–98.5 % |
   | 0.20 eV | 99.6–99.75 % | 92–93 % |
   | 0.30 eV | 87–90 % | — |

   *Fix:*
   - Replace "still fully polarized" with the actual Δ_ex −10 % result.
   - Note that the 0.114 upper bound of the zigzag spread is a partly polarized optimum.
   - State the claim with its real margin: it holds for any minority-edge position within the
     stated 0.1–0.2 eV uncertainty at 300 K.
   - Optional: quote the polarized-window peak for each sensitivity row.

3. **[DeepSeek] §3.2 credits the spurious 0.33 to the wrong edge.** — "the ribbon transmission
   drops from several quanta to zero within $\sim$$0.2$~eV of $E_F$ and stays zero up to the
   minority edge. That sharp edge is precisely what band-engineering arguments … seek; it
   yields a large thermopower and a peak $ZT\simeq0.33$" (lines 405–410).
   - *Verified:* the reduced-manifold ZT has two peaks, 0.256 at +0.19 eV (the truncation
     edge) and the global 0.332 at +1.035 eV. The larger one is the minority onset, which no
     majority background shunts (G↑ = 0, P_G = −100 %).
   - This wording predates the rewrite and was missed by all three same-model rounds and the
     August cross-model panel.
   - *Fix:* the truncated basis empties the majority channel between +0.19 and +1.0 eV, which
     creates sharp edges on both sides: ZT ≈ 0.26 at +0.19 eV and 0.33 at +1.03 eV. The
     fivefold comparison (0.33 → 0.063) stands.

4. **[Codex; second pass] The domain-wall numbers hold only at E_F, and Fig. `fig_wall`(a)
   contradicts its own caption.**
   - The text says the wall "reaches the exact adiabatic limit at the upper end" (line 678–679;
     Conclusions (iii), line 833). `wall_sweep.txt` gives T_AP = 7.94 of 8 at λ = 31.4 Å
     (99.2 %). The 4-decimal limit is reached only at λ ≈ 9 nm.
   - At +0.5 eV, close to the new ZT optimum, the wall is 70–77 % transparent at the
     intrinsic width (T_P = 9). The text does not say that all its percentages are at E_F.
   - `scripts/fig_wall.py:64` hard-codes `TP = {0.0: 8.0, 0.5: 5.0}`, a value left over from
     the single-band model. The dotted +0.5 eV reference sits at 5 while the AP curve
     saturates at 9.
   - The conclusion that constrictions or spacers are required is unaffected: walls of 70–99 %
     transparency leak massively either way.
   - *Fix:*
     - Set `TP[0.5] = 9.0` and regenerate the figure.
     - Replace "exact adiabatic limit at the upper end" with ≈ 99 % at E_F (≈ 77 % at
       +0.5 eV).
     - Label the E_F-only numbers as such.

## Minor points

- **[Codex MAJOR; DeepSeek, Antigravity, Kimi MINOR; second pass: overstated] PF and ZT peaks
  conflated.** §3.3 calls +0.5 eV "the global maximum of the power factor and $ZT$". The PF
  there is 0.582 pW/K², 1.5 % below the global PF maximum (0.591) at +0.71 eV. The Fig. 5
  caption has this right.
- **[Kimi] Design rule (ii) contradicts Table 2.** It says "At matched width the armchair
  ribbon is better for $N=8$ and $N=20$ and slightly worse for $N=14$". Table 2 has armchair
  N=14 at 0.072 > zigzag N=14 at 0.063, so armchair is better at all three widths. The
  comparison is also at matched N, not matched width (18.6 vs 21.9 Å).
- **[Codex, DeepSeek, Kimi; orchestrator recomputed] K-pocket number is stale.** It reads
  "$-0.20$~eV in the model" (lines 214, 354). The production 6×6 model gives −0.252 eV at K
  (pure c1). The residual is still inside the tracing accuracy.
- **[DeepSeek, Antigravity, Kimi; orchestrator recomputed] 700 K value for armchair N=8.** The
  text says "0.088 at 700 K" (line 524); Table 2 says 0.089. The recomputed value is 0.0893,
  so Table 2 is right.
- **[Codex] Armchair N=8 sensitivity sentence.** "insensitive to $\Delta_{\rm ex}$ and to all
  nine conduction-orbital parameters" is true of the −0.34 eV feature but sits awkwardly next
  to the overtaking cases. Fix it together with Major 2.
- **[Kimi] Largest excursions misattributed.** §3.7 names V_pdπ among the largest zigzag
  excursions. For zigzag N=14 the data rank Δ_ex, t_c22, t_c1 and ε_c1 above V_pdπ (−19 %).
  V_pdπ is the largest only for armchair N=8.
- **[Kimi] ±10 % convention range.** The text says "0.2–0.35 eV for the on-site energies".
  ε_c2 is ±0.15 eV and Δ_ex is ±0.36 eV, so state ±0.12–0.36 eV.
- **[Kimi] Temperature trend.** "decreases with temperature … as do the second-conduction-band
  optima of the wider ribbons" is imprecise: zigzag N=14 rises to 0.067 at 500 K before
  falling.
- **[Antigravity] Screening caveat still refers to the old operating point.** It reads
  "transport at $\mu-E_F\simeq+1$~eV assumes a rigid band structure" (line 794). Restate it
  for the +0.5–0.7 eV operating range.
- **[Antigravity] Singular leftover.** "on the effective conduction orbital" (line 635) should
  read "orbitals c₁, c₂".
- **[Kimi] Fig. 2 caption** names only CB1 and VB1, but both CB1 and CB2 were traced and are
  plotted.
- **[DeepSeek] Minority-edge value quoted inconsistently.** The text uses +1.0, +1.05, +1.06
  and +1.1 eV. Distinguish the monolayer CBM (+1.0) from the ribbon transport edge
  (+1.03–1.06).
- **[DeepSeek] §2.1 "no consequence below".** This is true of c₂ above 2.8 eV, but the CB2
  onset inside the window is set by poorly constrained parameters. Cross-reference §3.7.
- **[Codex, Antigravity, Kimi] Highlights.**
  - "no ab-initio input" → "no new ab-initio calculations".
  - Kimi: "ZT = 0.06-0.15" carries no uncertainty.
  - After Major 2, "every optimum inside the fully spin-polarized window" needs the same
    qualifier as the abstract.
- **[DeepSeek, Antigravity, Kimi] Repo audit gap.** The 500/700 K values, the κ_ph brackets,
  the P_G percentages and the polarized-window sensitivity peaks appear in the paper but in no
  `data/*.txt`. The public repo promises reproducibility, so dump them to text files.
  (Orchestrator recomputed zigzag N=14 at 500/700 K and armchair N=8 at 500/700 K: all match
  except the 0.088/0.089 rounding.)

## Where the models disagreed

- **Did "every optimum polarized" survive the sensitivity sweep?** Kimi caught it with
  arithmetic (ε_π + Δ_ex = +0.64 < +0.71). Codex and Antigravity attacked the robustness
  wording on t_c22 grounds instead, which is a height problem, not a polarization one. DeepSeek
  only noted that zigzag positions are missing from `sensitivity.txt`. Codex also checked the
  ε_c1 half of the same sentence, which turned out to be correct, and missed the Δ_ex half.
- **PF/ZT conflation severity:** MAJOR for Codex, MINOR for the other three. The verified
  difference is 1.5 % in PF, so it is minor.
- **The wall overstatement was raised only by Codex (MAJOR) and Kimi (MINOR).** Neither noticed
  the stale reference line in the figure, which the second-pass verifier found.
- **Only DeepSeek** caught the §3.2 attribution. It also raised the CB2-onset label, which was
  refuted (see below).
- **Overall:** Kimi says minor revisions; Codex, DeepSeek and Antigravity say major.

## What was checked and found sound

- Table 2 (all six peaks, positions, widths, κ_ph).
- π*-pinned invariance; phonon 3-mode floor; p-type scan; Δ^c_↓ null result.
- CB2 fit parameters, rms (0.044 vs 0.171), anticrossing gap (0.13 eV), upper band 7.5 eV at
  Γ, minority replicas above +3.3 eV.
- Convergence numbers (0.0685/0.0632/0.0632/0.0636; 100 K drift 0.6 %).
- Sensitivity spreads [0.029, 0.114] and [0.135, 0.267] as numbers.
- Wall λ_1/2 = 9.24 Å, ℓ_mt = 0.53 Å, v_F ≈ 3×10⁵ m/s, T_AP ≈ 0.6 at λ ≈ 1 Å, ≥ 0.95 T_P at
  2.4 nm (at E_F).
- Substrate windows; manifold factor (0.3322 → 0.0632).
- Narrative consistency of the abstract, conclusions, cover letter and §3.3–3.5 (apart from the
  items above).
- Orbital character of the +0.47 eV feature: the c₂ subbands really do enter there (see
  dropped finding below).

## Pipeline notes

- **First pass:** Kimi, Antigravity and DeepSeek all hit the 25-min limit with no report.
  - Kimi spent the time recomputing from `.npz` files.
  - DeepSeek stopped after reading its inputs.
  - Antigravity printed "Error: interrupted".
  - Codex finished in the first pass.
- **Re-run:** the three were re-run with a time-boxed brief (text files only, no
  recomputation, 40-min limit) and all three reported. Raw outputs are in the session
  scratchpad, not in the project.
- DeepSeek ran as `deepseek/deepseek-v4-pro`; `deepseek-reasoner` is no longer offered by
  opencode.
- Qwen and GLM were skipped by choice: 0/12 of their majors survived verification on
  2026-08-25.
- File integrity: checksums of the manuscript, highlights, cover letter and `data/*.txt`, plus
  `git status`, were identical before and after the review.
- **Orchestrator calculations** (read-only, scripts in the session scratchpad):
  - Polarization of the sensitivity variants (`check_dex.py`).
  - Lead-mode orbital character (`mode_character.py`).
  - 500/700 K ZT.
  - Monolayer bands at K.
- **Second-pass verifier:** Fable 5 independently recomputed findings 1–5. It confirmed 1, 2
  (Δ_ex half), 3 and 4, and marked the PF and wall items as overstated. It found the stale
  `TP[0.5]` in the wall script.

## Dropped findings

**Downgraded in orchestrator verification (Step 3), then fixed:**
- **[DeepSeek MAJOR → MINOR]** "'at the onset of the second conduction band' is wrong for
  zigzag N=8/14 because the fitted CB2 minimum is 0.73 eV at M."
  - The physics is right. Orbital character of the zigzag N=14 lead modes:

    | E (eV) | c₂-dominated modes / all modes |
    |---|---|
    | +0.45 | 0 of 6 |
    | +0.50 | 4 of 9 |
    | +0.55 | 6 of 11 |

    All six ribbons behave the same way: the c₂ subbands enter between +0.45 and +0.50 eV.
  - In the monolayer the c₂-character band is the *lower* band over the outer half of Γ–M,
    with a local minimum of +0.469 eV at 3/4 Γ→M (99 % c₂). The energy-ordered upper band
    has its minimum at 0.69–0.73 eV at M.
  - But the label is ambiguous: §2.1 does define CB2 with "a minimum of ≃0.7 eV at M". An
    earlier draft of this report wrongly said the manuscript never quotes the 0.7 eV; that
    was an orchestrator error, corrected here.
  - The +0.70/0.71 eV optima sit on later c₂ subband edges, not on the onset.
  - *Fixed 2026-10-21:* §2.1 now defines the term by c₂ character, and the body, abstract and
    conclusions say "on subband edges of the second conduction band".
- **[Antigravity MAJOR, part]** "'not converged beyond a factor of ~2' is inaccurate, the spread
  spans a factor of ~4." Refuted: the text means relative to the baseline, and −53 %/+81 % is
  a factor of about 2 each way. The rest of that finding is merged into Major 2.
- **[Antigravity, part]** "The cover letter glosses over the armchair N=8 exception." Not a
  defect on its own: the cover letter says every optimum is inside the polarized window, which
  is true at baseline. It gets the same qualifier as Major 2.
- **[Antigravity]** Treating the 2026-09-02 log line [−3.22, +1.06] against verify.py's
  [−3.20, +1.00] as a run conflict. Not a conflict: one is the ribbon transport gap, the other
  the wide-ribbon/monolayer gap.

**Dropped on second-pass verification (Step 3b):**
- The ε_c1 +10 % half of Major 2: that optimum really is 100 % polarized.
- The internal-contradiction reading of "insensitive to Δ_ex" (Codex): true of the −0.34 eV
  feature itself. Kept only as a wording minor.

---

## Delta check of the fixes (Codex, post-fix) — 2026-10-21

**Scope:** only the text changed in `ad296ec..3e801bd` (the fixes above), numbers checked against
`data/*.txt`. **Referee:** Codex (`codex exec -s read-only`, gpt-5.6-terra); first attempt
hung on stdin to the 40-min timeout (backgrounded without `< /dev/null`), the re-run completed.
The other three referees were not re-run. **Result:** no wrong number; 0 new majors after
verification. All numbers that have a `data/*.txt` source match it (cb2_fit, table2,
sensitivity_armchair8, polarization_margin, wall_sweep).

**Codex MAJORs, verified and downgraded to MINOR (wording overclaims in the Conclusions):**
- (i) "this landscape is unchanged … by a 0.2 eV shift of the minority edge": optimum dopings
  are unchanged, but the peak ZT moves by up to 2.3 % (zigzag N=20 0.0830→0.0849) and P_G is
  99.6–99.8 % for zigzag N=20 and armchair N=14/20 (`polarization_margin.txt` 76, 78–79).
  *Fix:* "preserved (same optimum dopings, P_G ≥ 99.6 %)".
- (ii) "the coincidence of the thermoelectric optimum with full polarization" is unqualified,
  and the Conclusions never mention the Δ_ex −10 % exception (0.36 eV edge shift, optima
  56 %/68 % polarized), which lies beyond the stated 0.2 eV margin. *Fix:* one clause in (i)
  naming the exception.

**Reproducibility gap (Codex MINORs, consolidated):** several numbers added in the fixes exist
only in script stdout or in session scratch scripts, not in tracked `data/*.txt`, although the
data statement says the tagged release reproduces every number:
- only in scratch scripts: c2 subbands entering at +0.45–0.50 eV in all six ribbons; the
  Δ_ex −10 % minority edges (+0.67 eV zigzag N=14, +0.72 eV armchair N=8); majority mode
  count 3→9 at +0.43–0.49 eV;
- only in stdout of tracked scripts: reduced-manifold 0.26 at +0.19 eV and the +1.03 eV onset
  (`fig_manifold_comparison.py`); S ≈ −48 µV/K and the PF values (`fig45_thermoelectric.py`);
- the 300/500/700 K series in §3.4 (0.098/0.089, 0.063/0.067/0.062, 0.093→0.106) has no text
  source.
- Not a gap: the 0.12–0.36 eV range is 10 % of the Table 1 parameters.
*Fix:* move the two scratch computations into `scripts/` and write these values to a tracked
`data/*.txt`, then re-tag.

**Disposition (2026-10-21):** both Conclusions fixes applied; every flagged number now written by a
tracked script to `data/*.txt` (`cb2_subbands`, `fig5_zigzag14`, `manifold`, extended `table2`,
minority-onset column in `polarization_margin`). Tracking corrected two values: c2 entry
+0.48–0.50 eV (was +0.45–0.50) and mode count 3 at +0.44 eV (was +0.43). Tagged `v1.2-submission`.
