# Paper Plan — Thermoelectric transport in CrN nanoribbons (tight-binding + Landauer)

**Target:** Physica E: Low-dimensional Systems and Nanostructures (ISSN 1386-9477)
**Format:** standard research article (theory)
**Method register:** analytical / lightweight — tight-binding + Landauer–Büttiker. **No DFT.**
**Status:** planned 2026-07-14; novelty re-verified same day (see `NOVELTY_CHECK.md`).

---

## 1. Working title (pick one at submission)
- *"Thermoelectric transport in hexagonal CrN nanoribbons: a tight-binding Landauer study of Seebeck coefficient and figure of merit"*
- *"Width- and edge-controlled thermoelectric response of CrN nanoribbons from a mean-field tight-binding model"*

## 2. Pitch / novelty statement (one paragraph, reuse in cover letter)
Nanoribbon thermoelectrics computed from tight-binding + Landauer transport is one of the
most reliably published formats in low-dimensional physics (graphene, silicene, phosphorene,
SiC, borophene ribbons). **Chromium nitride has never been placed in this framework.** CrN
thermoelectricity is known only from *experimental thin films*, and the only CrN-nanoribbon
theory in existence (a 2024 DMRG study) addresses **magnetic order, not transport**. We close
this gap with a spin-resolved tight-binding + Landauer model of hexagonal CrN armchair and
zigzag nanoribbons, mapping the Seebeck coefficient, power factor, and figure of merit ZT
versus ribbon width, chemical potential, temperature, and — exploiting CrN's magnetic edges —
spin channel. The work needs no ab-initio computation and yields design rules (optimal width,
doping window, edge type) for CrN-based low-dimensional thermoelectrics.

**Novelty is method+material, not method alone** — be explicit that the TB/Landauer template
is standard; the contribution is the first transport-level, spin-resolved thermoelectric map
of a specific, experimentally-relevant magnetic nitride ribbon.

## 3. Physical system & model choices
- **Material realization:** hexagonal (honeycomb, h-BN-like) **CrN monolayer**, then cut
  **armchair (ACNR)** and **zigzag (ZCNR)** nanoribbons of several widths N. This follows the
  precedent of the 2024 DMRG paper (which used *hexagonal* CrN nanoribbons) and the h-GaN /
  h-NbN monolayers already in the Physica E corpus. Justify the honeycomb allotrope up front
  (cite the DMRG paper + h-nitride monolayer literature); note rocksalt-derived ribbons as an
  appendix/outlook alternative.
- **Electronic Hamiltonian:** minimal multi-orbital Slater–Koster tight-binding — Cr d
  (at least the relevant t2g/eg subset) + N p — parametrized to reproduce a *published* CrN
  monolayer band structure (metal↔semiconductor character, gap, band ordering). Do **not**
  run DFT; take parameters from literature or fit to a published band plot.
- **Magnetism:** CrN edges are magnetic (DMRG result). Include a **mean-field Hubbard U** on
  the Cr d-orbitals solved self-consistently → spin-resolved bands. This is still analytical
  (mean-field decoupling), not DFT. Keep U as a small parameter set explored over a range.
- **Transport:** semi-infinite leads = same ribbon; central scattering region for
  disorder/vacancy studies. Landauer–Büttiker transmission T(E) (and Tσ(E) per spin) via
  **recursive Green's functions** — this is exactly what **Kwant** does out of the box.
- **Thermoelectric coefficients** from the Onsager/Cutler–Mott integrals:
  Lₙ = (2/h) ∫ (−∂f/∂E)(E−μ)ⁿ T(E) dE, with
  G = e²L₀, S = L₁/(eT L₀), κₑ = (L₂ − L₁²/L₀)/T, power factor PF = S²G,
  and ZT = S²G T / (κₑ + κ_ph).
- **Phonon thermal conductivity κ_ph** (the only non-electronic piece): keep it lightweight —
  a 1D mass-spring / harmonic phonon-Landauer estimate, or treat κ_ph parametrically and
  report both electronic ZTₑ (κ_ph→0 bound) and ZT for a bracket of literature κ_ph values.
  **Be transparent that κ_ph is estimated, not DFT-computed** — this is a stated limitation,
  not a hidden one.

