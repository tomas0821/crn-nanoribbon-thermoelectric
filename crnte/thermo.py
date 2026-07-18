"""Landauer/Onsager thermoelectric coefficients from a transmission function T(E).

Model-agnostic: give it an energy grid (eV) and T(E) (dimensionless, per spin), get the linear-
response coefficients. Formulas (Cutler-Mott / Onsager), per spin channel:

    L_n(mu,T) = integral (-df/dE) (E-mu)^n T(E) dE           [L0 dimensionless, L1 eV, L2 eV^2]
    G   = (e^2/h) L0                                          electrical conductance [S]
    S   = -(1/(e T)) L1/L0                                    Seebeck coefficient    [V/K]
    kappa_e = (1/(h T)) (L2 - L1^2/L0)                        electronic thermal conductance [W/K]
    PF  = S^2 G                                               power factor           [W/K^2]
    ZT_e = S^2 G T / kappa_e = L1^2 / (L0 L2 - L1^2)          electronic (kappa_ph -> 0) ZT
    ZT   = S^2 G T / (kappa_e + kappa_ph)                     full ZT (needs kappa_ph)

ZT_e is unit-free and is the kappa_ph -> 0 upper bound. Two spin channels combine as parallel
conductors (see combine_spins).
"""
from __future__ import annotations

import numpy as np

Q = 1.602176634e-19      # elementary charge (C)  [and eV -> J]
H = 6.62607015e-34       # Planck constant (J s)
KB = 1.380649e-23        # Boltzmann constant (J/K)
KB_EV = KB / Q           # Boltzmann constant (eV/K) = 8.617e-5
G0 = Q * Q / H           # conductance quantum e^2/h (S) = 3.874e-5


def dfermi(E_eV, mu_eV, T_K):
    """-df/dE (units 1/eV) for the Fermi function; numerically stable."""
    kT = KB_EV * T_K
    x = (np.asarray(E_eV) - mu_eV) / kT
    out = np.zeros_like(x, dtype=float)
    ok = np.abs(x) < 40.0
    out[ok] = 1.0 / (4.0 * kT * np.cosh(x[ok] / 2.0) ** 2)
    return out


def onsager(E_eV, TE, mu_eV, T_K):
    """Return (L0, L1, L2) for one spin channel. Energies in eV; TE dimensionless."""
    w = dfermi(E_eV, mu_eV, T_K)          # 1/eV
    de = E_eV - mu_eV
    L0 = np.trapz(w * TE, E_eV)
    L1 = np.trapz(w * TE * de, E_eV)
    L2 = np.trapz(w * TE * de * de, E_eV)
    return L0, L1, L2


def coefficients(E_eV, TE, mu_eV, T_K):
    """Thermoelectric coefficients for one spin channel at chemical potential mu, temperature T.

    Returns dict: G [S], S [V/K], kappa_e [W/K], PF [W/K^2], ZT_e [-], and raw L0,L1,L2.
    """
    L0, L1, L2 = onsager(E_eV, TE, mu_eV, T_K)
    if L0 <= 1e-9:   # no states in the Fermi window (physical L0 >~ 1e-3): insulating.
        # Guards against exponentially small L0 producing spurious huge S = L1/L0.
        return dict(G=0.0, S=0.0, kappa_e=0.0, PF=0.0, ZT_e=0.0, L0=L0, L1=L1, L2=L2)
    G = G0 * L0                                    # S
    S = -(1.0 / T_K) * (L1 / L0)                   # V/K   (L1/L0 in eV -> eV/e/K = V/K)
    kappa_e = (1.0 / (H * T_K)) * (L2 - L1 * L1 / L0) * Q * Q   # W/K  (eV^2 -> J^2 via Q^2)
    PF = S * S * G                                 # W/K^2
    denom = L0 * L2 - L1 * L1
    ZT_e = (L1 * L1 / denom) if denom > 0 else 0.0
    return dict(G=G, S=S, kappa_e=kappa_e, PF=PF, ZT_e=ZT_e, L0=L0, L1=L1, L2=L2)


def sweep_mu(E_eV, TE, mu_array, T_K):
    """Vectorized sweep of coefficients over mu. Returns dict of arrays (same keys as above)."""
    keys = ("G", "S", "kappa_e", "PF", "ZT_e")
    out = {k: np.empty(len(mu_array)) for k in keys}
    for i, mu in enumerate(mu_array):
        c = coefficients(E_eV, TE, mu, T_K)
        for k in keys:
            out[k][i] = c[k]
    return out


def combine_spins(cup, cdn, T_K):
    """Combine two spin channels as parallel conductors at temperature T_K (arrays or scalars).

    G_tot   = G_up + G_dn
    S_tot   = (sum_s G_s S_s) / G_tot
    kappa_e = (kappa_up + kappa_dn) + T * [ sum_s G_s S_s^2 - (sum_s G_s S_s)^2 / G_tot ]

    The bracket is the bipolar (circulating-current) term for parallel thermoelectric channels
    (non-negative by Cauchy-Schwarz); it vanishes for a single conducting channel or when the two
    channels have equal thermopower, and is exactly zero where the minority channel is gapped.
    Returns dict with G, S, kappa_e, PF.
    """
    G = cup["G"] + cdn["G"]
    Gsafe = np.where(G > 0, G, 1.0)
    GS = cup["S"] * cup["G"] + cdn["S"] * cdn["G"]          # sum_s G_s S_s
    GS2 = cup["S"] ** 2 * cup["G"] + cdn["S"] ** 2 * cdn["G"]  # sum_s G_s S_s^2
    S = GS / Gsafe
    bipolar = T_K * (GS2 - GS ** 2 / Gsafe)
    kappa_e = cup["kappa_e"] + cdn["kappa_e"] + bipolar
    PF = S * S * G
    return dict(G=G, S=S, kappa_e=kappa_e, PF=PF)


def ZT(coef_total, T_K, kappa_ph=0.0):
    """Full ZT = S^2 G T / (kappa_e + kappa_ph) from a combined-channel dict."""
    denom = coef_total["kappa_e"] + kappa_ph
    denom = np.where(denom > 0, denom, np.inf)
    return coef_total["S"] ** 2 * coef_total["G"] * T_K / denom


# universal thermal conductance quantum coefficient: kappa_0(T) = KAPPA0 * T  [W/K per mode]
KAPPA0 = np.pi ** 2 * KB ** 2 / (3.0 * H)     # = 9.464e-13 W/K^2


def kappa_ph_ballistic(T_K, n_modes=4):
    """Lightweight ballistic (phonon-Landauer) estimate of the ribbon phonon thermal conductance.

    kappa_ph = n_modes * kappa_0(T), the quantum upper bound for n_modes acoustic-like branches
    (a nanoribbon has ~4). This is an ESTIMATE, not DFT-computed (see the paper's stated scope);
    ZT should be reported for a bracket around it.
    """
    return n_modes * KAPPA0 * T_K
