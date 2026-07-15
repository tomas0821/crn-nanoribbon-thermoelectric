# 📓 Lab Notebook — CrN Nanoribbon Thermoelectric

**Started:** 2026-07-14
**Author:** Tomas Rojas

---

## 📥 AI Handoff & Next Actions

- [x] Rebuild the zigzag/armchair ribbons on the **fitted SK model** → `crnte/ribbon_sk.py`,
      `scripts/fig3_sk_transmission.py`. Faithful Fig. 3 done (see run below). *(2026-07-14)*
- [x] Compute thermoelectric integrals **S, PF, κ_e, ZT** from T(E) (Cutler–Mott/Onsager) → Figs. 4–5.
      Done: `crnte/thermo.py`, `scripts/fig45_thermoelectric.py`. See run below. *(2026-07-14)*
- [ ] Self-consistent mean-field **U at the ribbon edges** (inequivalent Cr sites) → spin-resolved
      edge bands; cross-check the DMRG J₁ ≈ 10–12 meV, J₂ ≈ −2–0 meV/Cr.
- [ ] Sweep ribbon **widths N = 8, 14, 20** (match the DMRG paper) for direct comparability.

---

## Project Overview

Theory/modelling paper for **Physica E**: thermoelectric transport of **hexagonal (honeycomb)
CrN nanoribbons** via **tight-binding + Landauer–Büttiker** (Kwant). Deliberately **no DFT** —
the TB model is parametrized by fitting published h-CrN bands (Kuklin et al., *Nanoscale* 9, 621
(2017)). See `paper_plan_*.md`, `NOVELTY_CHECK.md`, and `CLAUDE.md`.

**Novelty (re-verified 2026-07-14):** first **thermoelectric** (S, PF, ZT), **phase-coherent
Landauer** study of CrN nanoribbons. The one adjacent paper (DMRG, arXiv:2408.06754) does
DFT+DMRG+**Boltzmann** spin-filtering — no thermoelectric quantities — so we are complementary,
not colliding. (Claim is "first *thermoelectric*/Landauer", NOT "first transport".)

**Key observables:** spin-resolved transmission T_σ(E); Seebeck S; power factor PF = S²G;
electronic κ_e; figure of merit ZT = S²GT/(κ_e + κ_ph), vs μ, T, ribbon width, edge, spin.

**Method decisions (settled):**
- **No DFT** despite UCR cluster access — preserves novelty vs. the DMRG paper and the paper's
  lightweight identity. Rigor comes from transport + parameter-sensitivity analysis.
- **Reduced 4-orbital SK model** (Cr d_z²/d_xz/d_yz + N p_z): the in-plane σ manifold sits at
  −5.5 eV, irrelevant to transport. Passed the residual test → full Cr-5d + N-3p not needed.

**Environment:** isolated Kwant venv at `~/venvs/crn-te` (Python 3.12, numpy<2). System Python
3.14 cannot build Kwant. Run code with `~/venvs/crn-te/bin/python`. See `requirements.txt`.

**h-CrN targets (Kuklin, digitized → `crnte/kuklin_targets.py`):** a = 3.258 Å; half-metal,
3 μ_B/Cr; minority gap 3.9 eV; majority CBM at K = −0.2 eV, VBM touches E_F; minority VBM ≈
−3.0 eV, CBM ≈ +0.9 eV (E_F off-center in the gap); U = 3 eV.

---

## Simulation Logs

### Run: monolayer_sk_bands — 2026-07-14

Faithful reduced Slater–Koster model of the h-CrN monolayer, fitted to the digitized Kuklin
targets. **This is the current production monolayer model** (supersedes the cartoon below).

| Parameter (`SKParams`) | Value |
|-----------|-------|
| lattice constant a | 3.258 Å |
| eps_dz2 (Cr d_z², majority) | −2.3 eV |
| eps_pi (Cr d_xz/d_yz, bare) | −2.6 eV |
| eps_pz (N p_z) | −3.2 eV |
| pd_π (Cr d–N p_z) | 1.45 eV |
| t_zz (Cr–Cr 2nd-nbr d_z²) | 0.08 eV |
| exchange split Δ_ex | 3.6 eV |

**Final values (model vs. Kuklin target):**
| Observable | Model | Target |
|------------|-------|--------|
| majority character at E_F | metallic (crosses, +0.19 eV) | metallic (VBM touches E_F) |
| minority VBM | −3.2 eV | −3.0 eV |
| minority CBM | +1.0 eV | +0.9 eV |
| minority gap | 4.2 eV | 3.9 eV |
| non-bonding d_z² flat band | −2.55 eV | −2.3 eV |

**Notes:** Reproduces the half-metal (majority metallic, minority gapped, E_F inside the gap)
and near-E_F features to within ~0.2–0.3 eV — at/below the ±0.2 eV digitization noise floor, so
tuning was stopped there (no false precision). Physics insight: the band grazing E_F is the
**π-antibonding** (d_xz/d_yz + p_z), while d_z² is a flat non-bonding band below it. Sanity
checks (Hermiticity, d_z²–p_z decoupling) pass. Script: `scripts/fig2_sk_bands.py`.

![h-CrN reduced SK model vs Kuklin targets](figures/fig2_sk_bands.png)

