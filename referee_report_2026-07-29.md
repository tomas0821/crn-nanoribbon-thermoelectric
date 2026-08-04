---
type: referee-report
draft: manuscript/manuscript.tex
date: 2026-07-29
verdict: major revisions
---

# Referee report — CrN nanoribbon thermoelectric (round 1)

Panel: four independent adversarial referees (R1 methods/reproducibility, R2 novelty/positioning,
R3 results/figures/numbers, R4 journal fit/clarity), each reading the full LaTeX source; every
MAJOR finding independently verified by a refutation agent with access to the draft, the figures,
refs.bib, the cached data and the literature. 23 MAJOR raised → 21 kept, 2 refuted and dropped
(footer). 27 MINOR (quote-backed, unverified by design).

## Summary assessment

The paper's strongest asset survived direct attack: the priority claim ("first thermoelectric /
phase-coherent Landauer study of CrN nanoribbons") was independently re-checked with a fresh
duplication test and web searches and holds; the thermoelectric formalism, the collinear
AP-transmission zero, the manifold-truncation caution, and the abstract-to-figure delivery are all
sound. The weaknesses cluster in three places: (i) **honesty-of-numbers** — the text quotes a
κ_ph bracket (0.02–0.08) that contradicts its own Fig. 5(b) and is physically impossible, the
abstract makes an unqualified claim its own Table 2 contradicts, the flagship ZT = 0.15 is never
given an uncertainty, and the "~1 nm" OFF-state criterion misstates what Fig. `fig_wall` shows;
(ii) **reproducibility** — the promised repository is currently a 404 and the methods section
underspecifies the d+p_z fit, the ZA phonon branch, the Hubbard-U calibration and the domain-wall
convergence, none of which a reader could rebuild from the text; (iii) **positioning** — the
thermal-spin-valve section ignores the established nanoribbon spin-caloritronics literature, and
the abstract sells prior-art spin filtering without attribution. All of this is fixable without
new physics (only points 5, 7 and 18 may want small new computations), hence **major revisions**,
not rejection: the core result and its differentiation from the DMRG paper are solid.

## Major points

1. **[R1 §Data availability] The availability statement is false as submitted** — the cited
   repository returns HTTP 404 (private/nonexistent), and the manuscript repeatedly defers
   reproducibility details (digitized point sets, fit scripts, phonon anchors) to it —
   "…are openly available in the accompanying repository: `github.com/tomas0821/crn-nanoribbon-thermoelectric`" —
   *Fix:* make the repo public (with a tagged release) before submission, or ship the digitized
   data + fit specification as supplementary material. *(Known pending item — but it is the
   panel's hardest blocker.)*

2. **[R3 §Results 3.4] The quoted κ_ph bracket contradicts the paper's own Fig. 5(b) and is
   physically impossible** — "peak $ZT=0.040$ … (bracket $0.02$–$0.08$ for $2\times$ and
   $\tfrac12\times\kappa_{\rm ph}$)" — Fig. 5(b) shows ≈0.030/0.047; with κ_e dominating κ_tot,
   halving/doubling κ_ph cannot swing ZT by 2×. The 0.02–0.08 numbers appear to be a copy of the
   *parameter-sensitivity* spread [0.014, 0.079] — a different uncertainty. *Fix:* replace with
   the actual Fig. 5(b) values (~0.030–0.047) and audit every bracket in the paper so the κ_ph
   bracket and the sensitivity bracket are never conflated.

3. **[R3 §Abstract] Headline claim contradicted by Table 2** — "The largest thermoelectric
   response arises at the minority conduction-band edge ($\mu-E_F\simeq+1.0$ eV)…" — the single
   largest ZT in the study (0.145, armchair N=8) sits at −0.34 eV, inside the half-metallic
   window; the body hedges with "For most geometries", the abstract doesn't. *Fix:* qualify the
   abstract sentence to match the table.

4. **[R3 §Abstract/Fig. wall] The "~1 nm" OFF-state criterion misstates the paper's own figure** —
   "a noncollinear calculation shows this OFF state requires a magnetization reversal sharper
   than $\sim$$1$ nm" — Fig. `fig_wall`(b) shows T_AP jumping from machine zero to ≈0.7–0.8 at
   the very first finite wall (~1 Å; ON/OFF only ~10), and λ₁/₂ = 9 Å marks *half-transparency*,
   not OFF survival; the strict OFF state exists only at the singular collinear point λ = 0.
   *Fix:* restate honestly (quote T_AP(λ) / the ON/OFF ratio; any continuous texture leaks, so
   the device strictly requires the constrained-wall or spacer geometry).

