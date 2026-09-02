"""Ballistic phonon thermal conductance of h-CrN ribbons (phonon Landauer, no new DFT).

The monolayer phonon dispersion is parametrized from the published DFPT/PHONOPY spectrum of
freestanding h-CrN in Modarresi et al., Phys. Rev. Applied 11, 064015 (2019), Fig. 4(a)
(digitized 2026-07-17 from the 300-dpi render; calibration: 33.07 px/THz from the frequency
axis labels, 298 px/Angstrom^-1 from the to-scale M-Gamma-K path; estimated accuracy ~0.3 THz).
Anchor values (THz), direction-averaged over Gamma-M and Gamma-K:

    acoustic:  v_LA ~ 8.5 km/s, v_TA ~ 4.3 km/s (low-q slopes), zone-edge maxima
               LA ~ 10.4, TA ~ 5.4, ZA ~ 4.7 (ZA quadratic near Gamma, alpha ~ 44 THz A^2)
    optical:   O1 13.7 -> 7.2, O2 13.2 -> 10.8, O3 16.85 -> 15.1 (Gamma -> zone edge)

Each branch is a smooth monotone interpolation between these anchors (sine-form for the linear
branches -- whose zone-edge value + sine slope reproduce the digitized low-q velocities, a
consistency check -- and a quadratic-to-linear crossover for ZA). This is deliberately an
ESTIMATE in the spirit of the paper: transparent inputs, no fresh ab-initio computation, and
the ZT results are reported with an explicit kappa_ph bracket around it.

Mode counting (isotropic-branch approximation): a ribbon of transverse width W supports, at
frequency omega, M_b(omega) = (W/pi) * q_b(omega) propagating channels of branch b, where
q_b(omega) is the iso-frequency radius. The four gapless ribbon modes (LA, TA, ZA, twist) give
a floor M >= 4 at low frequency [Rego & Kirczenow, PRL 81, 232 (1998)]. Then

    kappa_ph(T) = (1/2 pi) int_0^inf  d omega  hbar omega  (dn_B/dT)  M(omega).
"""
from __future__ import annotations

import numpy as np

HBAR = 1.054571817e-34   # J s
KB = 1.380649e-23        # J/K
THZ = 2.0 * np.pi * 1e12  # angular frequency of 1 THz (rad/s)

Q_ZONE = 1.20            # average zone-boundary |q| (1/Angstrom): Gamma-M 1.114, Gamma-K 1.286

# branch anchors, THz (nu, not omega): (value at Gamma, value at zone boundary)
ZA_ALPHA = 44.0          # ZA ~ alpha q^2 at small q (THz Angstrom^2)
N_FLOOR = 4.0            # gapless-ribbon-mode floor (4 = Rego-Kirczenow 3D beam; 3 = strictly-2D LA,TA,ZA)
ZA_MAX = 4.7
TA_MAX = 5.4
LA_MAX = 10.4
OPTICAL = [(13.7, 7.2), (13.2, 10.8), (16.85, 15.1)]   # (Gamma, zone-edge)


def _nu_sine(q, nu_max):
    """Monotone sine-form acoustic branch: nu(q) = nu_max sin(pi q / 2 q_zone)."""
    return nu_max * np.sin(0.5 * np.pi * np.clip(q, 0.0, Q_ZONE) / Q_ZONE)


def _nu_za(q):
    """ZA branch: quadratic at small q crossing over to the sine form near the zone edge."""
    quad = ZA_ALPHA * q * q
    sine = _nu_sine(q, ZA_MAX)
    return np.minimum(quad, sine)


def _q_of_nu(nu, nu_of_q, qgrid):
    """Iso-frequency radius: largest q with nu_of_q(q) <= nu (0 if nu above the branch)."""
    vals = nu_of_q(qgrid)
    if nu >= vals.max():
        return 0.0 if nu > vals.max() + 1e-9 else qgrid[-1]
    idx = np.searchsorted(vals, nu)          # branches here are monotone increasing on qgrid
    return qgrid[min(idx, len(qgrid) - 1)]


_QGRID = np.linspace(0.0, Q_ZONE, 2001)


def modes(nu_thz, W_angstrom):
    """Propagating phonon channel count M(nu) for a ribbon of transverse width W (Angstrom)."""
    nu = float(nu_thz)
    if nu <= 0:
        return N_FLOOR
    Wpi = W_angstrom / np.pi
    m = 0.0
    # acoustic branches (monotone increasing)
    for f, top in ((_nu_za, ZA_MAX), (lambda q: _nu_sine(q, TA_MAX), TA_MAX),
                   (lambda q: _nu_sine(q, LA_MAX), LA_MAX)):
        if nu <= top:
            m += Wpi * _q_of_nu(nu, f, _QGRID)
    # gapless-ribbon-mode floor (LA, TA, ZA, twist) below the acoustic region top
    if nu <= TA_MAX:
        m = max(m, N_FLOOR)
    # optical branches: sine-form decrease from nu_G (Gamma) to nu_Z (zone edge), so the
    # iso-frequency radius is q(nu) = (2 q_zone / pi) arcsin[(nu_G - nu)/(nu_G - nu_Z)]
    for nu_G, nu_Z in OPTICAL:
        if nu_Z <= nu <= nu_G:
            m += Wpi * Q_ZONE * (2.0 / np.pi) * np.arcsin(
                np.clip((nu_G - nu) / (nu_G - nu_Z), 0.0, 1.0))
    return m


def kappa_ph(T_K, W_angstrom, nu_max=18.0, n_omega=1200):
    """Ballistic phonon thermal conductance (W/K) of a ribbon of width W at temperature T."""
    nus = np.linspace(1e-3, nu_max, n_omega)
    omg = nus * THZ                                   # rad/s
    x = np.minimum(HBAR * omg / (KB * T_K), 60.0)     # overflow guard (tail ~ e^-x anyway)
    dndT = (HBAR * omg / (KB * T_K * T_K)) * np.exp(x) / np.expm1(x) ** 2
    M = np.array([modes(nu, W_angstrom) for nu in nus])
    integrand = HBAR * omg * dndT * M
    return np.trapz(integrand, omg) / (2.0 * np.pi)


def ribbon_width(edge: str, N: int, a: float) -> float:
    """Physical transverse width (Angstrom) of the width-N ribbon (same convention as ribbon_sk)."""
    from .ribbon_sk import _transverse_bound
    lo, hi = _transverse_bound(edge, N, a)
    return hi - lo