---

### Run: thermoelectric_zigzag_N14 — 2026-07-14

Thermoelectric coefficients (Cutler–Mott/Onsager) from the spin-resolved T_σ(E) of the zigzag
CrN ribbon, fitted SK model. **This is the paper's headline result (Figs. 4–5).**

| Parameter | Value |
|-----------|-------|
| edge / width | zigzag / N ≈ 14 |
| fine T(E) grid | −1.2 … +1.5 eV, 0.005 eV (cached `data/zigzag_N14_TE.npz`) |
| μ sweep | −0.6 … +0.6 eV |
| κ_ph estimate | ballistic 4κ₀(T) = 1.14 nW/K at 300 K (bracketed 0.5×–2×) |

**Final values (300 K):**
| Observable | Value |
|------------|-------|
| peak power factor S²G | 2.18 pW/K² at μ−E_F = +0.19 eV (band edge) |
| peak ZT (ballistic κ_ph) | **0.48** at μ−E_F = +0.20 eV |
| ZT bracket (2×–0.5× κ_ph) | 0.26 – 0.85 |
| ZT(700 K), band-edge doping | ~0.4 – 1.2 (κ_ph bracket) |
| usable Seebeck at band edge | ~200–300 μV/K |

**Notes:** ZT peaks **right at the sharp majority transmission edge** (steep dT/dE at E_F) — the
half-metallic band edge is the thermoelectric sweet spot; the mechanism is clean and is the
paper's story. The κ_ph→0 electronic bound ZT_e *diverges in the gap* (S²G→0 and κ_e→0 together)
— reported only as an upper bound; the physical ZT uses the ballistic κ_ph and peaks at the edge.
Below E_F (metallic) S≈0. `crnte/thermo.py` validated vs. Mott formula + ZT_e self-consistency.
Scripts: `scripts/fig45_thermoelectric.py`.

![Seebeck S(μ) at 100/300/500 K](figures/fig4_seebeck.png)
![Power factor, ZT vs doping (κ_ph bracket), ZT(T)](figures/fig5_zt.png)

---

### Run: ribbon_transmission_sk — 2026-07-14

Spin-resolved Landauer transmission T(E) for zigzag & armchair CrN ribbons on the **fitted SK
model** (`crnte/ribbon_sk.py`). Multi-orbital Kwant build (Cr: 3 orbitals, N: 1), SK pd_π hopping
+ Cr–Cr t_zz. **This is the current production transport calculation.**

| Parameter | Value |
|-----------|-------|
| model | fitted reduced SK (`crnte/monolayer_sk.py`) |
| edges | zigzag, armchair |
| ribbon width | N ≈ 14 |
| energy window | −4.0 … +3.0 eV (181 pts) |
| runtime | ~33 s (laptop, MUMPS-less Kwant) |

**Final values:**
| Observable | Value |
|------------|-------|
| majority T at E_F (zigzag) | 14 (conducts) |
| minority T at E_F | 0 (gapped) → 100% spin-polarized |
| minority transport gap | ≈ [−3.2, +1.0] eV (matches monolayer SK) |
| majority upper band edge | ≈ +0.2 eV (sharp T drop 14→0) |

**Notes:** Faithful half-metallic filtering, now **two-sided** (minority gapped on both sides of
E_F) — fixes the cartoon's one-sided artifact. Consistent with the SK monolayer bands. Key
thermoelectric hook: the **sharp majority transmission edge at E_F** (steep dT/dE) should give a
large Seebeck coefficient. Feeds directly into the S/PF/ZT integrals (next). Script:
`scripts/fig3_sk_transmission.py`.

![Spin-resolved Landauer transmission (fitted SK model)](figures/fig3_sk_transmission.png)

---

### Run: ribbon_transmission_cartoon — 2026-07-14 *(superseded)*

Spin-resolved Landauer transmission T(E) for zigzag & armchair CrN ribbons (N ≈ 14), **on the
provisional 2-band cartoon model** — pipeline validation, to be redone on the SK model.

| Parameter | Value |
|-----------|-------|
| edges | zigzag, armchair |
| ribbon width | N ≈ 14 |
| model | provisional effective 2-band (`crnte/monolayer.py`) |
| energy window | −2.5 … +2.5 eV |

**Notes:** Clean quantized conductance plateaus (T = 2, 4, 6…) confirm the TB→Kwant→transport
chain works end-to-end. Half-metallic filtering visible: above E_F the minority channel is flat
zero while the majority conducts. One-sided filtering is a cartoon artifact (E_F at the gap
edge, not centered) — fixed by the SK model. Script: `scripts/fig3_transmission.py`.

![Spin-resolved Landauer transmission (cartoon model)](figures/fig3_transmission.png)

---

### Run: monolayer_bands_cartoon — 2026-07-14 *(superseded)*

Provisional 2-band effective monolayer model (Dirac-half-metal cartoon), first pipeline test.
Reproduced a = 3.258 Å and a 3.9 eV minority gap by construction, but imposed the moment and
mis-centered E_F. Superseded by `monolayer_sk_bands`. Script: `scripts/fig2_monolayer_bands.py`.

![Provisional cartoon monolayer bands](figures/fig2_monolayer_bands.png)
