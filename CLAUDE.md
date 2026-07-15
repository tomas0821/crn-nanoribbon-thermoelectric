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
- **No code exists yet** — this repo is currently plan + novelty-check notes only. When you
  start coding, create a `requirements.txt` (`kwant`, `numpy`, `scipy`, `matplotlib`; PythTB
  optional) and a virtual env; Kwant installs cleanly via conda/pip. Everything runs on a
  laptop — no HPC, no VASP/QE.
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
Read `paper_plan_...md`, then re-run the novelty check. The lowest-risk starting deliverable
is Fig. 2 + Fig. 3 (TB band structures + transmission) for hexagonal CrN armchair/zigzag
ribbons in Kwant.