## 4. Calculation order (magnetic screening BEFORE transport — the system is magnetic)
1. **Reproduce the monolayer band structure** with the TB parameter set; verify metal/
   semiconductor character against literature. (Sanity gate.)
2. **Self-consistent mean-field magnetism** for each ribbon (ACNR/ZCNR, widths N): converge
   edge magnetic moments, get spin-resolved bands. Confirm qualitative agreement with the
   2024 DMRG edge-magnetism result — this cross-check is a selling point.
3. **Transmission** Tσ(E) for each converged ribbon (Kwant).
4. **Thermoelectric sweep:** S, G, κₑ, PF, ZT vs μ and T for each width/edge/spin.
5. **Edge-disorder / vacancy study:** ZT enhancement via edge vacancies (well-known in ZGNRs)
   — a cheap, high-impact extra figure.
6. **κ_ph estimate** and final ZT assembly with the stated bracket.

## 5. Software stack (all lightweight, no DFT)
- **Kwant** — tight-binding assembly + Landauer transport + built-in thermoelectric machinery.
- **PythTB** (optional) — clean band-structure plots and parameter fitting.
- **NumPy / SciPy** — self-consistent mean-field loop, Onsager integrals, numerical
  derivatives.
- **Matplotlib** — figures.
- Everything runs on a laptop; no HPC, no VASP/QE. Keep a `requirements.txt` (kwant, numpy,
  scipy, matplotlib) — note this is normal research tooling, unrelated to the stdlib-only
  constraint of the lit-gap *toolkit*.

## 6. Figures & tables to plan for
- **Fig 1** — h-CrN monolayer + ACNR/ZCNR geometry, width convention, magnetic edge sketch.
- **Fig 2** — spin-resolved TB band structures vs width; metal↔semiconductor evolution.
- **Fig 3** — transmission Tσ(E) for representative widths (both edges).
- **Fig 4** — Seebeck S(μ, T); highlight sign changes / bipolar behavior.
- **Fig 5** — power factor, κₑ, and ZT vs μ and width at fixed T; ZT(T) at optimal μ.
- **Fig 6** — spin-Seebeck / spin-resolved ZT (exploits magnetic edges) **and/or** edge-vacancy
  enhancement of ZT.
- **Table 1** — TB (Slater–Koster) parameters + U, with the literature source they reproduce.
- **Table 2** — peak ZT, optimal μ, and width for each edge/spin; brief comparison to other
  nanoribbon thermoelectrics.

## 7. Manuscript structure (Physica E research-article template)
1. Introduction — low-dim thermoelectrics; nitride nanoribbons; CrN's experimental TE +
   magnetic-edge context; the explicit gap; contribution.
2. Model and method — geometry; TB Hamiltonian; mean-field magnetism; Landauer transport;
   thermoelectric coefficients; κ_ph treatment.
3. Results and discussion — bands → transmission → S/PF/κₑ/ZT → spin/disorder.
4. Conclusions — design rules; limitations (κ_ph estimate, TB parametrization); outlook
   (rocksalt ribbons, gating, strain).
- Length ~8–12 pp, 6 figures + 2 tables. Highlights + a short Statement-of-novelty paragraph.

## 8. Rough timeline (part-time)
- **Week 1** — TB parametrization + monolayer band reproduction (Fig 1–2 skeleton).
- **Week 2** — self-consistent mean-field magnetism for all ribbons; cross-check vs DMRG.
- **Week 3** — Kwant transport + thermoelectric sweeps (Fig 3–5).
- **Week 4** — spin/disorder study + κ_ph estimate (Fig 6); Table assembly.
- **Weeks 5–6** — writing, novelty re-check, internal review, submission.

## 9. Risk register
- **TB parametrization fidelity** — mitigate by fitting to a published band structure and
  reporting sensitivity to parameters.
- **κ_ph without DFT** — mitigate by bracketing and reporting electronic ZTₑ as an upper
  bound; frame as scope, not omission.
- **The 2024 DMRG CrN-nanoribbon paper** — turn into an asset: use it to validate edge
  magnetism and to differentiate on property (transport) + method (analytical). Read it in
  full and match its ribbon geometry so the two papers are complementary.
- **Novelty drift** — nitride-nanoribbon preprints appear often; re-run the novelty check
  immediately before submission.
