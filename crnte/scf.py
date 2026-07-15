"""Self-consistent mean-field (unrestricted Hartree-Fock) machinery for CrN ribbon EDGES.

Stage 1 (this file, verified below): a hand-built 1D Bloch Hamiltonian H_sigma(k) for a ribbon of
width N, with a SITE-DEPENDENT exchange shift on the Cr d orbitals -- the quantity the SCF loop
will iterate. Constructing it by hand (rather than via Kwant) gives a clean orbital<->site index
map, needed to project eigenvectors back onto sites for the occupation update.

The ribbon unit cell is periodic along the transport axis T; H(k)=H0 + V e^{ikT} + V^dag e^{-ikT}.
Cr sites carry 3 orbitals (d_z2, d_xz, d_yz), N sites 1 (p_z), same Slater-Koster hoppings as
crnte.ribbon_sk (pd_pi for Cr-N, t_zz for Cr-Cr d_z2). Later stages add: bulk filling/U
calibration, the SCF occupation loop, the edge moment profile, and J1/J2 from magnetic-config
energies.
"""
from __future__ import annotations

import numpy as np

from .monolayer_sk import SKParams
from .ribbon_sk import _transverse_bound

_S3 = np.sqrt(3.0)


def ribbon_cell(edge: str, N: int, a: float):
    """Sites of one ribbon unit cell (kwant-honeycomb convention). Returns (cr, nn, T, tc)."""
    d = a / _S3
    pv0 = np.array([a, 0.0])
    pv1 = np.array([a / 2.0, a * _S3 / 2.0])
    lo, hi = _transverse_bound(edge, N, a)
    if edge == "zigzag":
        T = np.array([a, 0.0]); tc, lc = 1, 0        # transverse=y, transport=x
    elif edge == "armchair":
        T = np.array([0.0, a * _S3]); tc, lc = 0, 1    # transverse=x, transport=y
    else:
        raise ValueError(edge)
    Tlen = np.linalg.norm(T)
    cr, nn = [], []
    R = 3 * N + 8
    for n in range(-R, R + 1):
        for m in range(-R, R + 1):
            base = n * pv0 + m * pv1
            for pos, lst in ((base, cr), (base + np.array([0.0, d]), nn)):
                if lo - 1e-6 <= pos[tc] <= hi + 1e-6 and -1e-6 <= pos[lc] < Tlen - 1e-6:
                    lst.append(pos)
    return np.array(cr), np.array(nn), T, tc


def _hop_block(A_is_cr, B_is_cr, bond, p, d):
    """Hopping matrix from site A's orbitals to site B's orbitals for separation `bond`=posB-posA."""
    dist = np.linalg.norm(bond)
    if A_is_cr and B_is_cr:                       # Cr-Cr 2nd neighbour: d_z2-d_z2 only
        if abs(dist - p.a) < 0.15 * p.a:
            return np.diag([p.t_zz, 0.0, 0.0]).astype(complex)
        return None
    if A_is_cr and (not B_is_cr):                 # Cr(d) -> N(p_z), Cr->N cosines
        if abs(dist - d) < 0.15 * d:
            l, m = bond / d
            return p.pdpi * np.array([[0.0], [l], [m]], dtype=complex)   # 3x1
        return None
    if (not A_is_cr) and B_is_cr:                 # N(p_z) -> Cr(d), Cr->N direction = -bond
        if abs(dist - d) < 0.15 * d:
            l, m = -bond / d
            return p.pdpi * np.array([[0.0, l, m]], dtype=complex)       # 1x3
        return None
    return None                                    # N-N: no hopping


def build_bloch(edge: str, N: int, p: SKParams, spin: int, exchange=None):
    """Return (H0, V, cr_index, rows). H(k)=H0+V e^{ikT}+V^dag e^{-ikT}.

    exchange: optional array of per-Cr-site exchange shifts added to that Cr's d orbitals (eV). If
    None, the uniform fitted shift ``p.cr_shift(spin)`` is used on every Cr (reproduces ribbon_sk).
    cr_index[i] = (i0,i1,i2) orbital indices of Cr site i; rows[i] = its transverse coordinate.
    """
    a, d = p.a, p.a / _S3
    cr, nn, T, tc = ribbon_cell(edge, N, a)
    nC, nN = len(cr), len(nn)
    dim = 3 * nC + nN
    cr_index = [(3 * i, 3 * i + 1, 3 * i + 2) for i in range(nC)]
    n_orb = [3 * nC + j for j in range(nN)]
    rows = cr[:, tc]

    if exchange is None:
        exchange = np.full(nC, p.cr_shift(spin))
    exchange = np.asarray(exchange, float)

    H0 = np.zeros((dim, dim), complex)
    V = np.zeros((dim, dim), complex)
    # on-site energies (Cr d get the per-site exchange shift; N p_z fixed)
    for i in range(nC):
        H0[3 * i, 3 * i] = p.eps_dz2 + exchange[i]
        H0[3 * i + 1, 3 * i + 1] = p.eps_pi + exchange[i]
        H0[3 * i + 2, 3 * i + 2] = p.eps_pi + exchange[i]
    for j in range(nN):
        H0[n_orb[j], n_orb[j]] = p.eps_pz

    pos = list(cr) + list(nn)
    is_cr = [True] * nC + [False] * nN
    sl = [slice(3 * i, 3 * i + 3) for i in range(nC)] + [slice(n_orb[j], n_orb[j] + 1) for j in range(nN)]
    for A in range(nC + nN):
        for B in range(nC + nN):
            for tau, mat in ((np.zeros(2), H0), (T, V)):     # tau=0 -> H0, tau=+T -> V
                if tau[0] == 0 and tau[1] == 0 and A == B:
                    continue
                blk = _hop_block(is_cr[A], is_cr[B], (pos[B] + tau) - pos[A], p, d)
                if blk is not None:
                    mat[sl[A], sl[B]] += blk
    return H0, V, cr_index, rows


def bands(H0, V, Tlen, nk=200):
    """Band energies over the 1D BZ k in (-pi/T, pi/T]."""
    ks = np.linspace(-np.pi, np.pi, nk) / Tlen
    out = []
    for k in ks:
        Hk = H0 + V * np.exp(1j * k * Tlen) + V.conj().T * np.exp(-1j * k * Tlen)
        out.append(np.linalg.eigvalsh(Hk))
    return ks, np.array(out)