5. **[R3 §Abstract/Table 2/Conclusions] The flagship ZT = 0.15 is quoted bare, with no
   uncertainty** — "the narrow armchair $N{=}8$ ribbon performs best ($ZT\simeq0.15$ at
   $300$ K)" — the ±10% sweep and the κ_ph bracket exist only for zigzag N=14; by the paper's own
   "not converged beyond a factor of ~2", 0.15 could be ~0.07–0.3. *Fix:* run the sensitivity
   sweep + κ_ph bracket for the armchair N=8 optimum (the geometry the paper promotes) and attach
   the bracket wherever 0.15 appears.

6. **[R3 §Results 3.5] The most important geometry is supported by a single table row** — "(iii)
   The narrow armchair $N=8$ ribbon is the exception and the most interesting geometry…" — no
   T(E), S(μ) or ZT(μ) for armchair N=8 appears in any figure (verified against every panel), so
   the −0.34 eV in-window optimum and S = −114 μV/K are uninspectable. *Fix:* add a panel (or
   extend Fig. 6) showing T(E), S(μ), ZT(μ) for armchair N=8 with the polarized window marked.

7. **[R3+R4 §Results 3.1] The "few-$k_BT$" dismissal of the fit residuals does not hold at the
   paper's own operating points** — "Both lie outside the few-$k_BT$ window that controls the
   transport integrals at the operating points discussed below." — (a) the polarized-window
   optima at +0.12/+0.08 eV sit within a few k_BT (26 meV) of the spurious π* states the model
   puts in [0, +0.19] eV where the DFT reference has none; (b) the armchair N=8 flagship at
   −0.34 eV and all in-window Table 2 entries are computed from the misfit valence band (digitized
   VB1 lies 0.8–1.6 eV below the model π* over much of M–K, and ribbon mode counts depend on the
   full dispersion, not just edge energies); (c) "misplaced in $k$-space (though not in energy)"
   in §Scope contradicts the +0.19 eV vs ~0 eV numbers of §3.1. *Fix:* quantify the effect
   (e.g. refit/pin the π* top as an extra sensitivity case and recompute in-window values), or
   downgrade all in-window ZT/S numbers to order-of-magnitude estimates and say so consistently.

8. **[R2 §3.7/Intro] The thermal spin valve ignores the established nanoribbon
   spin-caloritronics literature** — "The half-metallic window enables a two-terminal function
   that is stronger than spin filtering." — thermally driven currents switched by P/AP lead
   configurations in ferromagnetic zigzag nanoribbons are established (Zeng et al., Nano Lett.
   11, 1369 (2011), verified real; Bauer–Saitoh–van Wees, Nat. Mater. 11, 391 (2012); silicene
   thermal CMR, Sci. Rep. 2015; at least one Physica E paper on thermally driven spin current in
   zigzag GNRs); refs.bib contains none of it. *Fix:* cite the foundational works and state
   precisely what is new here — the exact, gap-enforced OFF over a ~4 eV window in a single
   pristine material, plus the noncollinear leakage quantification.

9. **[R2 §Abstract] The spin-filter headline is prior art sold without attribution** — "The
   ribbons are outstanding spin filters: … $100\%$ spin-polarized throughout the accessible
   window." — Kuklin (2017) predicted the 100%-polarized half-metal and the DMRG paper explicitly
   reported perfect spin filtering of zigzag CrN edges; 100% polarization below the minority edge
   is also partly inherited from the parametrization (Δ_ex fixed by the reported gap). The body
   concedes "confirming…" (§3.2); the abstract doesn't. *Fix:* present it in the abstract as a
   confirmation/quantification in the phase-coherent limit, reserving novelty language for what
   is new (quantized window, width/edge robustness, spin-resolved TE trade-off).

10. **[R1 §2.5 Phonons] The flexural ZA branch is never mentioned** — "acoustic velocities
    $v_{\rm LA}\simeq8.5$, $v_{\rm TA}\simeq4.3$ km/s…" — a 2D monolayer has three acoustic
    branches; ZA (quadratic near Γ, often the dominant 2D heat carrier at 300 K) is unreported,
    making κ_ph = 0.6–1.7 nW/K unreproducible from the text. (Verification note: `crnte/phonon.py`
    *does* treat ZA quadratically — α ≈ 44 THz Å², sine crossover — the treatment is simply
    unreported.) *Fix:* state the ZA representation and the anchor list for all six branches; note
    whether the ½–2× bracket covers the ZA-model ambiguity.

