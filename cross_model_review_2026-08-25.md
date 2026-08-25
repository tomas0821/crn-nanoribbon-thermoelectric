---
type: cross-model-review
draft: manuscript/manuscript.tex
date: 2026-08-25
referees: [kimi (model id not printed by CLI; incomplete run), antigravity/agy (model id not printed by CLI), deepseek-reasoner (via opencode), codex (gpt-5.6-terra)]
verdict: minor revisions
---

# Cross-model review — CrN nanoribbon thermoelectric

## Summary assessment

This manuscript has already been through three rounds of same-model (Claude) referee-panel
review. This pass used four different model families instead, specifically to surface
blind spots a single lab's training might share. It worked: all four referees independently
flagged the "Data and code availability" promise as broken (the repo was still private at
review time — this is now resolved, see below), and two independent models (DeepSeek and,
in an unfinished form, Kimi) independently derived the *same* phonon mode-counting critique
from first principles without prompting each other, which is a strong signal it's real. Three
findings — an undisclosed asymmetric μ-scan window, a factual mismatch between a quoted wall
transmission value and the cached data, and a genuine contradiction between a figure caption
and the body text — were missed by all three prior same-model rounds and are new, verified
catches from this exercise. Two of the referees (Antigravity, and to a lesser extent Codex)
also raised several MAJOR findings that turned out to already be explicit, numbered caveats in
the manuscript's own Scope and Limitations section; those are noted below as disclosed rather
than counted as fresh problems, and one (the c-orbital symmetry argument) is refuted outright
on physics grounds. Nothing found here undermines the paper's central claims (modest
thermoelectric performance, excellent spin filtering, the thermal spin valve, and the
methodological caution about missing bands) — the surviving items are a mix of one clean
factual correction, a few abstract/caption wording fixes, and two deeper physics questions
(the phonon mode floor, and optima sitting in the model's own acknowledged CB2-blind spot)
that are worth a paragraph each rather than new calculations.

## Major points

1. **[R-DeepSeek, R-Codex]** Five of the six Table 2 "global optimum" ZT values
   (μ−E_F = +1.05 to +1.09 eV) sit in the energy region the manuscript's own text says the
   model does not resolve (second conduction band + anticrossing above ~+0.5 eV) — verified
   numerically against `data/zigzag_N14_TE.npz`: at the reported zigzag-N14 optimum
   (μ−E_F=+1.08 eV), the majority channel already carries 5 conductance quanta, i.e.
   substantial spectral weight sits exactly where the paper calls the model unresolved. —
   *Fix:* Either extend the model through the CB2/anticrossing region before quoting optima
   there, or explicitly flag in §3.5/Table 2 that the headline minority-edge numbers are
   conditional on unresolved spectral weight, promoting the armchair N=8 in-window value
   (immune to this issue) as the one fully load-bearing number.

2. **[R-DeepSeek]** The chemical-potential scan used to define "global optimum" throughout the
   paper is an undisclosed, asymmetric window — confirmed in `scripts/fig6_width_edge_vacancy.py:29`:
   `MU = np.linspace(-0.6, 1.2, 361)`. This range appears nowhere in the manuscript (§2.3,
   Table 2's caption, and Fig. 6's caption were all checked). The p-type half of the
   half-metallic window (μ−E_F < −0.6 eV) is never searched, so "global optimum", "most
   geometries", and the armchair-N=8 "exception" language are only true within an undisclosed
   domain. — *Fix:* State the scan domain explicitly wherever "global optimum" is claimed, and
   either extend the scan into the p-type region or soften the language to "optimum within the
   explored window."

3. **[R-DeepSeek, R-Kimi (independent, unfinished)]** `crnte/phonon.py` imposes a floor of 4
   gapless acoustic modes at low frequency, citing Rego & Kirczenow's result for a 3D elastic
   beam (dilatational + torsional + 2 flexural branches). The manuscript's own phonon
   dispersion is anchored to a strictly planar 2D sheet (explicitly stated: "we treat the
   sheet as strictly planar") with 6 branches from a 2-atom cell — 3 acoustic (LA, TA, ZA) + 3
   optical — with no "twist"/torsional branch among the digitized anchors. Two independent
   models derived, without seeing each other's output, that a 2D membrane should have 3
   gapless acoustic branches, not 4, making the injected 4th mode look like an uncritical
   carry-over of a 3D-beam result rather than a property of this system. — *Fix:* Either
   justify the 4th mode's physical origin for this specific geometry, or correct the floor to
   3 modes and note how much (likely modest, since this mainly affects the low-T tail rather
   than the 300 K headline numbers) κ_ph and the quoted ZT values shift.

## Minor points

- **[R-DeepSeek]** `data/wall_sweep.txt` gives T(+0.0) = 0.6275 at λ=0.79 Å and 0.6216 at
  λ=1.57 Å (no point sampled at exactly λ=1 Å) — both bracket to ≈0.62–0.63, not the
  manuscript's quoted "T_AP≃0.7" at λ≃1 Å. This is a clean, data-verified numeric correction.
  The downstream "ON/OFF ratio of order ten" claim is unaffected either way (8/0.62≈13,
  8/0.7≈11).
- **[R-Codex, R-DeepSeek]** Fig. 3's caption states the current is "100% spin polarized
  throughout the accessible doping window," while §3.6 states P_G drops to 49% at +1.05 eV and
  crosses zero near +1.1 eV. Checked `scripts/fig3_sk_transmission.py:26`
  (`ENERGIES = np.linspace(-4.0, 3.0, 181)`): the figure's own plotted range extends well past
  +1.05–1.1 eV, i.e. into the region the body text itself says loses polarization. This is a
  genuine contradiction, not a scoping non-issue. *Fix:* bound the caption's claim to the
  actual polarized window (≲+1.0 eV) or note the loss of polarization above it.
- **[R-DeepSeek]** The abstract's "honest optima are ZT≃0.04–0.15" doesn't reflect that 3 of 6
  geometries' π*-pinned-variant global optima (0.028, 0.033, 0.027 — confirmed against
  `data/pistar_pinned.txt`) fall below that stated floor. Narrower than DeepSeek's original
  MAJOR framing, though: §3.5 already discusses this degradation in prose with the same
  numbers, so it's an abstract-length omission, not a hidden result. *Fix:* one qualifying
  clause in the abstract.
- **[R-DeepSeek]** The transport Hamiltonian has no spin-orbit coupling, yet §3.7 separately
  relies on a SOC-derived anisotropy K (from Modarresi's DFT+U+SOC calculation) to compute
  λ_int in the same section that calls the collinear antiparallel OFF state "exact." A real
  junction would have some (likely negligible) SOC-mediated spin-flip leakage, making "exact"
  a property of the SOC-free model rather than guaranteed by the material. Practically small,
  but a genuine, previously-uncaught internal-consistency point — this is exactly the kind of
  catch the cross-model exercise exists to surface. *Fix:* one caveat sentence.
- **[R-Antigravity]** 700 K ballistic-transport projections are not covered by any of the six
  existing Scope caveats (the T_C caveat addresses magnetic order, not phase-coherence length
  / electron-phonon dephasing at high T, which is a separate physical concern). Mitigated by
  the paper's blanket "coherent ballistic picture" framing throughout, but a short explicit
  sentence would close the gap.
- **[R-Codex, R-Antigravity, R-Kimi]** §3.7 says the LKAG exchange fit "reproduce[s] the sign
  and hierarchy of the DMRG couplings" one clause before admitting "(the sign of the small J₂
  is not resolved at this level)" — J₂ is +0.8 meV (LKAG) vs −2 to 0 meV (DMRG), i.e. opposite
  sign. Self-contradictory within one sentence; reword to state plainly that only J₁'s sign and
  the |J₁|≫|J₂| hierarchy are reproduced, with J₁ itself off by a factor of ~5.
- **[R-Kimi, independently]** Fig. 6(d)'s caption says it is "plotted from 100 K, below which
  the production energy grid is not converged" (implying 100 K itself is fine), while §2.3
  says "at 100 K the same quantity still drifts by ~6%...which is why...≲100 K absolute values
  are not quoted" — the figure plots the one temperature point the text seems to disclaim.
  Boundary-phrasing inconsistency; reword one of the two statements.
- **[R-DeepSeek]** Abstract says "gapped over nearly 4 eV"; Fig. 3's caption says "gapped over
  more than 4 eV" — same 4.2 eV model gap, inconsistent descriptor. Trivial; pick one.
- **[R-Antigravity]** κ_ph bracket quoted in descending order ("0.047–0.030") next to the
  sensitivity spread in ascending order ("[0.014, 0.079]") — cosmetic formatting
  inconsistency.

## Where the models disagreed

The most interesting divergence is on the "exact" T_AP=0 spin-valve claim: Codex argued the
"exact OFF" state should fail at finite temperature because Fermi-window tails leak past a
gap edge — verification showed this doesn't hold, because the OFF claim spans the *entire*
4.2 eV gap and the paper's discussion point (E_F) sits many kT from either edge even at 700 K,
so the finite-T integral is still exactly zero. DeepSeek, attacking the same sentence from a
different angle (no SOC in the model, despite SOC-derived numbers being used elsewhere in the
same section), landed on a real, if practically small, gap that Codex's version missed
entirely. Neither model flagged the other's angle — a clean example of genuine model-diversity
payoff on a single sentence.

A second divergence: Antigravity raised the unhybridized c-orbital's symmetry decoupling as a
MAJOR "unphysical scattering artifact" at edges/domain walls; none of the other three referees
touched this. On inspection it doesn't hold up — the decoupling is a mirror-plane (σ_h)
selection rule that neither ribbon edges (in-plane boundaries) nor the noncollinear domain-wall
texture (a spin-space rotation, not a new spatial hopping, since the model has no SOC) can
break. Worth recording as a case where a referee-specific blind spot (over-eager pattern-matching
to "decoupled orbital = suspicious") produced a plausible-sounding but physically unfounded
MAJOR that a same-model panel might have deferred to without the domain-specific check.

## What was checked and found sound

- The repo's public/tagged-release status: confirmed live (`gh repo view` → public;
  `v1.0-submission` tag present) — the one finding all three complete referees raised
  independently is resolved as of this session, after the referees read the draft.
- Table 2's baseline optima and the π*-pinned systematic's numbers: match `data/table2.txt`
  and `data/pistar_pinned.txt` exactly.
- T↑(E_F)=8, T_AP(E)=0 identically over the reported window, λ_1/2=9.11 Å: all reproducible
  from the cache, per R-DeepSeek's own verification pass.
- The T_C≈209 K caveat and the rigid-band/no-self-consistent-screening caveat, both raised as
  MAJOR by Antigravity and (for T_C) also by Codex: both are already explicit, numbered
  caveats in the manuscript's own Scope and Limitations section, verbatim what the referees
  asked for. Downgraded — these are not gaps, they were already disclosed before this review
  ran.
- The hand-tuned d+p_z parameter fit (flagged MAJOR by Codex and DeepSeek): the manuscript
  already discloses this openly, states its residuals, and quantifies the consequence via the
  ±10% sensitivity sweep; only the automated c-orbital fit (the piece driving the headline
  physics) has a deposited objective function. Downgraded from MAJOR to a minor
  nice-to-have.

## Pipeline notes / dropped findings

- **R-Kimi did not finish.** Its CLI call timed out (10 min budget) mid-verification, after
  extensive manual derivation but before emitting a formatted `severity:` report. Its
  substantive content (the phonon mode-count derivation) is folded into Major point 3 above,
  credited as an independent confirmation; its other in-progress notes (the Fig. 6(d)
  boundary-phrasing point, folded into Minor points above) were extracted from the raw
  transcript rather than a formal report. No MAJOR finding from Kimi was lost to the timeout —
  the mode-count issue was its only fully-reasoned candidate.
- **Dropped as refuted:** Antigravity's claim that the effective conduction orbital's
  mirror-symmetry decoupling causes "severe unphysical scattering artifacts" at edges/domain
  walls (see "Where the models disagreed" above).
- **Downgraded from MAJOR to already-disclosed/minor** (not dropped, but not counted as fresh
  problems): the T_C≈209 K vs 300–700 K transport claims (Codex, Antigravity); the rigid-Δ_ex/
  no-self-consistent-screening-under-gating point (Antigravity); the hand-tuned Hamiltonian
  reproducibility point (Codex, DeepSeek); the π*-pinned-variant-vs-abstract-floor point
  (DeepSeek, narrowed from MAJOR to a one-clause abstract fix since §3.5 already discloses it
  in prose).
- **Not independently re-verified** (noted but not adjudicated in depth): Codex's λ_int
  cross-consistency concern (combining DMRG J1, monolayer K, a continuum wall formula and a
  non-self-consistent transport Hamiltonian) and the general novelty-framing MINOR points from
  multiple referees — both are already substantially hedged in the current text ("an
  order-of-magnitude estimate", "to our knowledge") and did not seem to warrant further
  investigation within this pass's scope.
