"""Fit targets for the h-CrN monolayer TB model, digitized from Kuklin et al.,
Nanoscale 9, 621 (2017), Fig. 2d/3 + the paper text (c6nr07790k.pdf, in the project folder).

Energies are E - E_F in eV. "text-exact" values are quoted numerically in the paper; "figure"
values are read from Fig. 2d at ~+/-0.2 eV precision. These anchor the Slater-Koster + mean-field
fit (see the no-DFT decision in memory). Report parameter sensitivity rather than false precision.
"""

# --- structural (Kuklin, text-exact) ---
LATTICE_A = 3.258        # honeycomb lattice constant (Angstrom)
CRN_BOND = 1.884         # Cr-N bond length (Angstrom)
BUCKLING = 0.071         # +/- out-of-plane buckling (Angstrom); ~planar
U_EFF = 3.0             # DFT+U effective U* = U - J on Cr-d (eV)

# --- magnetism (text-exact) ---
MOMENT_CR = 3.0          # magnetic moment per Cr2+ (mu_B); must come OUT of mean-field U
FM_MINUS_AFM = -0.715    # FM ground state is 0.715 eV/2x2-cell below AFM

# --- half-metal gap (text-exact, PBE = HSE06) ---
MINORITY_GAP = 3.9       # spin-down band gap (eV)

# --- majority (spin-up) band features ---
MAJORITY = {
    "cbm_at_K": -0.2,        # text-exact: conduction-band min at K, just below E_F
    "vbm_touches_EF": 0.0,   # text-exact: valence-band top touches E_F on Gamma-M and K-Gamma
    "dz2_flatband": (-2.5, -2.0),   # figure+text: non-bonding d_z2 manifold near VB top
    "deep_pi_bands": (-4.5, -3.5),  # figure+text: (d_xz,d_yz)+N p_z pi-dative bands
}

# --- digitized LOWEST majority (spin-up) conduction band CB1 (Kuklin Fig. 2d) ------------------
# Digitized 2026-07-17 from the 300-dpi render of c6nr07790k.pdf p. 4. Calibration: E_F dashed
# line at page-y 1091, 66.2 px/eV from the axis digit labels; k-columns Gamma=646, M=750, K=853,
# Gamma'=957 (equal per-segment spacing). s is the path coordinate (Gamma=0, M=1, K=2, Gamma=3).
# Estimated accuracy +/-0.1 eV in the transport window, +/-0.3 eV near Gamma (band crowding).
# CB1 has the electron pocket at K (Kuklin text: CBM at K = -0.2 eV). The dip to +0.37 at
# s=0.75 is the CB1/CB2 anticrossing; a single effective band smooths through it. A second
# conduction band (CB2, min ~+0.6 near M) is NOT included in the model: it adds majority modes
# only above ~+0.5 eV.
CB1_DIGITIZED = [  # (s, E-E_F [eV])
    (0.00, 2.41), (0.10, 2.42), (0.25, 2.56), (0.50, 1.64), (0.75, 0.37),
    (0.90, 0.69), (1.00, 0.63), (1.10, 0.59), (1.25, 0.48), (1.50, 0.18),
    (1.75, -0.07), (1.90, -0.20), (2.00, -0.21), (2.10, -0.14), (2.25, 0.34),
    (2.50, 1.12), (2.75, 2.57), (2.90, 2.44),
]
# Weighted least-squares fit (weights favouring the transport window E < 1 eV) of a
# Cr-triangular-sublattice band eps_c + t_c1*S1 + t_c2*S2 + t_c3*S3:
CB1_FIT = {"eps_c": 0.9147, "t_c1": 0.2852, "t_c2": -0.0278, "t_c3": 0.0297}

# --- digitized top majority valence band VB1 (same calibration; for reference/plotting) --------
# Peaks at ~0 inside the Gamma-M and K-Gamma intervals (Kuklin text: VB touches E_F there),
# dips to -0.8 at M and -1.6 at K. NOTE: the reduced 4-orbital pi* band reproduces the ~0 top
# but places it near K rather than inside the intervals -- a stated limitation of the manifold.
VB1_DIGITIZED = [
    (0.75, -0.08), (1.00, -0.79), (1.25, -0.93), (1.50, -1.20), (1.75, -1.48),
    (2.00, -1.60), (2.10, -1.53), (2.25, -0.89), (2.50, -0.21),
]

# --- minority (spin-down) band features (figure, ~+/-0.2 eV) ---
MINORITY = {
    "vbm": -3.0,   # valence-band maximum (near M)
    "cbm": +0.9,   # conduction-band minimum (near M/K)  -> cbm - vbm = 3.9 eV gap
    # => E_F is ~3.0 eV above minority VBM and ~0.9 eV below minority CBM (asymmetric!)
}

# --- Cr d-orbital crystal-field ordering (Kuklin Fig. 3c; trigonal/D3h field) ---
# on-site energy centers (eV) for the DFT+U orbital groups; starting guesses for SK on-sites.
CF_ORBITAL_ENERGIES = {
    "dxy_dx2y2": -5.6,   # lowest: Cr sd2 hybrids, sigma with N sp2 (in-plane, deep)
    "dxz_dyz":   -4.4,   # middle: pi-dative with N p_z (out-of-plane)
    "dz2":       -2.3,   # highest: non-bonding, valence-band top -> dominates near E_F
}
N_ORBITAL_ENERGIES = {
    "sp_xy": (-5.7, -3.6),  # N sp_x p_y in-plane sigma (deep)
    "pz":    -4.4,          # N p_z pi (out-of-plane)
}