11. **[R1 §Table 1] No fitting procedure for the d+p_z parameters** — "The $d$+$p_z$ parameters
    are fitted to the band-structure targets of Ref. [Kuklin2017]" — targets are enumerated only
    qualitatively; no cost function, weights, or automated/manual statement; ε's and V_pdπ cannot
    be re-derived, yet the sensitivity scan shows they control peak ZT at the factor-of-2 level.
    *Fix:* list the explicit targets (energies at k-points, gap edges, pocket depth), the
    objective, and how the fit was done (manuscript or supplement).

12. **[R1 §2.1] The effective conduction orbital — the paper's central addition — is specified
    only as "weighted least squares"** — "fitted by weighted least squares to the digitized
    majority conduction band (fit residuals $\lesssim0.1$ eV…)" — no weighting scheme, point
    count/location, k-path, digitization tool, or provenance of the 0.1–0.3 eV uncertainty (these
    live only in code comments in a not-yet-public repo). Fig. 2 does show fit-vs-data, but
    ε_c, t_c1..3 are not reproducible from the paper alone. *Fix:* specify the digitization and
    weights, deposit the (k,E) points, show residuals.

13. **[R1 §2.2] The Δ_ex calibration is not reproducible as stated** — "We fix
    $\Delta_{\rm ex}$ by the reported minority gap rather than solving the self-consistency…" —
    if fixed by the 3.9 eV reported gap the model would give 3.9, yet it delivers 4.2 eV, and the
    map Δ_ex = 3.6 eV → edges [−3.2, +1.0] eV is never derived; the ZT optimum is pinned to that
    edge (+1.05–1.09 model vs +0.9 reported) and the edge-position uncertainty is never
    propagated into the optimal-doping values. *Fix:* give the explicit relation, state which
    quantity was targeted, and propagate the edge uncertainty.

14. **[R1 §3.8 Edge magnetism] The mean-field Hubbard calculation is irreproducible** — "with the
    effective on-site interaction calibrated so that the uniform solution recovers the fitted
    exchange" — U is never given (in eV), nor the decoupling/double-counting convention, the
    electron filling that fixes 2.67 μ_B, or any convergence tolerance/mixing. *Fix:* state all
    four; without them neither Fig. `fig_edgemag` nor the J constants can be checked.

15. **[R1 §2.3] The convergence statement is partly vacuous and omits the one case where it
    matters** — "We verified numerical convergence explicitly: the pristine transmission … is
    independent of the scattering-region length…" — for pristine ribbons that independence is a
    triviality; the grid claim shows no data; and the noncollinear Walker-wall junction (λ up to
    3 nm, exponential tails) has *no* convergence statement (region length vs λ, tail truncation).
    *Fix:* a real convergence table (peak ZT vs grid) + the wall-region length/truncation and
    evidence T_AP(λ) is converged.

16. **[R1 §Scope/Fig. 7] The ±10% sensitivity scan is inconsistent with the paper's own stated
    errors** — "Varying every model parameter by $\pm10\%$ … between $0.014$ and $0.079$" —
    ±10% on ε_c is ±0.09 eV and on t_c2 ±3 meV, both smaller than the acknowledged 0.1–0.3 eV
    digitization uncertainty; correlated (covariance) variations are never explored. *Fix:* tie
    the ranges to actual uncertainties (or sample the fit covariance) and state that ±10% is a
    convention, not an error bar.

17. **[R1 §3.4/Fig. 6d] ZT is quoted to 700 K with no mention of the Curie temperature** —
    "rising to $0.065$ at $700$ K" — rigid, T-independent exchange and perfect FM order are
    assumed; near/above T_C the half-metallic gap and the entire valve phenomenology collapse.
    *Fix:* cite the predicted T_C of h-CrN and either restrict the plotted range or caveat
    Δ_ex(T) softening explicitly (§Scope omits it entirely).

18. **[R4 §3.4/Scope] The obvious rescue calculation — edge disorder — is neither done nor
    excused** — "the same phonon-engineering route is open here (it requires an explicit
    phonon-transport calculation…)" — the *electronic* side of the disorder calculation is
    exactly what the existing Kwant setup provides (and the project plan listed a
    disorder/vacancy figure); the Scope section justifies only the missing phonon part. *Fix:*
    add one edge-vacancy/roughness transmission figure, or state explicitly why even the
    electronic disorder case is out of scope.

19. **[R4 §3.7] "A small, standard computation" hands the referee a major-revision demand** — "A
    single-unit-cell noncollinear DFT+$U$+SOC calculation of $K$---a small, standard
    computation---" — the paper certifies its own missing ingredient as trivial while declining
    to perform it, undercutting the deliberate no-ab-initio framing. *Fix:* delete the phrase and
    frame λ_int as future first-principles work; lead with the fact that constriction/spacer
    geometries make λ_int moot by design (the text already contains this).

