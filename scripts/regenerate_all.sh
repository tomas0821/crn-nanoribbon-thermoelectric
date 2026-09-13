#!/usr/bin/env bash
# Regenerate every production number and figure after a model change (here: the second
# effective conduction orbital c2). Clears the transport caches first (back up data/ before!),
# then runs the scripts in dependency order and copies the manuscript figures into place.
# Usage:  bash scripts/regenerate_all.sh  2>&1 | tee data/regenerate_all.log
set -euo pipefail
cd "$(dirname "$0")/.."
PY=~/venvs/crn-te/bin/python
export PYTHONWARNINGS=ignore

echo "== $(date) clearing transport caches (keeping edgemag.npz and the reduced-manifold *_noc.npz, which the c2 change does not touch) =="
find data -maxdepth 1 -name '*.npz' ! -name 'edgemag.npz' ! -name '*_noc.npz' ! -name 'kuklin_fig2d_traces.npz' -delete

run() { echo; echo "== $(date) $1 =="; $PY "scripts/$1" 2>&1 | grep -v MUMPS; }

run run_all_transmissions.py
run fig2_sk_bands.py
run fig3_sk_transmission.py
run fig45_thermoelectric.py
run fig6_width_edge_vacancy.py
run fig_armchair8.py
run fig_spinseebeck.py
run fig_manifold_comparison.py
run fig_spinvalve.py
run convergence.py
run phonon_floor3.py
run ptype_scan.py
run sensitivity_delta_c.py
run pistar_pinned.py
run sensitivity.py
run sensitivity_armchair8.py
run fig_wall.py
run verify.py

echo; echo "== $(date) copying manuscript figures =="
cp figures/fig2_sk_bands.png            manuscript/figures/fig2_bands.png
cp figures/fig3_sk_transmission.png     manuscript/figures/fig3_transmission.png
cp figures/fig6_width_edge_vacancy.png  manuscript/figures/fig6_designrules.png
for f in fig5_zt fig7_sensitivity fig_armchair8 fig_manifold fig_spinseebeck fig_spinvalve fig_wall; do
  cp "figures/$f.png" "manuscript/figures/$f.png"
done
echo "== $(date) DONE =="
