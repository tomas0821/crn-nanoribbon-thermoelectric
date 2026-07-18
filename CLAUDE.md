# CLAUDE.md — CrN nanoribbon thermoelectric project

## What this project is
A single **theory/modelling paper** targeting **Physica E: Low-dimensional Systems and
Nanostructures** (ISSN 1386-9477, Elsevier). It computes the **thermoelectric transport**
of **hexagonal CrN nanoribbons** using a **tight-binding + Landauer–Büttiker** approach —
deliberately **analytical / lightweight, NO heavy DFT**. This is Blueprint 2 of a lit-gap
analysis run on 2026-07-14.

## Hard constraints (do not drift from these)
- **No DFT / no ab-initio.** Method must stay tight-binding + Green's-function transport.
  Parametrize the TB model from published band structures, not from a fresh DFT run.
- **Target journal = Physica E**, standard research-article format (theory welcome; reviews
  are invited-only, so this is a research article). Frame everything **low-dimensionally**
  (nanoribbon / monolayer), matching the journal's scope.
- Software should be lightweight Python: **Kwant** (quantum transport) and/or **PythTB**,
  plus NumPy/SciPy/Matplotlib. No VASP/QE.

## Files here
- `paper_plan_crn-nanoribbon-thermoelectric.md` — the full plan (pitch, calc order,
  software, figures, manuscript structure, timeline). **Start here.**
- `NOVELTY_CHECK.md` — the exact novelty-check queries + evidence as of 2026-07-14, and the
  one adjacent-but-non-colliding paper to cite (2024 DMRG CrN nanoribbon magnetism).

## Provenance / context
- Parent lit-gap report: `/home/tomas/mnt/gdrive/Research/Current/physicaE/publication_gaps_report.md`
- Toolkit (novelty re-checks): `/home/tomas/mnt/gdrive/Research/Current/lit-gap-toolkit/`
  Re-run before drafting: `python3 <toolkit>/check_novelty.py --query "CrN nanoribbon thermoelectric"`
- **Re-verify novelty right before writing** — the nitride-nanoribbon field moves fast.

## Environment & commands
- **Code is complete** (`crnte/` package + `scripts/`), manuscript drafted
  (`manuscript/manuscript.tex`). Run everything with `~/venvs/crn-te/bin/python` (isolated
  Kwant venv, Python 3.12, numpy<2 — system Python 3.14 cannot build Kwant). Everything runs
  on a laptop — no HPC, no VASP/QE. All production data quoted in the paper is cached in
  `data/` (git-ignored; regenerate via `scripts/run_all_transmissions.py` + the fig scripts).
- **Model note (2026-07-17):** the TB model is the EXTENDED 5-orbital one (d+p_z manifold + an
  effective conduction orbital `c` fitted to Kuklin's digitized majority conduction pocket).
  The reduced d+p_z manifold alone overestimates ZT ~8x (see `fig_manifold.png`) — do not
  revert to it. κ_ph comes from `crnte/phonon.py` (phonon Landauer anchored to Modarresi's
  DFPT dispersion), not from the old 4κ₀T estimate.
- **Novelty re-check** (run before drafting *and* before submission):
  ```
  python3 /home/tomas/mnt/gdrive/Research/Current/lit-gap-toolkit/check_novelty.py \
    --query "CrN nanoribbon thermoelectric" --query "CrN nanoribbon Landauer"
  ```
  Also re-check Semantic Scholar once it is not HTTP-429 rate-limited (see `NOVELTY_CHECK.md`).
- **Suggested code layout** when work begins: keep the self-consistent mean-field magnetism
  loop, the Kwant transport assembly, and the Onsager/thermoelectric integrals as separate
  modules — the calc order in the plan (§4) maps directly onto them. Follow the plan's figure
  numbering (Fig 1–6, Tables 1–2) for output filenames so scripts trace to manuscript figures.

## First thing to do in a fresh session
Read `00_Master_Notebook.md` (current state + honest headline results), then check the
AI-handoff list there. Remaining pre-submission items: make the GitHub repo public (data
statement promises it), run the final novelty re-check, submit.