20. **[R4 §Conclusions/structure] "Twofold" undersells a paper that actually stacks four
    headlines across 12 figures** — "The honest headline is twofold." — TE map + spin filter +
    thermal spin valve with wall analysis + edge magnetism with J's, plus the manifold caution;
    verified panel duplications exist (Fig. 4 vs `fig_spinseebeck`(a); Fig. 5 vs Fig. 6 ZT
    panels). *Fix:* tighten toward ~8 figures (merge S(μ) into the spin-resolved figure, merge
    the duplicated ZT panels, move edge magnetism and/or the log-scale wall panel to
    supplementary), and rewrite the Conclusions around an explicit short list of claims.

## Minor points

- **[R2]** First mention of the DMRG paper discloses only its magnetism; its Boltzmann
  transport/perfect-spin-filter result is deferred two paragraphs — disclose at first mention.
- **[R2]** "Experimentally, CrN thin films are established thermoelectric materials" rests on a
  single 2009 citation; add 2–3 recent film studies (Fe-nanoparticle 2023, CrN/Cr₂N 2018, etc.).
- **[R2]** Priority claims ("the first…", "has not been addressed") lack the standard "to our
  knowledge" hedge — add once each in abstract, intro, conclusions.
- **[R2+R3+R4]** Abstract sentence "collapses … from $ZT\simeq0.3$ to an honest
  $ZT\simeq0.01$--$0.15$" splices a single-geometry collapse (0.33→0.040, zigzag N=14) onto a
  cross-geometry range whose 0.15 endpoint was never computed in the reduced manifold — and 0.01
  appears nowhere in the results (Table 2 minimum is 0.014). Quote the like-for-like collapse and
  the honest range (0.014–0.15) separately. *(Three referees flagged this independently.)*
- **[R2]** The manifold caution names no published study it applies to — cite an example of the
  minimal-basis workflow or soften to a forward-looking caution.
- **[R3]** Abstract quotes the model's 4.2 eV gap ("more than 4 eV") and +1.0 eV edge as if they
  were the material's 3.9 eV / +0.9 eV — say "nearly 4 eV" or give both.
- **[R3]** "degrading the conductance polarization … to $\simeq50\%$" — P_G is plotted nowhere;
  `fig_spinseebeck`(b) shows the *thermocurrent* polarization (≈−100% there), and its 100% line
  has unexplained gaps — add P_G(μ) or cite Fig. 3 mode counts; explain undefined-0/0 gaps.
- **[R3]** "$T_{\rm AP}(E)=0$ for $E-E_F\in[-3.2,+1.0]$ eV [Fig. valve(a)]" — the figure shows
  only [−1.2, +1.0] eV; extend the plot or caption the numerically verified full window.
- **[R3]** `fig_edgemag`: the two zigzag edges are inequivalent (~4.5% vs ~6%); the text quotes
  only the larger and never mentions the Cr- vs N-termination asymmetry.
- **[R3]** Fig. 1 claims to define the width convention N but never numbers the rows — annotate
  rows 1..N for a small N.
- **[R3]** A fit residual (≲0.1 eV) smaller than the data's own uncertainty (0.1–0.3 eV) is not
  meaningful precision; quote one honest conduction-band uncertainty (~0.2–0.3 eV) consistently.
- **[R1]** Magnetic-force-theorem extraction (J₁ = +59, J₂ = +0.8 meV) has no implementation
  detail (contour, broadening, k-sum) — one methods paragraph or supplement pointer.
- **[R1]** Fig. 4 shows a 100 K curve although the methods say ≲100 K needs finer grids — state
  the grid used or drop the curve.
- **[R1]** The mistracking estimate "$\hbar v_F/\Delta_{\rm ex}\simeq0.4$ Å" never states v_F
  (multichannel ribbon: which subband?) — give the formula with numbers.
- **[R1]** In the wall Hamiltonian "$\tfrac{\Delta}{2}\,\hat n(x)\cdot\boldsymbol\sigma$ on the
  Cr orbitals", Δ is undefined and it's ambiguous whether the c orbital rotates with n(x) —
  define Δ and the orbital set (affects the +0.5 eV curve of Fig. wall).
- **[R1]** "monotone interpolation" for phonon branches: name the interpolant and the
  Γ–M/Γ–K directional-averaging rule — two readers would build different M(ω).
- **[R4]** Abstract is 238 words with a 40+-word opening sentence — cut to <200, one sentence per
  headline.
