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