- **[R4]** Title omits the thermal spin valve that two figures, the longest subsection and the
  conclusions treat as a headline — extend the title or demote the valve.
- **[R4]** Δ_σ appears in Eq. (1) before definition; Δ_σ/Δ_ex/Δ are three notations for one
  quantity — define Δ_↑ = 0, Δ_↓ = Δ_ex under Eq. (1) and use Δ_ex in the wall field.
- **[R4]** Seven keywords vs Elsevier's cap of six — drop "spin filter".
- **[R4]** "DFPT" is never expanded — expand at first use.
- **[R4]** The domain-wall paragraph runs nearly a page as one paragraph (one sentence >70
  words), burying λ₁/₂ ≈ 9 Å — split into three paragraphs.
- **[R4]** Table 2 has no benchmark row (graphene comparison is prose-only) and silently drops
  the ½/1/2× κ_ph bracket the text promises "throughout" — add a bracket column or reference row.
- **[R4]** Fig. 5 (S(μ)) is largely redundant with `fig_spinseebeck`(a); Fig. 6(b)'s ZT(μ)
  reappears in other panels — fold and delete (same cleanup as major point 20).
- **[R4]** Data statement: add a tagged release/commit hash so the referee sees the exact version
  behind the numbers (complements major point 1).

## What was checked and found sound

- **The priority claim survived independent attack** (R2): a fresh FastTrack duplication test on
  three query formulations returned zero near-neighbours, and new web searches surfaced only the
  known non-colliding art — consistent with the four-database log in NOVELTY_CHECK.md through
  2026-07-27. The differentiation from the DMRG paper ("Boltzmann transport but no thermoelectric
  coefficients") is accurate, and the CrNdmrg2023 entry (PRB 107, 205418 (2023), published
  2023-05-25) and the corrected Quintela 2009 entry were verified against Crossref.
- The linear-response formalism (L_n moments, two-channel parallel addition, bipolar term and
  where it vanishes) is correct and standard (R1).
- The exact collinear AP-transmission zero is a rigorous lead-spectrum consequence; the
  machine-zero numerics are correctly framed as confirmation (R1); T_AP at 1e-16 and the
  adiabatic wide-wall limit verified in the figures (R3).
- The manifold-truncation caution is logically watertight and well quantified; Fig. `fig_manifold`
  matches the quoted 0.33 → 0.040 collapse exactly (R1, R2, R3).
- Table 2's six global optima and the zigzag polarized-window peaks reproduce Figs. 5–6 within
  reading precision; the sensitivity spread [0.014, 0.079] matches Fig. 7 exactly, largest
  excursions as stated; PF = 0.43 pW/K², κ_ph ≈ 1.1 nW/K and Wiedemann–Franz κ_e ≈ 1.7 nW/K
  reproduce ZT = 0.040; ZT(700 K) = 0.065 consistent between Fig. 5(c) and 6(d) (R3).
- Half-metallic window edges (−3.2/+1.0 eV) and T_↑(E_F) = 8 verified in Figs. 2–3 (R3).
- Journal fit: genuinely low-dimensional framing; no plausible desk-reject on scope; the
  no-fresh-DFT choice is preempted, not hidden; every abstract promise maps to a figure/table;
  §Scope is substantive and correctly placed; §2.4's notation is fully defined (R4).
- The planar approximation and the resulting exactness of the Slater–Koster selection rules are
  properly justified (R1).

---

### Dropped findings (failed adversarial verification)

- **R1 raised:** Δ^c_↓ = Δ_ex could be much smaller due to s-admixture, pulling the minority c
  replica into the transport window and threatening the 100%-polarization/OFF-window claims —
  **refuted:** arithmetically impossible from the draft's own numbers (the +1.0 eV edge is set by
  minority d+p_z states, not the c replica; even Δ^c_↓ = 2 eV leaves the replica at +1.8 eV,
  outside the window; Kuklin's reported 3.9 eV minority gap already includes the exact s-admixed
  minority conduction band).
- **R3 raised:** the quoted (S_↓ ≈ −150 μV/K at +1.05 eV) pair does not match
  `fig_spinseebeck`(a) — **refuted by recomputation:** the cached data (`data/zigzag_N14_TE.npz`
  via `crnte.thermo`) gives S_↓ = −152.3 and S_↑ = +4.4 μV/K exactly at +1.05 eV; the referee
  misread the figure's x-axis, and the point sits at G_↓ = 1.7 G₀, away from the divergent edge.

*Panel run 2026-07-29 (workflow wf_b254d524-d79, 27 agents). The manuscript was not modified.*
